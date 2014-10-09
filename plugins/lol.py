from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings

from helpers.dictionary import Dictionary


class LOLPlugin(WillPlugin):
    def __init__(self, *args, **kwargs):
        self.dictionary = Dictionary()
        return WillPlugin.__init__(self, *args, **kwargs)

    @randomly(num_times_per_day=360*24)
    def define(self, message, word):
        """
        define ___: Get the definition of a word
        """
        return self.reply(message, 'LOL')
