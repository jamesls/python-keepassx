import struct
import hashlib
import datetime
import binascii
import difflib
from pprint import pformat

from Crypto.Cipher import AES
from six.moves import xrange
from six import integer_types

SYSTEM_USER_UUID = '00000000000000000000000000000000'


class EntryNotFoundError(Exception):
    pass


class Header(object):
    """Header information for the keepass database.

    From the KeePass doc::

      Database header: [DBHDR]

      [ 4 bytes] DWORD    dwSignature1  = 0x9AA2D903
      [ 4 bytes] DWORD    dwSignature2  = 0xB54BFB65
      [ 4 bytes] DWORD    dwFlags
      [ 4 bytes] DWORD    dwVersion       { Ve.Ve.Mj.Mj:Mn.Mn.Bl.Bl }
      [16 bytes] BYTE{16} aMasterSeed
      [16 bytes] BYTE{16} aEncryptionIV
      [ 4 bytes] DWORD    dwGroups        Number of groups in database
      [ 4 bytes] DWORD    dwEntries       Number of entries in database
      [32 bytes] BYTE{32} aContentsHash   SHA-256 hash value of the plain contents
      [32 bytes] BYTE{32} aMasterSeed2    Used for the dwKeyEncRounds AES
                                          master key transformations
      [ 4 bytes] DWORD    dwKeyEncRounds  See above; number of transformations

      Notes:

      - dwFlags is a bitmap, which can include:
        * PWM_FLAG_SHA2     (1) for SHA-2.
        * PWM_FLAG_RIJNDAEL (2) for AES (Rijndael).
        * PWM_FLAG_ARCFOUR  (4) for ARC4.
        * PWM_FLAG_TWOFISH  (8) for Twofish.
      - aMasterSeed is a salt that gets hashed with the transformed user master key
        to form the final database data encryption/decryption key.
        * FinalKey = SHA-256(aMasterSeed, TransformedUserMasterKey)
      - aEncryptionIV is the initialization vector used by AES/Twofish for
        encrypting/decrypting the database data.
      - aContentsHash: "plain contents" refers to the database file, minus the
        database header, decrypted by FinalKey.
        * PlainContents = Decrypt_with_FinalKey(DatabaseFile - DatabaseHeader)

    """

    STRUCTURE = [
        ('signature1', 4, 'I'),
        ('signature2', 4, 'I'),
        ('flags', 4, 'I'),
        ('version', 4, 'I'),
        ('master_seed', 16, '16s'),
        ('encryption_iv', 16, '16s'),
        ('num_groups', 4, 'I'),
        ('num_entries', 4, 'I'),
        ('contents_hash', 32, '32s'),
        ('master_seed2', 32, '32s'),
        ('key_encryption_rounds', 4, 'I'),
    ]
    HEADER_SIZE = sum(_s[1] for _s in STRUCTURE)

    ENCRYPTION_TYPES = [
        ('SHA2', 1),
        ('Rijndael', 2),
        ('AES', 2),
        ('ArcFour', 4),
        ('TwoFish', 8),
    ]

    def __init__(self, contents):
        self.signature1 = None
        self.signature2 = None
        self.flags = None
        self.version = None
        self.master_seed = None
        self.encryption_iv = None
        self.num_groups = None
        self.num_entries = None
        self.contents_hash = None
        self.master_seed2 = None
        self.key_encryption_rounds = None
        self._populate_fields(contents)

    def _populate_fields(self, contents):
        index = 0
        for name, num_bytes, spec in self.STRUCTURE:
            setattr(self, name,
                    struct.unpack('<' + spec,
                                  contents[index:index+num_bytes])[0])
            index += num_bytes

    @property
    def encryption_type(self):
        for name, value in self.ENCRYPTION_TYPES[1:]:
            if value & self.flags:
                return name

    def __repr__(self):
        return pformat(self.__dict__)


class Database(object):
    """Database representing a KDB file."""
    def __init__(self, contents, password=None, key_file_contents=None):
        self.metadata = Header(contents[:Header.HEADER_SIZE])
        payload = self._decrypt_payload(
            contents[Header.HEADER_SIZE:],
            self._calculate_key(password.encode('utf-8'), key_file_contents,
                                self.metadata.master_seed,
                                self.metadata.master_seed2,
                                self.metadata.key_encryption_rounds),
            self.metadata.encryption_type,
            self.metadata.encryption_iv
        )
        self.groups, self.entries = self._parse_payload(payload)

    def _decrypt_payload(self, payload, key, encryption_type, iv):
        if encryption_type != 'Rijndael':
            raise ValueError("Unsupported encryption type: %s" %
                             encryption_type)
        decryptor = AES.new(key, AES.MODE_CBC, iv)
        payload = decryptor.decrypt(payload)
        extra = payload[-1]
        if not isinstance(payload[-1], integer_types):
            # Python 2.
            extra = ord(extra)
        payload = payload[:len(payload)-extra]
        if self.metadata.contents_hash != hashlib.sha256(payload).digest():
            raise ValueError("Decryption failed, decrypted checksum "
                             "does not match.")
        return payload

    def _calculate_key(self, password, key_file_contents,
                       seed1, seed2, num_rounds):
        # Based on Kdb3Database::setCompositeKey and Kdb3Database::loadReal.
        key = hashlib.sha256(password).digest()
        if key_file_contents is not None:
            # The key derivation also supports a few extra modes, if the key
            # file is 32 bytes, use that directly instead of taking the sha256
            # of the contents, if it's 64 bits, assume it's hex encoded and
            # decode and use the contents directly instead of taking the sha256
            # hash.
            if len(key_file_contents) == 64:
                # Then the key file contents is treated as hex and we
                # use the converted-to-binary contents as the file
                # key hash.
                file_key_hash = binascii.unhexlify(key_file_contents)
            elif len(key_file_contents) == 32:
                file_key_hash = key_file_contents
            else:
                file_key_hash = hashlib.sha256(key_file_contents).digest()
            key = hashlib.sha256(key + file_key_hash).digest()
        cipher = AES.new(seed2, AES.MODE_ECB)
        for i in xrange(num_rounds):
            key = cipher.encrypt(key)
        key = hashlib.sha256(key).digest()
        return hashlib.sha256(seed1 + key).digest()

    def _parse_payload(self, payload):
        groups, i = self._parse_groups_payload(payload)
        groups_by_groupid = dict((g.groupid, g) for g in groups)
        payload = payload[i:]
        entries = self._parse_entries_payload(payload)
        for entry in entries:
            entry.group = groups_by_groupid[entry.groupid]
        return groups, entries

    def _parse_groups_payload(self, payload):
        i = 0
        ignore = object()
        group_types = {
            0x0: ('ignored', BaseType),
            0x1: ('groupid', IntegerType),
            0x2: ('group_name', StringType),
            0x3: (ignore, DateType),
            0x4: (ignore, DateType),
            0x5: (ignore, DateType),
            0x6: (ignore, DateType),
            0x7: ('imageid', IntegerType),
            0x8: ('level', ShortType),
            0x9: ('flags', IntegerType),
            0xFFFF: (None, None),
            }
        groups = []
        for _ in xrange(self.metadata.num_groups):
            group = Group()
            while True:
                # The payload has a structure of
                # 2 bytes - field type
                # 4 bytes - length of field
                # n bytes - the field data
                # The way that the n bytes are interpreted will
                # depend on what the field type is.  Some will
                # be ints, some will be dates, some will be strings, etc.
                # So first read the field type and the field size.
                header = payload[i:i+6]
                i += 6
                # < == little endian
                # H == unsigned short, 2 bytes
                # I == unsigned int, 4 bytes
                field_type, field_size = struct.unpack('<HI', header)
                field_data = payload[i:i+field_size]
                i += field_size
                name, decoder = group_types[field_type]
                if name is ignore:
                    continue
                elif name is None:
                    break
                else:
                    setattr(group, name, decoder.decode(field_data))
            groups.append(group)
        return groups, i

    def _parse_entries_payload(self, payload):
        entry_types = {
            0x0: ('ignored', BaseType),
            0x1: ('uuid', UUIDType),
            0x2: ('groupid', IntegerType),
            0x3: ('imageid', IntegerType),
            0x4: ('title', StringType),
            0x5: ('url', StringType),
            0x6: ('username', StringType),
            0x7: ('password', StringType),
            0x8: ('notes', StringType),
            0x9: ('creation_time', DateType),
            0xa: ('last_mod_time', DateType),
            0xb: ('last_acc_time', DateType),
            0xc: ('expiration_time', DateType),
            0xd: ('binary_desc', StringType),
            0xe: ('binary_data', BaseType),
            0xFFFF: (None, None),
        }
        i = 0
        entries = []
        for _ in xrange(self.metadata.num_entries):
            entry = Entry()
            while True:
                # The payload has a structure of
                # 2 bytes - field type
                # 4 bytes - length of field
                # n bytes - the field data
                # The way that the n bytes are interpreted will
                # depend on what the field type is.  Some will
                # be ints, some will be dates, some will be strings, etc.
                # So first read the field type and the field size.
                header = payload[i:i+6]
                i += 6
                # < == little endian
                # H == unsigned short, 2 bytes
                # I == unsigned int, 4 bytes
                field_type, field_size = struct.unpack('<HI', header)
                field_data = payload[i:i+field_size]
                i += field_size
                name, decoder = entry_types[field_type]
                if name is None:
                    break
                else:
                    setattr(entry, name, decoder.decode(field_data))
            if entry.uuid != SYSTEM_USER_UUID:
                entries.append(entry)
        return entries

    def find_by_uuid(self, uuid):
        """Find an entry by uuid.

        :raise: EntryNotFoundError
        """
        for entry in self.entries:
            if entry.uuid == uuid:
                return entry
        raise EntryNotFoundError("Entry not found for uuid: %s" % uuid)

    def find_by_title(self, title):
        """Find an entry by exact title.

        :raise: EntryNotFoundError

        """
        for entry in self.entries:
            if entry.title == title:
                return entry
        raise EntryNotFoundError("Entry not found for title: %s" % title)

    def fuzzy_search_by_title(self, title):
        """Find an entry by by fuzzy match.

        This will check things such as:

            * case insensitive matching
            * typo checks
            * prefix matches

        Returns a list of matches (an empty list is returned if no matches are
        found).

        """
        # Exact matches trump
        found = []
        for entry in self.entries:
            if entry.title == title:
                return [entry]
        # Case insensitive matches next.
        title_lower = title.lower()
        for entry in self.entries:
            if entry.title.lower() == title.lower():
                return [entry]
        # Subsequence/prefix matches next.
        entries = []
        for entry in self.entries:
            if self._is_subsequence(title_lower, entry.title.lower()):
                entries.append(entry)
        if entries:
            return entries
        # Finally close matches that might have mispellings.
        entry_map= {entry.title.lower(): entry for entry in self.entries}
        matches = difflib.get_close_matches(
            title.lower(), entry_map.keys(), cutoff=0.7)
        if matches:
            return [entry_map[name] for name in matches]
        return []

    def _is_subsequence(self, short_str, full_str):
        current_index = 0
        for i in range(len(full_str)):
            if short_str[current_index] == full_str[i]:
                current_index += 1
            if current_index == len(short_str):
                return True
        return False


class Group(object):
    """The group associated with an entry."""
    def __init__(self):
        self.ignored = None
        self.groupid = None
        self.group_name = None
        self.imageid = None
        self.level = None
        self.flags = None

    def __repr__(self):
        return 'Group(groupid=%s, group_name=%s)' % (
            self.groupid, self.group_name)


class Entry(object):
    """A password entry in a KDB file."""
    def __init__(self):
        self.ignored = None
        self.uuid = None
        self.groupid = None
        self.imageid = None
        self.title = None
        self.url = None
        self.username = None
        self.password = None
        self.notes = None
        self.creation_time = None
        self.last_mod_time = None
        self.last_acc_time = None
        self.expiration_time = None
        self.binary_desc = None
        self.binary_data = None
        # This is filled in when the database
        # is initially loaded (a Group object with
        # a matching groupid is populated).
        self.group = None

    def __repr__(self):
        return "Entry(uuid=%s, title=%s)" % (
            self.uuid, self.title)


class BaseType(object):
    @staticmethod
    def decode(payload):
        return payload


class UUIDType(object):
    @staticmethod
    def decode(payload):
        return binascii.b2a_hex(payload).decode('utf-8').replace('\0', '')


class StringType(BaseType):
    @staticmethod
    def decode(payload):
        # Strings are null terminated.
        return payload.decode('utf-8').replace('\0', '')


class IntegerType(BaseType):
    @staticmethod
    def decode(payload):
        return struct.unpack('<I', payload)[0]


class ShortType(BaseType):
    @staticmethod
    def decode(payload):
        return struct.unpack("<H", payload)[0]


class DateType(BaseType):
    @staticmethod
    def decode(payload):
        # Little endian 5 unsigned chars.
        # Based off of keepassx 0.4.3 source:
        # Kdb3Database.cpp: Kdb3Database::dateFromPackedStruct5
        uchar = struct.unpack('<5B', payload)
        year = (uchar[0] << 6) | (uchar[1] >> 2)
        month = ((uchar[1] & 0x00000003) << 2) | (uchar[2] >> 6);
        day = (uchar[2] >> 1) & 0x0000001F
        hour = ((uchar[2] & 0x00000001) << 4) | (uchar[3] >> 4)
        minutes = ((uchar[3] &0x0000000F) << 2) | (uchar[4] >> 6)
        seconds = uchar[4] & 0x0000003F
        return datetime.datetime(year, month, day, hour, minutes, seconds)
