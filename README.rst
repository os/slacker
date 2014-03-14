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
    slack.chat.post_message('#general', 'Hello fellow slackers!')

Installation
============
.. code-block:: bash

    $ pip install git+git://github.com/os/slacker.git

Documentation
=============
https://api.slack.com/
