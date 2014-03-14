=======
Slacker
=======

About
=====
Slacker is a full-featured Python interface for the Slack API.

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
