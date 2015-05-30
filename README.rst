=======
Slacker
=======

|pypi|_
|build status|_
|code quality|_
|pypi downloads|_

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


.. |build status| image:: https://img.shields.io/travis/os/slacker.svg
.. _build status: http://travis-ci.org/os/slacker
.. |pypi| image:: https://img.shields.io/pypi/v/Slacker.svg
.. _pypi: https://pypi.python.org/pypi/slacker/
.. |code quality| image:: https://scrutinizer-ci.com/g/os/slacker/badges/quality-score.png?b=master
.. _code quality: https://scrutinizer-ci.com/g/os/slacker/
.. |pypi downloads| image:: https://img.shields.io/pypi/dm/Slacker.svg
.. _pypi downloads: https://pypi.python.org/pypi/slacker/

