import functools
import json
import random
import re
import traceback

from memoize import Memoizer
from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings


EMOTICONS_URL = "https://%(server)s/v2/emoticon?max-results=1000&auth_token=%(token)s"

store = {}
memo = Memoizer(store)

def error_logger(func):
    @functools.wraps(func)
    def _error_logger(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            logging.critical('Error in {func}: \n{tb}'.format(
                func=func,
                tb=traceback.format_exc(),
            ))


class HipchatMixin(WillPlugin):

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
        response = requests.get(url, headers=headers, data=json.dumps(data))
        data = response.read()
        return json.loads(data)

    @error_logger
    def find_emoticons(self, search=None):
        """
        Find emoticons based on the given search string
        """
        emoticons = self.get_emoticon_list()
        if search:
            emoticons = filter(
                emoticons,
                lambda e: re.match(search, e['shortcut'])
            )
        return map(
            emoticons,
            lambda e: '(%s)' % e['shortcut']
        )


class EmoticonPlugin(WillPlugin, HipchatMixin):

    @respond_to("^emoticon (?P<search>.*?)")
    def single(self, message, search=None):
        emoticons = self.find_emoticons(search)
        self.reply(message, random.choice(emoticons))

    @respond_to("^emoticon list (?P<search>.*?)")
    def list(self, message, search=None):
        emoticons = self.find_emoticons(search)
        self.reply(message, json.dumps(emoticons))
