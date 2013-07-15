import unittest
import tempfile
import yaml

import mock

from keepassx.main import merge_config_file_values
from keepassx.main import create_parser


class TestConfigMerging(unittest.TestCase):
    """Tests for config file merging."""

    def setUp(self):
        self.temp = tempfile.NamedTemporaryFile()
        self.config_patch = mock.patch('keepassx.main.CONFIG_FILENAME',
                                        self.temp.name)
        self.config_patch.start()

    def tearDown(self):
        self.config_patch.stop()

    def set_config_values(self, values):
        with open(self.temp.name, 'w') as f:
            f.write(yaml.safe_dump(values))

    def test_config_values_are_merged_in(self):
        tmp_filename = '/tmp/foobar'
        self.set_config_values({
            'db_file': tmp_filename,
            'key_file': 'keyfile',
        })
        parser = create_parser()
        args = parser.parse_args('list'.split())
        self.assertIsNone(args.db_file)
        self.assertIsNone(args.key_file)
        merge_config_file_values(args)
        self.assertEqual(args.db_file, tmp_filename)
        self.assertEqual(args.key_file, 'keyfile')

    def test_config_file_not_a_dict(self):
        tmp_filename = '/tmp/foobar'
        self.set_config_values(None)
        parser = create_parser()
        args = parser.parse_args('-d foo list'.split())
        merge_config_file_values(args)
        self.assertIsNone(args.key_file)
        self.assertEqual(args.db_file, 'foo')
