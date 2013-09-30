===============
python-keepassx
===============

`KeePassX`_ is a cross platform password manager.  However, KeePassX is a desktop
GUI application.  That's where ``python-keepassx`` comes in.  By using
``python-keepassx``, you can access your passwords using a command line
interface to KeePassX.  You can also use the python library directly in your
own python applications.


What is this project and why should I care?
-------------------------------------------

Keepassx is a great password manager.  However, if you're like me, you're in
the terminal frequently.  It would be better if you could access your passwords
in the terminal, or even better, in the python code you write.  python-keepassx
can read and write the database files that keepassx uses, and in doing so
allows you to access your passwords.


I've never heard of a password manager, what is it?
---------------------------------------------------

We use things that require passwords.  From social media such as Facebook,
Twitter, and Instagram to things like online banking and tax returns nearly
everything we access requires a username and password.  It's not uncommon these
days to require over 100 passwords.

If you're following `password best practices`_, you should not be using the
same password for more than one site.  This makes sense, if you use the same
password for your Facebook account and your online banking account, if someone
gets your Facebook password, they can now access your online banking account.
Also, you shouldn't be using passwords that are easy to guess: no dictionary
words, birthdays, family and pet names, addresses, or any personal information.
How do we deal with the fact that we need to create and remember 100s of these
passwords?

That's where a password manager comes into play.  A password manager is an
application that you use to enter all of your passwords and usernames.  This
database of passwords is then secured with some form of a master password.

Now whenver you need to log in to a site, you use the password manager, and
enter your master password to gain access to the site specific password.

The benefit of this approach is that you can still use a unique (and even
randomly generated) password for each password, but at the same time only have
to remember a single master password.


I've never hard of KeePassx, what is it?
----------------------------------------

KeePassX is a password manager.  Check out it's `homepage
<http://www.keepassx.org/>`_.  It is based off of the `KeePass
<http://keepass.info/>`_ application, which is only available on windows.

Some of the biggest benefits for using keepassx including:

* Free
* Cross platform
* Open source

The last two options are a really big deal.  I use keepassx on windows
linux, mac, iPhone, and Ipad.  The fact that it's open source makes it easy to
port to any platform.  It also makes it easy to audit the code and see exactly
how it's storing your passwords.  The fact that it's open source means you
never have to worry about a vendor going away and you being completely out of
luck.



I'd like to try out this project, what do I do?
-----------------------------------------------

Check out the :doc:`gettingstarted` for an introduction
to using python-keepassx.


I just want reference/API docs, where are they?
-----------------------------------------------

Check out the reference docs here: :doc:`reference`.



=================
Table of Contents
=================


.. toctree::
   :maxdepth: 2

   gettingstarted
   topics
   reference


==================
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _password best practices: https://www.schneier.com/blog/archives/2009/08/password_advice.html
.. _KeePassX: http://www.keepassx.org/
