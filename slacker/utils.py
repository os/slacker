#!/usr/bin/python
# -*- coding: utf-8 -*-

from slacker import Slacker

def get_channel_id(token, channel_name):

    slack = Slacker(token)
    channels = slack.channels.list().body['channels']

    for channel in channels:
        name, channel_id = channel['name'], channel['id']
        if name == channel_name:
            return channel_id
