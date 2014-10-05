import json
import random
import re

from memoize import Memoizer
from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings
import requests

import settings


EMOTICONS_URL = "https://%(server)s/v2/emoticon?max-results=1000&auth_token=%(token)s"

store = {}
memo = Memoizer(store)

class HipchatEmoticonsMixin(object):

    @memo(max_age=12*60*60)
    def get_emoticon_list(self):
        """
        Fetch the list of emoticons from hipchat
        """
        url = EMOTICONS_URL % {
            "server": settings.HIPCHAT_SERVER,
            "token": settings.V2_TOKEN
        }
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        response = requests.get(url, headers=headers)
        data = response.json()
        return data['items']

    def find_emoticons(self, search=None):
        """
        Find emoticons based on the given search string
        """
        emoticons = self.get_emoticon_list() or []
        if search:
            search = search.strip()
            if search:
                search = '.*%s.*' % search
                emoticons = filter(
                    lambda e: re.match(search, e['shortcut']),
                    emoticons,
                )
        return map(
            lambda e: '(%s)' % e['shortcut'],
            emoticons,
        )


class EmoticonPlugin(WillPlugin, HipchatEmoticonsMixin):

    @respond_to("^emoticon me(?P<search>.*?)$")
    def emoticon_me(self, message, search=None):
        "emoticon me ___: Search hipchat emoticons for ___ and return a random one"
        emoticons = self.find_emoticons(search)
        if emoticons:
            self.reply(message, random.choice(emoticons))
        else:
            self.reply(message, 'I cannae find any captain!')

    @respond_to("^emoticons me(?P<search>.*?)$")
    def emoticons_me(self, message, search=None):
        "emoticons me ___: Search hipchat emoticons for ___ and return all of them"
        emoticons = self.find_emoticons(search)
        if emoticons:
            self.reply(message, ','.join(emoticons))
        else:
            self.reply(message, 'I cannae find any captain!')
