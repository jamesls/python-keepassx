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

To get started, we're going to use a test database so can experiement with
``kp`` features.  Later parts of this tutorial will show you how to use
your existing password database (if you are an existing KeePassX desktop
application user).

First we need to create a new database where we can store our passwords.
To do this, we need to specify a file location and our master password.

    $ kp create ~/.passwords
    Enter master password:
    Confirm password:
    Password database created at ~/.passwords

Once we have a password database created we can now add passwords to our
database::

    $ kp new --title "Gmail" --username "example@gmail.com"
    Enter password:
    Confirm password:
    New entry successfully created.

Now our password is securely stored in our password database.  To
retrieve our password for our new entry, we can use the ``kp get``
command with our master password::

    $ kp get Gmail
    Enter master password:
    Password copied to clipboard.

Our password for our entry has now been copied to our clipboard.
If we paste the contents of the clipboard, we'll see our password.


Next Steps
==========

In the previous section, we saw how to create a database, create a
new entry, and then retrieve our entry.  KeepassX supports more advanced
features, which we'll explore in this section.

Groups
------

A password entry is associated with a single group.  This allows you
to group your passwords.  In our example above, we did not specify
a group name so it used the default group of "General".  Instead
let's create two new entries.  Let's say we want to store our work
email password and our personal email password::

    $ kp new --group "Work" --title "Gmail" --username "example2@gmail.com"
    Enter password:
    Confirm password:
    New entry successfully created.

    $ kp new --group "Personal" --title "Gmail" --username "example3@gmail.com"
    Enter password:
    Confirm password:
    New entry successfully created.


To retrieve our password, we can say::


    $ kp get Work Gmail
    Enter master password:
    Password copied to clipboard.

    $ kp get Personal Gmail
    Enter master password:
    Password copied to clipboard.


Creating Entries in an Editor
-----------------------------

You can also create an entry in an editor.  This is useful
if you don't want to remember all the parameters used to create
an entry.  KeepassX also has other fields in an entry you can
specify (URL, Comment, Expires).  To use this use the ``--interactive``
option when creating an entry::

    $ kp new --interactive

Your editor will open with a template for you to fill in::

    # Please fill in the fields below.
    Group: General
    Title:
    Username:
    URL:
    Comment:
    Expires: Never

Fill in the fields with the appropriate values::

    # Please fill in the fields below.
    Group: Work
    Title: Gmail2
    Username: example5@gmail.com
    URL: https://gmail.com
    Comment: Second email address for work.
    Expires: Never

When you're done, save and exit your editor.
You will then be prompted for a password::

    $ kp new --interactive
    Enter password:
    Confirm password:
    New entry successfully created.


Generating Passwords
--------------------

One of the benefits for using a password manager is that
you can use random (and long) passwords that you don't
have to remember.  You can allow KeepassX to generate a
secure password for you.  You can control the parameters
of the password (length, characters to use, etc.) to ensure
an application might place on a password.
