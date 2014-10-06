import json
import random

from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings

from mixins.hipchat_emoticons_mixin import HipchatEmoticonsMixin


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
