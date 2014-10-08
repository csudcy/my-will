import json
import re

from memoize import Memoizer
import requests


EMOTICONS_URL = "https://%(server)s/v2/emoticon?max-results=1000&auth_token=%(token)s"

store = {}
memo = Memoizer(store)

class HipchatEmoticons(object):
    def __init__(self, server, token):
        self.url = EMOTICONS_URL % {
            "server": server,
            "token": token
        }

    @memo(max_age=12*60*60)
    def get_emoticon_list(self):
        """
        Fetch the list of emoticons from hipchat
        """
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        response = requests.get(self.url, headers=headers)
        data = response.json()
        return data['items']

    def find(self, search=None):
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

if __name__ == '__main__':
    he = HipchatEmoticons(
        'api.hipchat.com',
        '<V2 API token goes here>'
    )
    print len(he.find())
    print len(he.find('ar'))
    print he.find('ar')
    print he.find('arya')
