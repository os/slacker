#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest
from mock import patch

from slacker.utils import get_channel_id

class TestUtils(unittest.TestCase):

    @patch('slacker.utils.Slacker')
    def test_get_channel_id(self, mock_slacker):

        mock_slacker.return_value.channels.list.return_value.body = {
            'channels': [
                {'name': 'general', 'id': 'C111'},
                {'name': 'random', 'id': 'C222'}
            ]
        }

        self.assertEqual(
            'C111', get_channel_id('aaa', 'general')
        )

    @patch('slacker.utils.Slacker')
    def test_get_channel_id_without_channel(self, mock_slacker):

        mock_slacker.return_value.channels.list.return_value.body = {
            'channels': [
                {'name': 'general', 'id': 'C111'},
                {'name': 'random', 'id': 'C222'}
            ]
        }

        self.assertEqual(
            None, get_channel_id('aaa', 'fake_group')
        )
