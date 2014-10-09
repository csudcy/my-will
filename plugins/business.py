from will.plugin import WillPlugin
from will.decorators import respond_to

from helpers.business import aquire_business

class BusinessPlugin(WillPlugin):
    def __init__(self, *args, **kwargs):
        return WillPlugin.__init__(self, *args, **kwargs)

    @respond_to("^business")
    def business(self, message, word):
        """
        business: Get your favourite corporate strategems
        """
        return self.reply(message, aquire_business())