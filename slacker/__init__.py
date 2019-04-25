# Copyright 2015 Oktay Sancak
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

import requests

import time

from slacker.utilities import (
    get_api_url,
    get_item_id_by_name,
)


__version__ = '0.13.0'

DEFAULT_TIMEOUT = 10
DEFAULT_RETRIES = 0
# seconds to wait after a 429 error if Slack's API doesn't provide one
DEFAULT_WAIT = 20

__all__ = ['Error', 'Response', 'BaseAPI', 'API', 'Auth', 'Users', 'Groups',
           'Channels', 'Chat', 'IM', 'IncomingWebhook', 'Search', 'Files',
           'Stars', 'Emoji', 'Presence', 'RTM', 'Team', 'Reactions', 'Pins',
           'UserGroups', 'UserGroupsUsers', 'MPIM', 'OAuth', 'DND', 'Bots',
           'FilesComments', 'Reminders', 'TeamProfile', 'UsersProfile',
           'IDPGroups', 'Apps', 'AppsPermissions', 'Slacker', 'Dialog',
           'Conversations', 'Migration']


class Error(Exception):
    pass


class Response(object):
    def __init__(self, body):
        self.raw = body
        self.body = json.loads(body)
        self.successful = self.body['ok']
        self.error = self.body.get('error')

    def __str__(self):
        return json.dumps(self.body)


class BaseAPI(object):
    def __init__(self, token=None, timeout=DEFAULT_TIMEOUT, proxies=None,
                 session=None, rate_limit_retries=DEFAULT_RETRIES):
        self.token = token
        self.timeout = timeout
        self.proxies = proxies
        self.session = session
        self.rate_limit_retries = rate_limit_retries

    def _request(self, request_method, method, **kwargs):
        if self.token:
            kwargs.setdefault('params', {})['token'] = self.token

        url = get_api_url(method)

        # while we have rate limit retries left, fetch the resource and back
        # off as Slack's HTTP response suggests
        for retry_num in range(self.rate_limit_retries):
            response = request_method(
                url, timeout=self.timeout, proxies=self.proxies, **kwargs
            )

            if response.status_code == requests.codes.ok:
                break

            # handle HTTP 429 as documented at
            # https://api.slack.com/docs/rate-limits
            if response.status_code == requests.codes.too_many:
                time.sleep(int(
                    response.headers.get('retry-after', DEFAULT_WAIT)
                ))
                continue

            response.raise_for_status()
        else:
            # with no retries left, make one final attempt to fetch the
            # resource, but do not handle too_many status differently
            response = request_method(
                url, timeout=self.timeout, proxies=self.proxies, **kwargs
            )
            response.raise_for_status()

        response = Response(response.text)
        if not response.successful:
            raise Error(response.error)

        return response

    def _session_get(self, url, params=None, **kwargs):
        kwargs.setdefault('allow_redirects', True)
        return self.session.request(
            method='get', url=url, params=params, **kwargs
        )

    def _session_post(self, url, data=None, **kwargs):
        return self.session.request(
            method='post', url=url, data=data, **kwargs
        )

    def get(self, api, **kwargs):
        return self._request(
            self._session_get if self.session else requests.get,
            api, **kwargs
        )

    def post(self, api, **kwargs):
        return self._request(
            self._session_post if self.session else requests.post,
            api, **kwargs
        )


class API(BaseAPI):
    def test(self, error=None, **kwargs):
        if error:
            kwargs['error'] = error

        return self.get('api.test', params=kwargs)


class Auth(BaseAPI):
    def test(self):
        return self.get('auth.test')

    def revoke(self, test=True):
        return self.post('auth.revoke', data={'test': int(test)})


class Conversations(BaseAPI):
    def archive(self, channel):
        return self.post('conversations.archive', data={'channel': channel})

    def close(self, channel):
        return self.post('conversations.close', data={'channel': channel})

    def create(self, name, user_ids=None, is_private=None):
        if isinstance(user_ids, (list, tuple)):
            user_ids = ','.join(user_ids)

        return self.post(
            'conversations.create',
            data={'name': name, 'user_ids': user_ids, 'is_private': is_private}
        )

    def history(self, channel, cursor=None, inclusive=None, latest=None,
                oldest=None, limit=None):
        return self.get(
            'conversations.history',
            params={
                'channel': channel,
                'cursor': cursor,
                'inclusive': inclusive,
                'latest': latest,
                'oldest': oldest,
                'limit': limit
            }
        )

    def info(self, channel, include_locale=None, include_num_members=None):
        return self.get(
            'conversations.info',
            params={
                'channel': channel,
                'include_locale': include_locale,
                'include_num_members': include_num_members
            }
        )

    def invite(self, channel, users):
        if isinstance(users, (list, tuple)):
            users = ','.join(users)

        return self.post(
            'conversations.invite',
            data={'channel': channel, 'users': users}
        )

    def join(self, channel):
        return self.post('conversations.join', data={'channel': channel})

    def kick(self, channel, user):
        return self.post(
            'conversations.kick',
            data={'channel': channel, 'user': user}
        )

    def leave(self, channel):
        return self.post('conversations.leave', data={'channel': channel})

    def list(self, cursor=None, exclude_archived=None, types=None, limit=None):
        if isinstance(types, (list, tuple)):
            types = ','.join(types)

        return self.get(
            'conversations.list',
            params={
                'cursor': cursor,
                'exclude_archived': exclude_archived,
                'types': types,
                'limit': limit
            }
        )

    def members(self, channel, cursor=None, limit=None):
        return self.get(
            'conversations.members',
            params={'channel': channel, 'cursor': cursor, 'limit': limit}
        )

    def open(self, channel=None, users=None, return_im=None):
        if isinstance(users, (list, tuple)):
            users = ','.join(users)

        return self.post(
            'conversations.open',
            data={'channel': channel, 'users': users, 'return_im': return_im}
        )

    def rename(self, channel, name):
        return self.post(
            'conversations.rename',
            data={'channel': channel, 'name': name}
        )

    def replies(self, channel, ts, cursor=None, inclusive=None, latest=None,
                oldest=None, limit=None):
        return self.get(
            'conversations.replies',
            params={
                'channel': channel,
                'ts': ts,
                'cursor': cursor,
                'inclusive': inclusive,
                'latest': latest,
                'oldest': oldest,
                'limit': limit
            }
        )

    def set_purpose(self, channel, purpose):
        return self.post(
            'conversations.setPurpose',
            data={'channel': channel, 'purpose': purpose}
        )

    def set_topic(self, channel, topic):
        return self.post(
            'conversations.setTopic',
            data={'channel': channel, 'topic': topic}
        )

    def unarchive(self, channel):
        return self.post('conversations.unarchive', data={'channel': channel})


class Dialog(BaseAPI):
    def open(self, dialog, trigger_id):
        return self.post('dialog.open',
                         data={
                             'dialog': json.dumps(dialog),
                             'trigger_id': trigger_id,
                         })


class UsersProfile(BaseAPI):
    def get(self, user=None, include_labels=False):
        return super(UsersProfile, self).get(
            'users.profile.get',
            params={'user': user, 'include_labels': int(include_labels)}
        )

    def set(self, user=None, profile=None, name=None, value=None):
        return self.post('users.profile.set',
                         data={
                             'user': user,
                             'profile': profile,
                             'name': name,
                             'value': value
                         })


class UsersAdmin(BaseAPI):
    def invite(self, email, channels=None, first_name=None,
               last_name=None, resend=True):
        return self.post('users.admin.invite',
                         params={
                             'email': email,
                             'channels': channels,
                             'first_name': first_name,
                             'last_name': last_name,
                             'resend': resend
                         })


class Users(BaseAPI):
    def __init__(self, *args, **kwargs):
        super(Users, self).__init__(*args, **kwargs)
        self._profile = UsersProfile(*args, **kwargs)
        self._admin = UsersAdmin(*args, **kwargs)

    @property
    def profile(self):
        return self._profile

    @property
    def admin(self):
        return self._admin

    def info(self, user, include_locale=False):
        return self.get('users.info',
                        params={'user': user, 'include_locale': include_locale})

    def list(self, presence=False):
        return self.get('users.list', params={'presence': int(presence)})

    def identity(self):
        return self.get('users.identity')

    def set_active(self):
        return self.post('users.setActive')

    def get_presence(self, user):
        return self.get('users.getPresence', params={'user': user})

    def set_presence(self, presence):
        return self.post('users.setPresence', data={'presence': presence})

    def get_user_id(self, user_name):
        members = self.list().body['members']
        return get_item_id_by_name(members, user_name)


class Groups(BaseAPI):
    def create(self, name):
        return self.post('groups.create', data={'name': name})

    def create_child(self, channel):
        return self.post('groups.createChild', data={'channel': channel})

    def info(self, channel):
        return self.get('groups.info', params={'channel': channel})

    def list(self, exclude_archived=None):
        return self.get('groups.list',
                        params={'exclude_archived': exclude_archived})

    def history(self, channel, latest=None, oldest=None, count=None,
                inclusive=None):
        return self.get('groups.history',
                        params={
                            'channel': channel,
                            'latest': latest,
                            'oldest': oldest,
                            'count': count,
                            'inclusive': inclusive
                        })

    def invite(self, channel, user):
        return self.post('groups.invite',
                         data={'channel': channel, 'user': user})

    def kick(self, channel, user):
        return self.post('groups.kick',
                         data={'channel': channel, 'user': user})

    def leave(self, channel):
        return self.post('groups.leave', data={'channel': channel})

    def mark(self, channel, ts):
        return self.post('groups.mark', data={'channel': channel, 'ts': ts})

    def rename(self, channel, name):
        return self.post('groups.rename',
                         data={'channel': channel, 'name': name})

    def replies(self, channel, thread_ts):
        return self.get('groups.replies',
                        params={'channel': channel, 'thread_ts': thread_ts})

    def archive(self, channel):
        return self.post('groups.archive', data={'channel': channel})

    def unarchive(self, channel):
        return self.post('groups.unarchive', data={'channel': channel})

    def open(self, channel):
        return self.post('groups.open', data={'channel': channel})

    def close(self, channel):
        return self.post('groups.close', data={'channel': channel})

    def set_purpose(self, channel, purpose):
        return self.post('groups.setPurpose',
                         data={'channel': channel, 'purpose': purpose})

    def set_topic(self, channel, topic):
        return self.post('groups.setTopic',
                         data={'channel': channel, 'topic': topic})


class Channels(BaseAPI):
    def create(self, name):
        return self.post('channels.create', data={'name': name})

    def info(self, channel):
        return self.get('channels.info', params={'channel': channel})

    def list(self, exclude_archived=None, exclude_members=None):
        return self.get('channels.list',
                        params={'exclude_archived': exclude_archived,
                                'exclude_members': exclude_members})

    def history(self, channel, latest=None, oldest=None, count=None,
                inclusive=False, unreads=False):
        return self.get('channels.history',
                        params={
                            'channel': channel,
                            'latest': latest,
                            'oldest': oldest,
                            'count': count,
                            'inclusive': int(inclusive),
                            'unreads': int(unreads)
                        })

    def mark(self, channel, ts):
        return self.post('channels.mark',
                         data={'channel': channel, 'ts': ts})

    def join(self, name):
        return self.post('channels.join', data={'name': name})

    def leave(self, channel):
        return self.post('channels.leave', data={'channel': channel})

    def invite(self, channel, user):
        return self.post('channels.invite',
                         data={'channel': channel, 'user': user})

    def kick(self, channel, user):
        return self.post('channels.kick',
                         data={'channel': channel, 'user': user})

    def rename(self, channel, name):
        return self.post('channels.rename',
                         data={'channel': channel, 'name': name})

    def replies(self, channel, thread_ts):
        return self.get('channels.replies',
                        params={'channel': channel, 'thread_ts': thread_ts})

    def archive(self, channel):
        return self.post('channels.archive', data={'channel': channel})

    def unarchive(self, channel):
        return self.post('channels.unarchive', data={'channel': channel})

    def set_purpose(self, channel, purpose):
        return self.post('channels.setPurpose',
                         data={'channel': channel, 'purpose': purpose})

    def set_topic(self, channel, topic):
        return self.post('channels.setTopic',
                         data={'channel': channel, 'topic': topic})

    def get_channel_id(self, channel_name):
        channels = self.list().body['channels']
        return get_item_id_by_name(channels, channel_name)


class Chat(BaseAPI):
    def post_message(self, channel, text=None, username=None, as_user=None,
                     parse=None, link_names=None, attachments=None,
                     unfurl_links=None, unfurl_media=None, icon_url=None,
                     icon_emoji=None, thread_ts=None, reply_broadcast=None):

        # Ensure attachments are json encoded
        if attachments:
            if isinstance(attachments, list):
                attachments = json.dumps(attachments)

        return self.post('chat.postMessage',
                         data={
                             'channel': channel,
                             'text': text,
                             'username': username,
                             'as_user': as_user,
                             'parse': parse,
                             'link_names': link_names,
                             'attachments': attachments,
                             'unfurl_links': unfurl_links,
                             'unfurl_media': unfurl_media,
                             'icon_url': icon_url,
                             'icon_emoji': icon_emoji,
                             'thread_ts': thread_ts,
                             'reply_broadcast': reply_broadcast
                         })

    def me_message(self, channel, text):
        return self.post('chat.meMessage',
                         data={'channel': channel, 'text': text})

    def command(self, channel, command, text):
        return self.post('chat.command',
                         data={
                             'channel': channel,
                             'command': command,
                             'text': text
                         })

    def update(self, channel, ts, text, attachments=None, parse=None,
               link_names=False, as_user=None):
        # Ensure attachments are json encoded
        if attachments is not None and isinstance(attachments, list):
            attachments = json.dumps(attachments)
        return self.post('chat.update',
                         data={
                             'channel': channel,
                             'ts': ts,
                             'text': text,
                             'attachments': attachments,
                             'parse': parse,
                             'link_names': int(link_names),
                             'as_user': as_user,
                         })

    def delete(self, channel, ts, as_user=False):
        return self.post('chat.delete',
                         data={
                             'channel': channel,
                             'ts': ts,
                             'as_user': as_user
                         })

    def post_ephemeral(self, channel, text, user, as_user=None,
                       attachments=None, link_names=None, parse=None):
        # Ensure attachments are json encoded
        if attachments is not None and isinstance(attachments, list):
            attachments = json.dumps(attachments)
        return self.post('chat.postEphemeral',
                         data={
                             'channel': channel,
                             'text': text,
                             'user': user,
                             'as_user': as_user,
                             'attachments': attachments,
                             'link_names': link_names,
                             'parse': parse,
                         })

    def unfurl(self, channel, ts, unfurls, user_auth_message=None,
               user_auth_required=False, user_auth_url=None):
        return self.post('chat.unfurl',
                         data={
                             'channel': channel,
                             'ts': ts,
                             'unfurls': unfurls,
                             'user_auth_message': user_auth_message,
                             'user_auth_required': user_auth_required,
                             'user_auth_url': user_auth_url,
                         })

    def get_permalink(self, channel, message_ts):
        return self.get('chat.getPermalink',
                        params={
                            'channel': channel,
                            'message_ts': message_ts
                        })


class IM(BaseAPI):
    def list(self):
        return self.get('im.list')

    def history(self, channel, latest=None, oldest=None, count=None,
                inclusive=None, unreads=False):
        return self.get('im.history',
                        params={
                            'channel': channel,
                            'latest': latest,
                            'oldest': oldest,
                            'count': count,
                            'inclusive': inclusive,
                            'unreads': int(unreads)
                        })

    def replies(self, channel, thread_ts):
        return self.get('im.replies',
                        params={'channel': channel, 'thread_ts': thread_ts})

    def mark(self, channel, ts):
        return self.post('im.mark', data={'channel': channel, 'ts': ts})

    def open(self, user):
        return self.post('im.open', data={'user': user})

    def close(self, channel):
        return self.post('im.close', data={'channel': channel})


class MPIM(BaseAPI):
    def open(self, users):
        if isinstance(users, (tuple, list)):
            users = ','.join(users)

        return self.post('mpim.open', data={'users': users})

    def close(self, channel):
        return self.post('mpim.close', data={'channel': channel})

    def mark(self, channel, ts):
        return self.post('mpim.mark', data={'channel': channel, 'ts': ts})

    def list(self):
        return self.get('mpim.list')

    def history(self, channel, latest=None, oldest=None, inclusive=False,
                count=None, unreads=False):
        return self.get('mpim.history',
                        params={
                            'channel': channel,
                            'latest': latest,
                            'oldest': oldest,
                            'inclusive': int(inclusive),
                            'count': count,
                            'unreads': int(unreads)
                        })

    def replies(self, channel, thread_ts):
        return self.get('mpim.replies',
                        params={'channel': channel, 'thread_ts': thread_ts})


class Search(BaseAPI):
    def all(self, query, sort=None, sort_dir=None, highlight=None, count=None,
            page=None):
        return self.get('search.all',
                        params={
                            'query': query,
                            'sort': sort,
                            'sort_dir': sort_dir,
                            'highlight': highlight,
                            'count': count,
                            'page': page
                        })

    def files(self, query, sort=None, sort_dir=None, highlight=None,
              count=None, page=None):
        return self.get('search.files',
                        params={
                            'query': query,
                            'sort': sort,
                            'sort_dir': sort_dir,
                            'highlight': highlight,
                            'count': count,
                            'page': page
                        })

    def messages(self, query, sort=None, sort_dir=None, highlight=None,
                 count=None, page=None):
        return self.get('search.messages',
                        params={
                            'query': query,
                            'sort': sort,
                            'sort_dir': sort_dir,
                            'highlight': highlight,
                            'count': count,
                            'page': page
                        })


class FilesComments(BaseAPI):
    def add(self, file_, comment):
        return self.post('files.comments.add',
                         data={'file': file_, 'comment': comment})

    def delete(self, file_, id_):
        return self.post('files.comments.delete',
                         data={'file': file_, 'id': id_})

    def edit(self, file_, id_, comment):
        return self.post('files.comments.edit',
                         data={'file': file_, 'id': id_, 'comment': comment})


class Files(BaseAPI):
    def __init__(self, *args, **kwargs):
        super(Files, self).__init__(*args, **kwargs)
        self._comments = FilesComments(*args, **kwargs)

    @property
    def comments(self):
        return self._comments

    def list(self, user=None, ts_from=None, ts_to=None, types=None,
             count=None, page=None, channel=None):
        return self.get('files.list',
                        params={
                            'user': user,
                            'ts_from': ts_from,
                            'ts_to': ts_to,
                            'types': types,
                            'count': count,
                            'page': page,
                            'channel': channel
                        })

    def info(self, file_, count=None, page=None):
        return self.get('files.info',
                        params={'file': file_, 'count': count, 'page': page})

    def upload(self, file_=None, content=None, filetype=None, filename=None,
               title=None, initial_comment=None, channels=None, thread_ts=None):
        if isinstance(channels, (tuple, list)):
            channels = ','.join(channels)

        data = {
            'content': content,
            'filetype': filetype,
            'filename': filename,
            'title': title,
            'initial_comment': initial_comment,
            'channels': channels,
            'thread_ts': thread_ts
        }

        if file_:
            if isinstance(file_, str):
                with open(file_, 'rb') as f:
                    return self.post(
                        'files.upload', data=data, files={'file': f}
                    )

            return self.post(
                'files.upload', data=data, files={'file': file_}
            )

        return self.post('files.upload', data=data)

    def delete(self, file_):
        return self.post('files.delete', data={'file': file_})

    def revoke_public_url(self, file_):
        return self.post('files.revokePublicURL', data={'file': file_})

    def shared_public_url(self, file_):
        return self.post('files.sharedPublicURL', data={'file': file_})


class Stars(BaseAPI):
    def add(self, file_=None, file_comment=None, channel=None, timestamp=None):
        assert file_ or file_comment or channel

        return self.post('stars.add',
                         data={
                             'file': file_,
                             'file_comment': file_comment,
                             'channel': channel,
                             'timestamp': timestamp
                         })

    def list(self, user=None, count=None, page=None):
        return self.get('stars.list',
                        params={'user': user, 'count': count, 'page': page})

    def remove(self, file_=None, file_comment=None, channel=None,
               timestamp=None):
        assert file_ or file_comment or channel

        return self.post('stars.remove',
                         data={
                             'file': file_,
                             'file_comment': file_comment,
                             'channel': channel,
                             'timestamp': timestamp
                         })


class Emoji(BaseAPI):
    def list(self):
        return self.get('emoji.list')


class Presence(BaseAPI):
    AWAY = 'away'
    ACTIVE = 'active'
    TYPES = (AWAY, ACTIVE)

    def set(self, presence):
        assert presence in Presence.TYPES, 'Invalid presence type'
        return self.post('presence.set', data={'presence': presence})


class RTM(BaseAPI):
    def start(self, simple_latest=False, no_unreads=False, mpim_aware=False):
        return self.get('rtm.start',
                        params={
                            'simple_latest': int(simple_latest),
                            'no_unreads': int(no_unreads),
                            'mpim_aware': int(mpim_aware),
                        })

    def connect(self):
        return self.get('rtm.connect')


class TeamProfile(BaseAPI):
    def get(self, visibility=None):
        return super(TeamProfile, self).get(
            'team.profile.get',
            params={'visibility': visibility}
        )


class Team(BaseAPI):
    def __init__(self, *args, **kwargs):
        super(Team, self).__init__(*args, **kwargs)
        self._profile = TeamProfile(*args, **kwargs)

    @property
    def profile(self):
        return self._profile

    def info(self):
        return self.get('team.info')

    def access_logs(self, count=None, page=None, before=None):
        return self.get('team.accessLogs',
                        params={
                            'count': count,
                            'page': page,
                            'before': before
                        })

    def integration_logs(self, service_id=None, app_id=None, user=None,
                         change_type=None, count=None, page=None):
        return self.get('team.integrationLogs',
                        params={
                            'service_id': service_id,
                            'app_id': app_id,
                            'user': user,
                            'change_type': change_type,
                            'count': count,
                            'page': page,
                        })

    def billable_info(self, user=None):
        return self.get('team.billableInfo', params={'user': user})


class Reactions(BaseAPI):
    def add(self, name, file_=None, file_comment=None, channel=None,
            timestamp=None):
        # One of file, file_comment, or the combination of channel and timestamp
        # must be specified
        assert (file_ or file_comment) or (channel and timestamp)

        return self.post('reactions.add',
                         data={
                             'name': name,
                             'file': file_,
                             'file_comment': file_comment,
                             'channel': channel,
                             'timestamp': timestamp,
                         })

    def get(self, file_=None, file_comment=None, channel=None, timestamp=None,
            full=None):
        return super(Reactions, self).get('reactions.get',
                                          params={
                                              'file': file_,
                                              'file_comment': file_comment,
                                              'channel': channel,
                                              'timestamp': timestamp,
                                              'full': full,
                                          })

    def list(self, user=None, full=None, count=None, page=None):
        return super(Reactions, self).get('reactions.list',
                                          params={
                                              'user': user,
                                              'full': full,
                                              'count': count,
                                              'page': page,
                                          })

    def remove(self, name, file_=None, file_comment=None, channel=None,
               timestamp=None):
        # One of file, file_comment, or the combination of channel and timestamp
        # must be specified
        assert (file_ or file_comment) or (channel and timestamp)

        return self.post('reactions.remove',
                         data={
                             'name': name,
                             'file': file_,
                             'file_comment': file_comment,
                             'channel': channel,
                             'timestamp': timestamp,
                         })


class Pins(BaseAPI):
    def add(self, channel, file_=None, file_comment=None, timestamp=None):
        # One of file, file_comment, or timestamp must also be specified
        assert file_ or file_comment or timestamp

        return self.post('pins.add',
                         data={
                             'channel': channel,
                             'file': file_,
                             'file_comment': file_comment,
                             'timestamp': timestamp,
                         })

    def remove(self, channel, file_=None, file_comment=None, timestamp=None):
        # One of file, file_comment, or timestamp must also be specified
        assert file_ or file_comment or timestamp

        return self.post('pins.remove',
                         data={
                             'channel': channel,
                             'file': file_,
                             'file_comment': file_comment,
                             'timestamp': timestamp,
                         })

    def list(self, channel):
        return self.get('pins.list', params={'channel': channel})


class UserGroupsUsers(BaseAPI):
    def list(self, usergroup, include_disabled=None):
        if isinstance(include_disabled, bool):
            include_disabled = int(include_disabled)

        return self.get('usergroups.users.list', params={
            'usergroup': usergroup,
            'include_disabled': include_disabled,
        })

    def update(self, usergroup, users, include_count=None):
        if isinstance(users, (tuple, list)):
            users = ','.join(users)

        if isinstance(include_count, bool):
            include_count = int(include_count)

        return self.post('usergroups.users.update', data={
            'usergroup': usergroup,
            'users': users,
            'include_count': include_count,
        })


class UserGroups(BaseAPI):
    def __init__(self, *args, **kwargs):
        super(UserGroups, self).__init__(*args, **kwargs)
        self._users = UserGroupsUsers(*args, **kwargs)

    @property
    def users(self):
        return self._users

    def list(self, include_disabled=None, include_count=None,
             include_users=None):
        if isinstance(include_disabled, bool):
            include_disabled = int(include_disabled)

        if isinstance(include_count, bool):
            include_count = int(include_count)

        if isinstance(include_users, bool):
            include_users = int(include_users)

        return self.get('usergroups.list', params={
            'include_disabled': include_disabled,
            'include_count': include_count,
            'include_users': include_users,
        })

    def create(self, name, handle=None, description=None, channels=None,
               include_count=None):
        if isinstance(channels, (tuple, list)):
            channels = ','.join(channels)

        if isinstance(include_count, bool):
            include_count = int(include_count)

        return self.post('usergroups.create', data={
            'name': name,
            'handle': handle,
            'description': description,
            'channels': channels,
            'include_count': include_count,
        })

    def update(self, usergroup, name=None, handle=None, description=None,
               channels=None, include_count=None):
        if isinstance(channels, (tuple, list)):
            channels = ','.join(channels)

        if isinstance(include_count, bool):
            include_count = int(include_count)

        return self.post('usergroups.update', data={
            'usergroup': usergroup,
            'name': name,
            'handle': handle,
            'description': description,
            'channels': channels,
            'include_count': include_count,
        })

    def disable(self, usergroup, include_count=None):
        if isinstance(include_count, bool):
            include_count = int(include_count)

        return self.post('usergroups.disable', data={
            'usergroup': usergroup,
            'include_count': include_count,
        })

    def enable(self, usergroup, include_count=None):
        if isinstance(include_count, bool):
            include_count = int(include_count)

        return self.post('usergroups.enable', data={
            'usergroup': usergroup,
            'include_count': include_count,
        })


class DND(BaseAPI):
    def team_info(self, users=None):
        if isinstance(users, (tuple, list)):
            users = ','.join(users)

        return self.get('dnd.teamInfo', params={'users': users})

    def set_snooze(self, num_minutes):
        return self.post('dnd.setSnooze', data={'num_minutes': num_minutes})

    def info(self, user=None):
        return self.get('dnd.info', params={'user': user})

    def end_dnd(self):
        return self.post('dnd.endDnd')

    def end_snooze(self):
        return self.post('dnd.endSnooze')


class Migration(BaseAPI):
    def exchange(self, users, to_old=False):
        if isinstance(users, (list, tuple)):
            users = ','.join(users)

        return self.get(
            'migration.exchange', params={'users': users, 'to_old': to_old}
        )


class Reminders(BaseAPI):
    def add(self, text, time, user=None):
        return self.post('reminders.add', data={
            'text': text,
            'time': time,
            'user': user,
        })

    def complete(self, reminder):
        return self.post('reminders.complete', data={'reminder': reminder})

    def delete(self, reminder):
        return self.post('reminders.delete', data={'reminder': reminder})

    def info(self, reminder):
        return self.get('reminders.info', params={'reminder': reminder})

    def list(self):
        return self.get('reminders.list')


class Bots(BaseAPI):
    def info(self, bot=None):
        return self.get('bots.info', params={'bot': bot})


class IDPGroups(BaseAPI):
    def list(self, include_users=False):
        return self.get('idpgroups.list',
                        params={'include_users': int(include_users)})


class OAuth(BaseAPI):
    def access(self, client_id, client_secret, code, redirect_uri=None):
        return self.post('oauth.access',
                         data={
                             'client_id': client_id,
                             'client_secret': client_secret,
                             'code': code,
                             'redirect_uri': redirect_uri
                         })

    def token(self, client_id, client_secret, code, redirect_uri=None,
              single_channel=None):
        return self.post('oauth.token',
                         data={
                             'client_id': client_id,
                             'client_secret': client_secret,
                             'code': code,
                             'redirect_uri': redirect_uri,
                             'single_channel': single_channel,
                         })


class AppsPermissions(BaseAPI):
    def info(self):
        return self.get('apps.permissions.info')

    def request(self, scopes, trigger_id):
        return self.post('apps.permissions.request',
                         data={
                             scopes: ','.join(scopes),
                             trigger_id: trigger_id,
                         })


class Apps(BaseAPI):
    def __init__(self, *args, **kwargs):
        super(Apps, self).__init__(*args, **kwargs)
        self._permissions = AppsPermissions(*args, **kwargs)

    @property
    def permissions(self):
        return self._permissions

    def uninstall(self, client_id, client_secret):
        return self.get(
            'apps.uninstall',
            params={'client_id': client_id, 'client_secret': client_secret}
        )


class IncomingWebhook(object):
    def __init__(self, url=None, timeout=DEFAULT_TIMEOUT, proxies=None):
        self.url = url
        self.timeout = timeout
        self.proxies = proxies

    def post(self, data):
        """
        Posts message with payload formatted in accordance with
        this documentation https://api.slack.com/incoming-webhooks
        """
        if not self.url:
            raise Error('URL for incoming webhook is undefined')

        return requests.post(self.url, data=json.dumps(data),
                             timeout=self.timeout, proxies=self.proxies)


class Slacker(object):
    oauth = OAuth(timeout=DEFAULT_TIMEOUT)

    def __init__(self, token, incoming_webhook_url=None,
                 timeout=DEFAULT_TIMEOUT, http_proxy=None, https_proxy=None,
                 session=None, rate_limit_retries=DEFAULT_RETRIES):

        proxies = self.__create_proxies(http_proxy, https_proxy)
        api_args = {
            'token': token,
            'timeout': timeout,
            'proxies': proxies,
            'session': session,
            'rate_limit_retries': rate_limit_retries,
        }
        self.im = IM(**api_args)
        self.api = API(**api_args)
        self.dnd = DND(**api_args)
        self.rtm = RTM(**api_args)
        self.apps = Apps(**api_args)
        self.auth = Auth(**api_args)
        self.bots = Bots(**api_args)
        self.chat = Chat(**api_args)
        self.dialog = Dialog(**api_args)
        self.team = Team(**api_args)
        self.pins = Pins(**api_args)
        self.mpim = MPIM(**api_args)
        self.users = Users(**api_args)
        self.files = Files(**api_args)
        self.stars = Stars(**api_args)
        self.emoji = Emoji(**api_args)
        self.search = Search(**api_args)
        self.groups = Groups(**api_args)
        self.channels = Channels(**api_args)
        self.presence = Presence(**api_args)
        self.reminders = Reminders(**api_args)
        self.migration = Migration(**api_args)
        self.reactions = Reactions(**api_args)
        self.idpgroups = IDPGroups(**api_args)
        self.usergroups = UserGroups(**api_args)
        self.conversations = Conversations(**api_args)
        self.incomingwebhook = IncomingWebhook(url=incoming_webhook_url,
                                               timeout=timeout, proxies=proxies)

    def __create_proxies(self, http_proxy=None, https_proxy=None):
        proxies = dict()
        if http_proxy:
            proxies['http'] = http_proxy
        if https_proxy:
            proxies['https'] = https_proxy
        return proxies
