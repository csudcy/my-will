from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings

from helpers.business import Business


class BusinessPlugin(WillPlugin):

    def __init__(self, *args, **kwargs):
        self.business = Business()
        return WillPlugin.__init__(self, *args, **kwargs)

    @hear("business")
    def hear_business(self, message):
        """
        business: Get your favourite corporate strategems
        """
        return self.reply(message, self.business.acquire_business())
