Python KeepassX
===============

.. image:: https://secure.travis-ci.org/jamesls/python-keepassx.png?branch=master
   :target: http://travis-ci.org/jamesls/python-keepassx

.. image:: https://coveralls.io/repos/jamesls/python-keepassx/badge.png?branch=master
   :target: https://coveralls.io/r/jamesls/python-keepassx?branch=master

Python keepassx is a python library and a command line utility for working with
keepassx database files (``.kdb`` files).  This allow you to programatically
access your usernames/passwords instead of having to use the KeePassX GUI.

The ``keepassx`` module currently supports read only operations (adding entries
and creating kdb files are a planned feature).  You can list
your entries::

    $ kp -d password.kdb list
    Password:
    Entries:

    +---------+----------------------------------+-----------+
    | Title   |               Uuid               | GroupName |
    +---------+----------------------------------+-----------+
    | mytitle | c4d301502050cd695e353b16094be4a7 | Internet  |
    +---------+----------------------------------+-----------+

You can also get a username/password::

  $ kp -d password.kdb get username mytitle
  Password:
  myusername

   $ kp -d password.kdb get p mytitle
   Password:
   Password has been copied to clipboard.

You can use either the ``Title`` or the ``Uuid`` to refer to an entry when
getting a username/password.

Python KeepassX is an early project and is undergoing constant development.
