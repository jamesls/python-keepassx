#!/usr/bin/env python

import os
import hashlib
import unittest
from datetime import datetime

from keepassx.db import Database, Header


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
        self.assertEqual(len(db.entries), 3)
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
        key_file = open_data_file('passwordkey.key').name
        db = Database(kdb_contents, 'password', key_file)


if __name__ == '__main__':
    unittest.main()
