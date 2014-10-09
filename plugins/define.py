from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings

from helpers.dictionary import Dictionary


class DefinePlugin(WillPlugin):
    def __init__(self, *args, **kwargs):
        self.dictionary = Dictionary()
        return WillPlugin.__init__(self, *args, **kwargs)

    @respond_to("^define$")
    def define(self, message):
        """
        define: Get the definition of a random word
        """
        return self.reply(message, self.dictionary.get_random_definition())

    @respond_to("^define (?P<word>[a-zA-Z]+)$")
    def define(self, message, word):
        """
        define ___: Get the definition of ___
        """
        return self.reply(message, self.dictionary.get_definition(word))
