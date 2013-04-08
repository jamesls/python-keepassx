import sys
import os
import argparse
import getpass

from keepassx.db import Database, EntryNotFoundError
from keepassx import clipboard
from keepassx import __version__


def open_db_file(args):
    if args.db_file is not None:
        return args.db_file
    elif 'KP_DB_FILE' in os.environ:
        return open(os.environ['KP_DB_FILE'])
    else:
        sys.stderr.write("Must supply a db filename.\n")
        sys.exit(1)


def open_key_file(args):
    if args.key_file is not None:
        return args.key_file
    elif 'KP_KEY_FILE' in os.environ:
        return open(os.environ['KP_DB_FILE'])
    else:
        # A keyfile is optional so None can just be returned.
        return None


def create_db(args):
    if 'KP_INSECURE_PASSWORD' in os.environ:
        # This env var is really intended for testing purposes.
        # No one should be using this var.
        password = os.environ['KP_INSECURE_PASSWORD']
    else:
        password = getpass.getpass('Password: ')
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
    print "Entries:\n"
    for entry in db.entries:
        print entry.title, entry.uuid, entry.group.group_name


def do_get(args):
    db = create_db(args)
    try:
        entry = db.find_by_uuid(args.entry_id)
    except EntryNotFoundError:
        try:
            entry = db.find_by_title(args.entry_id)
        except EntryNotFoundError:
            sys.stderr.write(
                "Could not find an entry for: %s\n" % args.entry_id)
    if args.entry_type == 'username':
        print entry.username
    elif args.entry_type == 'password':
        clipboard.copy(entry.password)


def main(args=None):
    parser = argparse.ArgumentParser(prog='kp')
    parser.add_argument('-k', '--key-file', type=argparse.FileType('r'))
    parser.add_argument('-d', '--db-file', type=argparse.FileType('r'))
    parser.add_argument('--version', action='version',
                        version='%(prog)s version ' + __version__)
    subparsers = parser.add_subparsers()

    list_parser = subparsers.add_parser('list', help='List entries')
    list_parser.set_defaults(run=do_list)

    get_parser = subparsers.add_parser('get', help='Get password for entry')
    get_parser.add_argument('entry_type', help='Either username of password')
    get_parser.add_argument('entry_id', help='Either username of password')
    get_parser.set_defaults(run=do_get)

    args = parser.parse_args(args=args)
    args.run(args)
