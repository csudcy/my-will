import json
import re

from memoize import Memoizer
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
