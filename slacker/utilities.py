#!/usr/bin/python
# -*- coding: utf-8 -*-


def get_item_id_by_name(list_dict, key_name):
    for d in list_dict:
        if d['name'] == key_name:
            return d['id']
