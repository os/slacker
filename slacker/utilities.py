def get_api_url(method):
    """
    Returns API URL for the given method.

    :param method: Method name
    :type method: str

    :returns: API URL for the given method
    :rtype: str
    """
    return 'https://slack.com/api/{}'.format(method)


def get_item_id_by_name(list_dict, key_name):
    for d in list_dict:
        if d['name'] == key_name:
            return d['id']
