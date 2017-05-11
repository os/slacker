#!/usr/bin/env python
"""Post slack message."""

# https://github.com/os/slacker
# https://api.slack.com/methods

import os
from slacker import Slacker


def post_slack():
    """Post slack message."""
    try:
        token = os.environ['SLACK_TOKEN']
        slack = Slacker(token)

        obj = slack.chat.post_message(
            channel='#general',
            text='',
            as_user=True,
            attachments=[{"pretext": "Subject",
                          "text": "Body"}])
        print obj.successful, obj.__dict__['body']['channel'], obj.__dict__[
            'body']['ts']
    except KeyError, ex:
        print 'Environment variable %s not set.' % str(ex)


if __name__ == '__main__':
    post_slack()
