#!/usr/bin/env python

import os
import unittest
from datetime import datetime

from keepassx.db import Database, Header, EntryNotFoundError
from keepassx.db import encode_password


def open_data_file(name):
    return open(os.path.join(os.path.dirname(os.path.dirname(__file__)),
                             'misc', name), 'rb')


class TestKeepassX(unittest.TestCase):
    def setUp(self):
        self.kdb_contents = open_data_file('password.kdb').read()
        self.password = b'password'

    def test_parse_header(self):
        # I've basically created a kdb file via the GUI and am now
        # verifying the header properties.
        header = Header(self.kdb_contents)
        self.assertEqual(header.HEADER_SIZE, 124)
        self.assertEqual(header.signature1, 0x9AA2D903)
        self.assertEqual(header.signature2, 0xB54BFB65)
        self.assertEqual(header.flags, 3)
        self.assertEqual(header.version, 0x30002)
        self.assertEqual(header.master_seed, (b'\xc8\xff\xe9\xca\xad\x8a7\xeaw'
                                              b'\xd5\x0e\xfe\x16\xdb\t\xad'))
        self.assertEqual(header.encryption_iv, (b"\xa8\x15v\xc9\xdf0\x85\x93UD"
                                                b"\xf3\x91\xcc\xa7'\x97"))
        self.assertEqual(header.num_groups, 2)
        self.assertEqual(header.num_entries, 3)
        self.assertEqual(header.contents_hash, (b'\xec\xdd\xd5U+\x87\xa64\xe7<'
                                                b'\x9b"\'6\x05\xe208U2\xe4Lp%'
                                                b'\x9d\xd9@tM\xe9@\xd9'))
        self.assertEqual(header.master_seed2, b'\x1f\xb4\xe8-4\xeb\xa1\xc6\x1e'
                                              b'\xe8\x15\xc2<\x17L\xe1Y\xf9'
                                              b'\x83\xc2\xd2H\x1a%\xca\x9e|'
                                              b'\x1ck\x1b\xb5\t')
        self.assertEqual(header.key_encryption_rounds, 50000)

    def test_database_metadata(self):
        """Header is accessible from database object as the metadata attr."""
        db = Database(self.kdb_contents, self.password)
        self.assertEqual(db.metadata.version, 0x30002)

    def test_encryption_type(self):
        # The code will raise an exception if the hash doesn't match
        # but it's also a good thing for us to test.
        header = Header(self.kdb_contents)
        self.assertEqual(header.encryption_type, 'Rijndael')

    def test_parse_groups_from_decrypted_data(self):
        db = Database(self.kdb_contents, self.password)
        self.assertEqual(len(db.groups), 2)
        self.assertEqual(db.groups[0].group_name, 'Internet')
        self.assertEqual(db.groups[0].groupid, 1876827345)
        self.assertEqual(db.groups[0].level, 0)

    def test_parse_entries_from_decrypted_data(self):
        db = Database(self.kdb_contents, self.password)
        self.assertEqual(len(db.entries), 1)
        entry = db.entries[0]
        self.assertEqual(entry.title, 'mytitle')
        self.assertEqual(entry.uuid, 'c4d301502050cd695e353b16094be4a7')
        self.assertEqual(entry.groupid, 1876827345)
        self.assertEqual(entry.url, 'myurl')
        self.assertEqual(entry.username, 'myusername')
        self.assertEqual(entry.password, 'mypassword')
        self.assertEqual(entry.notes, '')
        self.assertEqual(entry.creation_time, datetime(2012, 7, 14, 13, 17, 8))

    def test_parse_entries_from_decrypted_data_with_key_file(self):
        kdb_contents = open_data_file('passwordkey.kdb').read()
        key_file_contents = open_data_file('passwordkey.key').read()
        db = Database(kdb_contents, self.password, key_file_contents)
        self.assertEqual(db.entries[0].group.group_name, 'Internet')

    def test_entries_can_be_grouped_by_groupid(self):
        db = Database(self.kdb_contents, self.password)
        self.assertEqual(db.entries[0].group.group_name, 'Internet')

    def test_find_entry_by_uuid(self):
        db = Database(self.kdb_contents, self.password)
        entry = db.find_by_uuid('c4d301502050cd695e353b16094be4a7')
        self.assertEqual(entry.uuid, 'c4d301502050cd695e353b16094be4a7')

    def test_find_entry_does_not_exist(self):
        db = Database(self.kdb_contents, self.password)
        with self.assertRaises(EntryNotFoundError):
            db.find_by_uuid('baduuid')

    def test_find_entry_by_title(self):
        db = Database(self.kdb_contents, self.password)
        entry = db.find_by_title('mytitle')
        self.assertEqual(entry.title, 'mytitle')

    def test_search_entry_by_title(self):
        db = Database(self.kdb_contents, self.password)
        entry = db.fuzzy_search_by_title('mytitle')[0]
        self.assertEqual(entry.title, 'mytitle')

        entry = db.fuzzy_search_by_title('myTITLE')[0]
        self.assertEqual(entry.title, 'mytitle')

        entry = db.fuzzy_search_by_title('mytle')[0]
        self.assertEqual(entry.title, 'mytitle')

        entry = db.fuzzy_search_by_title('badvalue')
        self.assertEqual(entry, [])

    def test_search_entry_with_typos(self):
        db = Database(self.kdb_contents, self.password)
        # 'le' has been transposed.
        entry = db.fuzzy_search_by_title('mytitel')[0]
        self.assertEqual(entry.title, 'mytitle')

    def test_find_entry_by_title_does_not_exist(self):
        db = Database(self.kdb_contents, self.password)
        with self.assertRaises(EntryNotFoundError):
            db.find_by_title('badtitle')

    def test_64byte_key(self):
        # keepassx has some special casing of key files if they're
        # 32 or 64 bytes long.
        kdb_contents = open_data_file('password64byte.kdb').read()
        key_file_contents = open_data_file('password64byte.key').read()
        db = Database(kdb_contents, self.password, key_file_contents)
        self.assertEqual(db.entries[0].group.group_name, 'Internet')

    def test_32byte_key(self):
        # keepassx has some special casing of key files if they're
        # 32 or 64 bytes long.
        kdb_contents = open_data_file('password32byte.kdb').read()
        key_file_contents = open_data_file('password32byte.key').read()
        db = Database(kdb_contents, self.password, key_file_contents)
        self.assertEqual(db.entries[0].group.group_name, 'Internet')

    def test_64byte_key_no_password(self):
        kdb_contents = open_data_file('passwordlesskey.kdb').read()
        key_file_contents = open_data_file('passwordlesskey.key').read()
        db = Database(kdb_contents, b'', key_file_contents)
        self.assertEqual(db.entries[0].group.group_name, 'Internet')

    def test_multi_entry_exact_search(self):
        # This particular kdb file has multiple entries with the title
        # "mytitle".
        kdb_contents = open_data_file('passwordmultientry.kdb').read()
        db = Database(kdb_contents, self.password)
        self.assertEqual(len(db.entries), 3)
        matches = db.fuzzy_search_by_title('mytitle')
        self.assertEqual(len(matches), 3)
        self.assertEqual(matches[0].title, 'mytitle')
        self.assertEqual(matches[1].title, 'mytitle')
        self.assertEqual(matches[2].title, 'mytitle')

    def test_multi_entry_case_insensitive_search(self):
        kdb_contents = open_data_file('passwordmultientry.kdb').read()
        db = Database(kdb_contents, self.password)
        self.assertEqual(len(db.entries), 3)
        matches = db.fuzzy_search_by_title('mYtItlE')
        self.assertEqual(len(matches), 3)
        self.assertEqual(matches[0].title, 'mytitle')
        self.assertEqual(matches[1].title, 'mytitle')
        self.assertEqual(matches[2].title, 'mytitle')

    def test_fuzzy_search_ignore_groups(self):
        kdb_contents = open_data_file('passwordmultientry.kdb').read()
        db = Database(kdb_contents, self.password)
        # There are 3 entries in the db with 'mytitle' titles.
        # 1 of the entries is in the Backup group.  If we
        # specify ignore_groups in our search, we should not
        # get the entry in the Backup group.
        matches = db.fuzzy_search_by_title('mytitle',
                                           ignore_groups=['Backup'])
        self.assertEqual(len(matches), 2)
        self.assertEqual(matches[0].title, 'mytitle')
        self.assertEqual(matches[1].title, 'mytitle')

        self.assertNotEqual(matches[0].group.group_name,
                            'Backup')
        self.assertNotEqual(matches[1].group.group_name,
                            'Backup')

    def test_master_password_latin1(self):
        password = u"\u00f6\u00e4\u00fc\u00df"
        kdb_contents = open_data_file('password-latin1.kdb').read()
        db = Database(kdb_contents, encode_password(password))
        self.assertEqual(len(db.groups), 2)

    def test_master_password_unicode(self):
        kdb_contents = open_data_file('password-unicode.kdb').read()
        db = Database(kdb_contents, encode_password(u'password\u2713'))
        # Verify we can read anything from the db.
        self.assertEqual(len(db.groups), 2)


class TestEncodePassword(unittest.TestCase):
    def test_encode_ascii(self):
        self.assertEqual(encode_password('foo'), b'foo')

    def test_encode_cp1252_compatible_chars(self):
        self.assertEqual(encode_password(u"\u00f6"), b'\xf6')

    def test_non_cp1252_compatible_chars_replaced(self):
        self.assertEqual(encode_password(u"\u2713"), b'?')
        # And to show you how terrible keepass's encoding
        # is:
        self.assertEqual(encode_password(u"\u2714"), b'?')
        # Or in other words:
        self.assertEqual(encode_password(u"\u2714"),
                         encode_password(u"\u2713"))
