from will.plugin import WillPlugin
from will.decorators import respond_to

import datetime

class FarmersMarketPlugin(WillPlugin):
    def __init__(self, *args, **kwargs):
        return WillPlugin.__init__(self, *args, **kwargs)

    @respond_to("^market?")
    def define(self, message, word):
        """
        blarg: Say hi!
        """
        if datetime.datetime.today().weekday() in [3,4]:
            return self.reply(message, "Yeah, Farmer's Market! :D")
        else:
            return self.reply(message, "No.... :(")
