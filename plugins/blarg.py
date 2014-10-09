from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings


class BlargPlugin(WillPlugin):
    def __init__(self, *args, **kwargs):
        return WillPlugin.__init__(self, *args, **kwargs)

    @respond_to("^blarg")
    def define(self, message, word):
        """
        define ___: Get the definition of a word
        """
        return self.reply(message, 'Hi Danny!')