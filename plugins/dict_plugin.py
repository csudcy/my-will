from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings

from dict_mixin import DictMixin

class DictPlugin(WillPlugin, DictPlugin):
    def __init__(self, *args, **kwargs):
        DictMixin.__init__(self)
        WillPlugin.__init__(self, *args, **kwargs)

    @respond_to("^define (?P<word>.)$")
    def define(self, message, word):
        """
        define _____: Get the definition of a word
        """
        return self.reply(message, self.get_definition())
