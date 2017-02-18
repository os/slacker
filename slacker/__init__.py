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

from slacker.utils import get_item_id_by_name


API_BASE_URL = 'https://slack.com/api/{api}'
DEFAULT_TIMEOUT = 10


__all__ = ['Error', 'Response', 'BaseAPI', 'API', 'Auth', 'Users', 'Groups',
           'Channels', 'Chat', 'IM', 'IncomingWebhook', 'Search', 'Files',
           'Stars', 'Emoji', 'Presence', 'RTM', 'Team', 'Reactions', 'Pins',
           'UserGroups', 'UserGroupsUsers', 'MPIM', 'OAuth', 'DND', 'Bots',
           'FilesComments', 'Reminders', 'TeamProfile', 'UsersProfile',
           'IDPGroups', 'Slacker']


class Error(Exception):
    pass


class Response(object):
    def __init__(self, body):
        self.raw = body
        self.body = json.loads(body)
        self.successful = self.body['ok']
        self.error = self.body.get('error')


class BaseAPI(object):
    def __init__(self, token=None, timeout=DEFAULT_TIMEOUT):
        self.token = token
        self.timeout = timeout

    def _request(self, method, api, **kwargs):
        if self.token:
            kwargs.setdefault('params', {})['token'] = self.token

        response = method(API_BASE_URL.format(api=api),
                          timeout=self.timeout,
                          **kwargs)

        response.raise_for_status()

        response = Response(response.text)
        if not response.successful:
            raise Error(response.error)

        return response

    def get(self, api, **kwargs):
        return self._request(requests.get, api, **kwargs)

    def post(self, api, **kwargs):
        return self._request(requests.post, api, **kwargs)


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


class Users(BaseAPI):
    def __init__(self, *args, **kwargs):
        super(Users, self).__init__(*args, **kwargs)
        self._profile = UsersProfile(*args, **kwargs)

    @property
    def profile(self):
        return self._profile

    def info(self, user):
        return self.get('users.info', params={'user': user})

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

    def list(self, exclude_archived=None):
        return self.get('channels.list',
                        params={'exclude_archived': exclude_archived})

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
                     icon_emoji=None):

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
                             'icon_emoji': icon_emoji
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
        if attachments and isinstance(attachments, list):
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
                            'unreads' : int(unreads)
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

    def delete(self, file_, id):
        return self.post('files.comments.delete',
                         data={'file': file_, 'id': id})

    def edit(self, file_, id, comment):
        return self.post('files.comments.edit',
                         data={'file': file_, 'id': id, 'comment': comment})


class Files(BaseAPI):
    def __init__(self, *args, **kwargs):
        super(Files, self).__init__(*args, **kwargs)
        self._comments = FilesComments(*args, **kwargs)

    @property
    def comments(self):
        return self._comments

    def list(self, user=None, ts_from=None, ts_to=None, types=None,
             count=None, page=None):
        return self.get('files.list',
                        params={
                            'user': user,
                            'ts_from': ts_from,
                            'ts_to': ts_to,
                            'types': types,
                            'count': count,
                            'page': page
                        })

    def info(self, file_, count=None, page=None):
        return self.get('files.info',
                        params={'file': file_, 'count': count, 'page': page})

    def upload(self, file_=None, content=None, filetype=None, filename=None,
               title=None, initial_comment=None, channels=None):
        if isinstance(channels, (tuple, list)):
            channels = ','.join(channels)

        data = {
            'content': content,
            'filetype': filetype,
            'filename': filename,
            'title': title,
            'initial_comment': initial_comment,
            'channels': channels
        }

        if file_:
            with open(file_, 'rb') as f:
                return self.post('files.upload', data=data, files={'file': f})
        else:
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

    def remove(self, file_=None, file_comment=None, channel=None, timestamp=None):
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

    def access_logs(self, count=None, page=None):
        return self.get('team.accessLogs',
                        params={'count': count, 'page': page})

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

    def list(self, include_disabled=None, include_count=None, include_users=None):
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


class IncomingWebhook(object):
    def __init__(self, url=None, timeout=DEFAULT_TIMEOUT):
        self.url = url
        self.timeout = timeout

    def post(self, data):
        """
        Posts message with payload formatted in accordance with
        this documentation https://api.slack.com/incoming-webhooks
        """
        if not self.url:
            raise Error('URL for incoming webhook is undefined')

        return requests.post(self.url, data=json.dumps(data),
                             timeout=self.timeout)


class Slacker(object):
    oauth = OAuth(timeout=DEFAULT_TIMEOUT)

    def __init__(self, token, incoming_webhook_url=None,
                 timeout=DEFAULT_TIMEOUT):
        self.im = IM(token=token, timeout=timeout)
        self.api = API(token=token, timeout=timeout)
        self.dnd = DND(token=token, timeout=timeout)
        self.rtm = RTM(token=token, timeout=timeout)
        self.auth = Auth(token=token, timeout=timeout)
        self.bots = Bots(token=token, timeout=timeout)
        self.chat = Chat(token=token, timeout=timeout)
        self.team = Team(token=token, timeout=timeout)
        self.pins = Pins(token=token, timeout=timeout)
        self.mpim = MPIM(token=token, timeout=timeout)
        self.users = Users(token=token, timeout=timeout)
        self.files = Files(token=token, timeout=timeout)
        self.stars = Stars(token=token, timeout=timeout)
        self.emoji = Emoji(token=token, timeout=timeout)
        self.search = Search(token=token, timeout=timeout)
        self.groups = Groups(token=token, timeout=timeout)
        self.channels = Channels(token=token, timeout=timeout)
        self.presence = Presence(token=token, timeout=timeout)
        self.reminders = Reminders(token=token, timeout=timeout)
        self.reactions = Reactions(token=token, timeout=timeout)
        self.idpgroups = IDPGroups(token=token, timeout=timeout)
        self.usergroups = UserGroups(token=token, timeout=timeout)
        self.incomingwebhook = IncomingWebhook(url=incoming_webhook_url,
                                               timeout=timeout)
