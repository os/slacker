=======
Slacker
=======

.. image:: https://raw.githubusercontent.com/os/slacker/master/static/slacker.jpg

About
=====
Slacker is a full-featured Python interface for the `Slack API 
<https://api.slack.com/>`_.

Examples
========
.. code-block:: python

    from slacker import Slacker

    slack = Slacker('<your-slack-api-token-goes-here>')
    
    # Send a message to #general channel
    slack.chat.post_message('#general', 'Hello fellow slackers!')

    # Get users list
    response = slack.users.list()
    users = response.body['members']

    # Upload a file
    slack.files.upload('hello.txt')

Installation
============
.. code-block:: bash

    $ pip install slacker

Documentation
=============
https://api.slack.com/
