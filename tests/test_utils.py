import unittest

from slacker.utils import get_item_id_by_name


class TestUtils(unittest.TestCase):

    def test_get_item_id_by_name(self):
        list_dict = [{'name': 'channel_name', 'id': '123'}, {}]

        self.assertEqual(
            '123', get_item_id_by_name(list_dict, 'channel_name')
        )
