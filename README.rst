=======
slacker
=======

:Info: Slacker API for Python.
:Author: Oktay Sancak

Documentation: https://api.slack.com/

About
=====
Slacker is an Apache2 Licensed Slack API library, written in Python.

Dependencies
============
Requests_ >= version 2.2.1.

.. _Requests: http://python-requests.org/

Installation
============
.. code-block:: bash

    $ pip install git+git://github.com/os/slacker.git

Examples
========
.. code-block:: python

    from slacker import Slacker
    slack = Slacker('<your-slack-api-token-goes-here>')
    slack.chat.post_message('#general', 'Hello fellow slackers!')

Documentation
=============
https://api.slack.com/
