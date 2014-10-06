from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings

from mixins.dict_mixin import DictMixin

class DefinePlugin(WillPlugin, DictMixin):
    def __init__(self, *args, **kwargs):
        DictMixin.__init__(self)
        WillPlugin.__init__(self, *args, **kwargs)

    @respond_to("^define (?P<word>[a-zA-Z]+)$")
    def define(self, message, word):
        """
        define ___: Get the definition of a word
        """
        return self.reply(message, self.get_definition(word))
