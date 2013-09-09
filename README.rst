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

    +---------+----------------------------------+-----------+
    | Title   |               Uuid               | GroupName |
    +---------+----------------------------------+-----------+
    | mytitle | c4d301502050cd695e353b16094be4a7 | Internet  |
    +---------+----------------------------------+-----------+

You can also get a username/password::

    $ kp -d demo.kdb get Github
    Password:


    title:     Github
    username:  githubuser
    url:       github.com/githubuser
    notes:


    Password has been copied to clipboard.

Check out the `docs`_ and the `getting started guide`_ for more info.

Python KeepassX is an early project and is undergoing constant development.


.. _docs: http://keepassx.readthedocs.org/
.. _getting started guide: http://keepassx.readthedocs.org/en/latest/gettingstarted.html
