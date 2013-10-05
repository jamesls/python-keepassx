======
Topics
======

Key File Support
================

keepassx fully supports key files.  You can provide a key file
through the ``-k/--key-file`` argument or the ``KP_KEY_FILE``
environment variable.  A key file can be used either as an alternative to a
password or in combination with a password.  By using both a key file and
a password to secure your password database, you will require both something
you know (your password) and something you have (your keyfile) in order to
access the entries in the password database.  For more information on key
files, see the `keepass docs <http://keepass.info/help/base/keys.html#keyfiles>`_.


Config File
===========

Instead of specifying the ``-d/--db-file`` and the ``-k/--keyfile`` everytime
you can instead put these values in a config file.  The config file is
located at ``~/.kpconfig``. and is a yaml file with the following format::

    db_file: /path/to/dbfile.kdb
    key_file: /path/to/keyfile.key

Below is a summary of the options you have available for providing your
db/key file:

.. list-table::
   :header-rows: 1

   * - Config Option
     - Command Line Argument
     - Environment Variable
     - Config File Name
   * - DB File
     - ``-d/--db-file foo.kdb``
     - ``KP_DB_FILE=foo.kdb``
     - ``db_file: foo.kdb``
   * - Key File
     - ``-k/--key-file foo.key``
     - ``KP_KEY_FILE=foo.key``
     - ``key_file: foo.key``


In the table above, the precedence is from left to right.  So, for example,
the ``-d`` option will trump the ``KP_DB_FILE`` option, and the ``KP_DB_FILE``
option will trump the ``db_file:`` value in the ``~/.kpconfig`` config file.
