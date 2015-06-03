Python KeepassX
===============

.. image:: https://secure.travis-ci.org/jamesls/python-keepassx.png?branch=master
   :target: http://travis-ci.org/jamesls/python-keepassx

.. image:: https://coveralls.io/repos/jamesls/python-keepassx/badge.png?branch=master
   :target: https://coveralls.io/r/jamesls/python-keepassx?branch=master

`KeePassX`_ is a cross platform password manager.  However, KeePassX is a desktop
GUI application.  That's where ``python-keepassx`` comes in.  By using
``python-keepassx``, you can access your passwords using a command line
interface to KeePassX.  You can also use the python library directly in your
own python applications.

Python-keepassx: **simple**, command line interface to your passwords.


::

    $ kp -d password.kdb list
    Password:

    +---------+----------------------------------+-----------+
    | Title   |               Uuid               | GroupName |
    +---------+----------------------------------+-----------+
    | mytitle | c4d301502050cd695e353b16094be4a7 | Internet  |
    +---------+----------------------------------+-----------+


    $ kp -d demo.kdb get Github
    Password:

    title:     Github
    username:  githubuser
    url:       github.com/githubuser
    notes:


    Password has been copied to clipboard.


Aren't there similar projects already?
--------------------------------------

Yes.  This project is different because it has:

* A simple, straightforward API.
* Full support for key files.
* Both a command line interface and a python API.
* Support for python 2.7, 3.3, and 3.4 (and higher).


Documentation
=============

Check out the `docs`_ and the `getting started guide`_ for more info.

Check out the `changelog`_ to see what's in the latest release.


.. _docs: http://keepassx.readthedocs.org/
.. _getting started guide: http://keepassx.readthedocs.org/en/latest/gettingstarted.html
.. _changelog: http://keepassx.readthedocs.org/en/latest/#changelog
.. _KeePassX: https://www.keepassx.org/
