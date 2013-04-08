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
