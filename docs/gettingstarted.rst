=====================
Getting Started Guide
=====================


This tutorial will walk you through how to get up and running with
python-keepassx.  For the rest of this document, we'll refer to KeePassX GUI as
the original KeePassX desktop application, and ``keepassx`` as the python
library.


Installing keepassx
===================

``keepassx`` is a python package so you can use pip or your preferred methods
to install ``keepassx``.  In this tutorial we'll use pip::


    $ pip install keepassx

.. TODO: need to add common install issues

Should should now have a ``kp`` executable available on the command line::

    $ kp --version
    kp version 0.0.1

You are now ready to start using ``keepassx``.


First Steps
===========

To get started, we're going to use a test database so can expirement with
``kp`` features.

First we need to download the demo database.  You can download the demo
databases `here <https://github.com/jamesls/python-keepassx/raw/master/misc/demo.kdb>`_::

    $ wget https://github.com/jamesls/python-keepassx/raw/master/misc/demo.kdb

The first thing we can do is list the contents of the kdb file.
The password for the demo kdb file is "password".

::

    $ kp -d demo.kdb list
    Password:
    Entries:

    +---------+----------------------------------+-----------+
    | Title   |               Uuid               | GroupName |
    +---------+----------------------------------+-----------+
    | Github  | 477ee351ada4883c7b018a0535ab1a5d | Internet  |
    | Gmail   | 297ee351218556022ef663376783dabd | eMail     |
    | mytitle | c4d301502050cd695e353b16094be4a7 | Internet  |
    +---------+----------------------------------+-----------+


From the output above, we can see that there are three entries available, with
the titles "Github", "Gmail", and "mytitle".  We can get the username and
password of an account in a number of ways.  First, we can refer to the Title
of the entry::


    $ kp -d demo.kdb get Github
    Password:


    title:     Github
    username:  githubuser
    url:       github.com/githubuser
    notes:


    Password has been copied to clipboard.


We can see that the username is "githubuser" and that our password has been
copied to the clipboard.  We can confirm this by pasting the contents.  On a
mac we can run::

    $ echo $(pbpaste)
    mypassword


Efficient Retrieval
-------------------

We can improve how we retrive passwords.  First, we can set an env var so we
don't have to repeatedly type '-d demo.kdb'

::

    $ export KP_DB_FILE=./demo.kdb
    $ kp list
     Password:
     Entries:

     +---------+----------------------------------+-----------+
     | Title   |               Uuid               | GroupName |
     +---------+----------------------------------+-----------+
     | Github  | 477ee351ada4883c7b018a0535ab1a5d | Internet  |
     | Gmail   | 297ee351218556022ef663376783dabd | eMail     |
     | mytitle | c4d301502050cd695e353b16094be4a7 | Internet  |
     +---------+----------------------------------+-----------+


Secondly, we have a few options when specifying the entry we're looking for.
In the example above we used the exact Title of the entry to retrive the entry
details.  However, we can also do the following::

    # Get by uuid
    $ kp get 477ee351ada4883c7b018a0535ab1a5d

    # Case insensitive matching.
    $ kp get github

    # Prefix matching
    $ kp get git

    # Fuzzy matching
    $ kp get githbu


In the case of fuzzy matching, it's possible that multiple results can be
matched.  When this happens, the most relevant entry will be displayed.


Controlling Output
------------------

You can also control which fields are displayed by specifying the fields you
want after a get command.  For example::


    $ kp get github title username
    Password:


    title:     Github
    username:  githubuser


    Password has been copied to clipboard.

In the example above, we are only showing the title and username. The available fields are:

.. list-table::
   :header-rows: 1

   * - Name
     - Description
   * - uuid
     - A unique identifier associated with the entry.
   * - group
     - The group associated with this entry (one Group can have many entries).
   * - imageid
     - The id of the image associated with theis entry.
   * - title
     - The title of the entry.
   * - url
     - A url for the entry.  This can be the login URL for a website.
   * - username
     - The username of the entry.
   * - notes
     - Any misc. notes associated with the entry.
   * - creation_time
     - The time the entry was created.
   * - last_mod_time
     - The time the entry was last modified.
   * - last_acc_time
     - The time the entry was last accessed.
   * - expiration_time
     - The time the entry expires.


Next steps
==========

This tutorial covered using an existing kdb file to list and get passwords.
The next steps would be to create your own kdb files.  Currently,
``python-keepassx`` does not support creating kdb files (though this is a
planned feature).  For now you will have to `download keepassx
<http://www.keepassx.org/downloads>`_ and create your own kdb files.

Another powerful feature of keepassx worth investivating is using keyfiles.
``python-keepassx`` supports keyfiles via the `-k` argument or the
``KP_KEY_FILE`` environment variable.
