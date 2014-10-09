from will.plugin import WillPlugin
from will.decorators import respond_to

class BlargPlugin(WillPlugin):
    def __init__(self, *args, **kwargs):
        return WillPlugin.__init__(self, *args, **kwargs)

    @respond_to("^blarg")
    def blarg(self, message, word):
        """
        blarg: Say hi!
        """
        return self.reply(message, 'Hi Danny!')