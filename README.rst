=======
Slacker
=======

.. image:: https://raw.githubusercontent.com/os/slacker/master/static/slacker.jpg

About
=====
Slacker is a full-featured Python interface for the `Slack API 
<https://api.slack.com/>`_.

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
