#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import unittest

from mock import patch, Mock

from slacker import Channels


class TestUtils(unittest.TestCase):
    @patch('slacker.requests')
    def test_get_channel_id(self, mock_requests):
        text = {
            'ok': 'true',
            'channels': [
                {'name': 'general', 'id': 'C111'},
                {'name': 'random', 'id': 'C222'}
            ]
        }
        json_to_text = json.dumps(text)

        mock_requests.get.return_value = Mock(
            status_code=200, text=json_to_text,
        )

        channels = Channels(token='aaa')

        self.assertEqual(
            'C111', channels.get_channel_id('general')
        )

    @patch('slacker.requests')
    def test_get_channel_id_without_channel(self, mock_requests):
        text = {
            'ok': 'true',
            'channels': [
                {'name': 'general', 'id': 'C111'},
                {'name': 'random', 'id': 'C222'}
            ]
        }
        json_to_text = json.dumps(text)

        mock_requests.get.return_value = Mock(
            status_code=200, text=json_to_text,
        )

        channels = Channels(token='aaa')

        self.assertEqual(
            None, channels.get_channel_id('fake_group')
        )
