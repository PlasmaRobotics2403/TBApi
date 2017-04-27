.. currentmodule:: tbapi
.. TBApi documentation master file, created by
   sphinx-quickstart on Tue Apr 25 17:08:22 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

#####################################################
TBApi - A Python Wrapper for The Blue Alliance API v3
#####################################################

************
Installation
************

Python3+ is required for usage with TBApi.  To install Python3+ and PIP for your system, visit `the Python Website <https://www.python.org/downloads/>`_.

Once Python is installed, the library can be installed or updated by running::

	pip install --upgrade tbapi

The library can then be easily imported and used within your projects.

*****
Usage
*****

The TBApi Library can be imported simply by calling::

  import tbapi

From there, you must create a :class:`Parser` object that allows you to interact with The Blue Alliance's API servers.  You can generate an API key by visiting `TBA Account Settings <https://www.thebluealliance.com/account>`_.
::

  parser = tbapi.Parser(api_key)


This :class:`Parser` object can then be used to gather data from The Blue Alliance API.  :class:`Parser` methods are available for every API call and can be found below.

******
Parser
******

.. autoclass:: Parser
  :members:

************
Data Classes
************

Individual Data Classes that represent certain types of data.

=========
Data List
=========

A modified List including filter support and access to the raw JSON arrays represented.

.. autoclass:: DataList
  :members:

====
Data
====

.. autoclass:: Data
  :members:

======
Status
======

.. autoclass:: Status
  :members:

===
App
===

.. autoclass:: App
  :members:

====
Team
====

.. autoclass:: Team
  :members:

========
District
========

.. autoclass:: District
  :members:

=====
Robot
=====

.. autoclass:: Robot
  :members:

======
Social
======

.. autoclass:: Social
  :members:

=====
Event
=====

.. autoclass:: Event
  :members:

============
Event Status
============

.. autoclass:: EventStatus
  :members:

**********
Exceptions
**********

.. autoclass:: EmptyError

.. autoclass:: ParseError

.. autoclass:: KeyInputError

.. autoclass:: OfflineError

.. autoclass:: FluidKeyError
