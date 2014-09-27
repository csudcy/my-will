import functools
import json
import logging
import random
import re
import traceback

from memoize import Memoizer
from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings
import requests


logger = logging.getLogger(__name__)

logger.critical('load start')

EMOTICONS_URL = "https://%(server)s/v2/emoticon?max-results=1000&auth_token=%(token)s"

store = {}
memo = Memoizer(store)

def error_logger(func):
    @functools.wraps(func)
    def _error_logger(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            logger.critical('Error in {func}: \n{tb}'.format(
                func=func,
                tb=traceback.format_exc(),
            ))


class HipchatEmoticonsMixin(object):

    @memo(max_age=12*60*60)
    def get_emoticon_list(self):
        """
        Fetch the list of emoticons from hipchat
        """
        logger.critical('get_emoticon_list start')
        url = EMOTICONS_URL % {
            "server": settings.HIPCHAT_SERVER,
            "token": settings.V2_TOKEN
        }
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        response = requests.get(url, headers=headers, data=json.dumps(data))
        data = response.read()
        logger.critical('get_emoticon_list end')
        return json.loads(data)

    @error_logger
    def find_emoticons(self, search=None):
        """
        Find emoticons based on the given search string
        """
        logger.critical('find_emoticons start')
        emoticons = self.get_emoticon_list()
        if search:
            emoticons = filter(
                emoticons,
                lambda e: re.match(search, e['shortcut'])
            )
        logger.critical('find_emoticons end')
        return map(
            emoticons,
            lambda e: '(%s)' % e['shortcut']
        )


class EmoticonPlugin(WillPlugin, HipchatEmoticonsMixin):

    @respond_to("^emoticon me (?P<search>.*?)")
    @error_logger
    def single(self, message, search=None):
        "emoticon me ___: Search hipchat emoticons for ___ and return a random one"
        logger.critical('single start')
        emoticons = self.find_emoticons(search)
        if emoticons:
            self.reply(message, random.choice(emoticons))
        else:
            self.reply(message, 'I cannae find any captain!')
        logger.critical('single end')

    @respond_to("^emoticons me (?P<search>.*?)")
    @error_logger
    def list(self, message, search=None):
        "emoticons me ___: Search hipchat emoticons for ___ and return all of them"
        logger.critical('list start')
        emoticons = self.find_emoticons(search)
        if emoticons:
            self.reply(message, json.dumps(emoticons))
        else:
            self.reply(message, 'I cannae find any captain!')
        logger.critical('list end')

logger.critical('load end')
