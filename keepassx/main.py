import sys
import os
import argparse
import getpass

import yaml
from prettytable import PrettyTable

from keepassx.db import Database, encode_password
from keepassx.db import InvalidPasswordError, EntryNotFoundError
from keepassx import clipboard
from keepassx import __version__


CONFIG_FILENAME = os.path.expanduser('~/.kpconfig')


def open_db_file(args):
    if args.db_file is not None:
        db_file = args.db_file
    elif 'KP_DB_FILE' in os.environ:
        db_file = os.environ['KP_DB_FILE']
    else:
        sys.stderr.write("Must supply a db filename.\n")
        sys.exit(1)
    return open(os.path.expanduser(db_file), 'rb')


def open_key_file(args):
    if args.key_file is not None:
        key_file = args.key_file
    elif 'KP_KEY_FILE' in os.environ:
        key_file = os.environ['KP_KEY_FILE']
    else:
        # A keyfile is optional so None can just be returned.
        return None
    return open(os.path.expanduser(key_file), 'rb')


def create_db(args):
    if 'KP_INSECURE_PASSWORD' in os.environ:
        # This env var is really intended for testing purposes.
        # No one should be using this var.
        password = os.environ['KP_INSECURE_PASSWORD']
    elif args.stdin:
        password = sys.stdin.read()
    else:
        password = getpass.getpass('Password: ')

    password = password.strip(' \t\n\r')
    password = encode_password(password)
    db_file = open_db_file(args)
    key_file = open_key_file(args)
    if key_file is not None:
        key_file_contents = key_file.read()
    else:
        # A key file is optional, so it's ok if no key file
        # was specified.
        key_file_contents = None
    db = Database(db_file.read(), password=password,
                  key_file_contents=key_file_contents)
    return db


def do_list(args):
    db = create_db(args)
    t = PrettyTable(['Title', 'Uuid', 'GroupName'])
    t.align['Title'] = 'l'
    t.align['GroupName'] = 'l'
    if args.term is None:
        entries = sorted(db.entries, key=lambda x: x.title.lower())
    else:
        entries = _search_for_entry(db, args.term)
    for entry in entries:
        if entry.group.group_name == 'Backup':
            continue
        t.add_row([entry.title, entry.uuid, entry.group.group_name])
    print(t)


def do_get(args):
    db = create_db(args)
    try:
        entry = _search_for_entry(db, args.entry_id)[0]
    except EntryNotFoundError as e:
        sys.stderr.write(str(e))
        sys.stderr.write("\n")
        return
    default_fields = ['title', 'username', 'url', 'notes']
    if args.entry_fields:
        fields = args.entry_fields
    else:
        fields = default_fields
    sys.stderr.write('\n')
    for field in fields:
        print("%-10s %s" % (field + ':', getattr(entry, field)))
    if args.clipboard_copy:
        clipboard.copy(entry.password)
        sys.stderr.write("\nPassword has been copied to clipboard.\n")

def do_getpwd(args):
    db = create_db(args)
    try:
        entry = _search_for_entry(db, args.entry_id)[0]
    except EntryNotFoundError as e:
        sys.stderr.write(str(e))
        sys.stderr.write("\n")
        return
    print("%s" % (getattr(entry, 'password')))

def _search_for_entry(db, term):
    entries = None
    try:
        entries = [db.find_by_uuid(term)]
    except EntryNotFoundError:
        try:
            entries = [db.find_by_title(term)]
        except EntryNotFoundError:
            # Last try, do a fuzzy match and see if we come up
            # with anything.
            entries = db.fuzzy_search_by_title(term)
            if not entries:
                raise EntryNotFoundError(
                    "Could not find an entry for: %s" % term)
    return entries


def merge_config_file_values(args):
    if os.path.isfile(CONFIG_FILENAME):
        with open(CONFIG_FILENAME, 'r') as f:
            config_data = yaml.safe_load(f)
            if not isinstance(config_data, dict):
                return
        if args.db_file is None:
            args.db_file = config_data.get('db_file')
        if args.key_file is None:
            args.key_file = config_data.get('key_file')


def create_parser():
    parser = argparse.ArgumentParser(prog='kp')
    parser.add_argument('-d', '--db-file',
                        help='The filename of your .kdb file.')
    parser.add_argument('-k', '--key-file',
                        help='The filename of a keyfile. This option is '
                             'only necessary if you have a keyfile associated '
                             'with your .kdb file.')
    parser.add_argument('-s', '--stdin', action='store_true',
                        help='Read the master password from stdin. '
                             'By default, your are prompted to '
                             'type in the master password.  If this '
                             'option is specified, the master '
                             'password will be read from stdin and '
                             'you will not be prompted for your '
                             'master password')
    parser.add_argument('--version', action='version',
                        version='%(prog)s version ' + __version__)
    subparsers = parser.add_subparsers()

    list_parser = subparsers.add_parser('list', help='List entries')
    list_parser.add_argument('term', nargs='?', help='List entries that '
                             'match the specified term.  Can be an entry id, '
                             'a uuid, or anything else supported by the "get" '
                             'command.')
    list_parser.set_defaults(run=do_list)

    get_parser = subparsers.add_parser('get', help='Get password for entry')
    get_parser.add_argument('entry_id', help='Entry name or uuid.')
    get_parser.add_argument('entry_fields', nargs='*',
                            help='Either username or password')
    get_parser.add_argument('-n', '--no-clipboard-copy', action="store_false",
                            dest="clipboard_copy", default=True,
                            help="Don't copy the password to the clipboard")
    get_parser.set_defaults(run=do_get)

    getpwd_parser = subparsers.add_parser('getpwd', help='Get password for entry')
    getpwd_parser.add_argument('entry_id', help='Entry name or uuid.')
    getpwd_parser.set_defaults(run=do_getpwd)

    return parser


def _parse_args(parser, args):
    parsed_args = parser.parse_args(args=args)
    if not hasattr(parsed_args, 'run') and not args:
        # This is for python3.3 support which is different
        # from 2.x.
        # See http://bugs.python.org/issue16308
        # Rather than try to get clever, we just simulate what's suppose to
        # happen which is to print the usage, write a message to stderr and
        # exit.
        parser.print_usage()
        sys.stderr.write('kp: error: too few arguments\n')
        raise SystemExit(2)
    return parsed_args


def main(args=None):
    parser = create_parser()
    args = _parse_args(parser, args)
    merge_config_file_values(args)
    try:
        args.run(args)
    except KeyboardInterrupt:
        sys.stdout.write("\n")
        return 1
    except InvalidPasswordError:
        sys.stderr.write("Invalid password, could not open "
                         "password database.\n")
