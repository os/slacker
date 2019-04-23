#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest

import responses

from slacker import Channels
from slacker.utilities import get_api_url


class TestChannels(unittest.TestCase):
    @responses.activate
    def test_valid_ids_return_channel_id(self):
        response = {
            'ok': 'true',
            'channels': [
                {'name': 'general', 'id': 'C111'},
                {'name': 'random', 'id': 'C222'}
            ]
        }
        responses.add(
            responses.GET,
            get_api_url('channels.list'),
            json=response,
            status=200
        )
        channels = Channels(token='aaa')
        self.assertEqual(channels.get_channel_id('general'), 'C111')

    @responses.activate
    def test_invalid_channel_ids_return_none(self):
        response = {
            'ok': 'true',
            'channels': [
                {'name': 'general', 'id': 'C111'},
                {'name': 'random', 'id': 'C222'}
            ]
        }
        responses.add(
            responses.GET,
            get_api_url('channels.list'),
            json=response,
            status=200
        )
        channels = Channels(token='aaa')
        self.assertEqual(channels.get_channel_id('fake_group'), None)
