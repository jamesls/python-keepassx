#!/usr/bin/env python

import os
import hashlib
import unittest
from datetime import datetime

from keepassx.db import Database, Header, EntryNotFoundError


def open_data_file(name):
    return open(os.path.join(os.path.dirname(os.path.dirname(__file__)),
                             'misc', name))


class TestKeepassX(unittest.TestCase):
    def setUp(self):
        self.kdb_contents = open_data_file('password.kdb').read()


    def test_parse_header(self):
        # I've basically created a kdb file via the GUI and am now
        # verifying the header properties.
        header = Header(self.kdb_contents)
        self.assertEqual(header.HEADER_SIZE, 124)
        self.assertEqual(header.signature1, 0x9AA2D903)
        self.assertEqual(header.signature2, 0xB54BFB65)
        self.assertEqual(header.flags, 3)
        self.assertEqual(header.version, 0x30002)
        self.assertEqual(header.master_seed, ('\xc8\xff\xe9\xca\xad\x8a7\xea'
                                              'w\xd5\x0e\xfe\x16\xdb\t\xad'))
        self.assertEqual(header.encryption_iv, ("\xa8\x15v\xc9\xdf0\x85\x93UD"
                                                "\xf3\x91\xcc\xa7'\x97"))
        self.assertEqual(header.num_groups, 2)
        self.assertEqual(header.num_entries, 3)
        self.assertEqual(header.contents_hash, ('\xec\xdd\xd5U+\x87\xa64\xe7<'
                                                '\x9b"\'6\x05\xe208U2\xe4Lp%'
                                                '\x9d\xd9@tM\xe9@\xd9'))
        self.assertEqual(header.master_seed2, ('\x1f\xb4\xe8-4\xeb\xa1\xc6\x1e'
                                               '\xe8\x15\xc2<\x17L\xe1Y\xf9'
                                               '\x83\xc2\xd2H\x1a%\xca\x9e|'
                                               '\x1ck\x1b\xb5\t'))
        self.assertEqual(header.key_encryption_rounds, 50000)

    def test_database_metadata(self):
        """Header is accessible from database object as the metadata attr."""
        db = Database(self.kdb_contents, 'password')
        self.assertEqual(db.metadata.version, 0x30002)

    def test_encryption_type(self):
        # The code will raise an exception if the hash doesn't match
        # but it's also a good thing for us to test.
        header = Header(self.kdb_contents)
        self.assertEqual(header.encryption_type, 'Rijndael')

    def test_parse_groups_from_decrypted_data(self):
        db = Database(self.kdb_contents, 'password')
        self.assertEqual(len(db.groups), 2)
        self.assertEqual(db.groups[0].group_name, 'Internet')
        self.assertEqual(db.groups[0].groupid, 1876827345)
        self.assertEqual(db.groups[0].level, 0)

    def test_parse_entries_from_decrypted_data(self):
        db = Database(self.kdb_contents, 'password')
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
        db = Database(kdb_contents, 'password', key_file_contents)
        self.assertEqual(db.entries[0].group.group_name, 'Internet')

    def test_entries_can_be_grouped_by_groupid(self):
        db = Database(self.kdb_contents, 'password')
        self.assertEqual(db.entries[0].group.group_name, 'Internet')

    def test_find_entry_by_uuid(self):
        db = Database(self.kdb_contents, 'password')
        entry = db.find_by_uuid('c4d301502050cd695e353b16094be4a7')
        self.assertEqual(entry.uuid, 'c4d301502050cd695e353b16094be4a7')

    def test_find_entry_does_not_exist(self):
        db = Database(self.kdb_contents, 'password')
        with self.assertRaises(EntryNotFoundError):
            entry = db.find_by_uuid('baduuid')

    def test_find_entry_by_title(self):
        db = Database(self.kdb_contents, 'password')
        entry = db.find_by_title('mytitle')
        self.assertEqual(entry.title, 'mytitle')

    def test_search_entry_by_title(self):
        db = Database(self.kdb_contents, 'password')
        entry = db.fuzzy_search_by_title('mytitle')[0]
        self.assertEqual(entry.title, 'mytitle')

        entry = db.fuzzy_search_by_title('myTITLE')[0]
        self.assertEqual(entry.title, 'mytitle')

        entry = db.fuzzy_search_by_title('mytle')[0]
        self.assertEqual(entry.title, 'mytitle')

        entry = db.fuzzy_search_by_title('badvalue')
        self.assertEqual(entry, [])

    def test_search_entry_with_typos(self):
        db = Database(self.kdb_contents, 'password')
        # 'le' has been transposed.
        entry = db.fuzzy_search_by_title('mytitel')[0]
        self.assertEqual(entry.title, 'mytitle')

    def test_find_entry_by_title_does_not_exist(self):
        db = Database(self.kdb_contents, 'password')
        with self.assertRaises(EntryNotFoundError):
            entry = db.find_by_title('badtitle')

    def test_64byte_key(self):
        # keepassx has some special casing of key files if they're
        # 32 or 64 bytes long.
        kdb_contents = open_data_file('password32key.kdb').read()
        key_file_contents = open_data_file('password32key.key').read()
        db = Database(kdb_contents, 'password', key_file_contents)
        self.assertEqual(db.entries[0].group.group_name, 'Internet')

    def test_32byte_key(self):
        # keepassx has some special casing of key files if they're
        # 32 or 64 bytes long.
        kdb_contents = open_data_file('password32byte.kdb').read()
        key_file_contents = open_data_file('password32byte.key').read()
        db = Database(kdb_contents, 'password', key_file_contents)
        self.assertEqual(db.entries[0].group.group_name, 'Internet')


if __name__ == '__main__':
    unittest.main()
