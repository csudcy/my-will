from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings

from helpers.urban_dictionary import UrbanDictionary


class UrbanDefinePlugin(WillPlugin):
    def __init__(self, *args, **kwargs):
        self.dictionary = UrbanDictionary()
        return WillPlugin.__init__(self, *args, **kwargs)

    @respond_to("^slang (?P<word>[a-zA-Z]+)$")
    def slang(self, message, word):
        """
        slang ___: Get the definition of a slang
        """
        return self.reply(message, self.dictionary.get_definition(word))
