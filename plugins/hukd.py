from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings

from helpers.hot_deals import Dealer


class HUKDPlugin(WillPlugin):
    def __init__(self, *args, **kwargs):
        self.dealer = Dealer()
        return WillPlugin.__init__(self, *args, **kwargs)

    @respond_to("^deal me (?P<word>[a-zA-Z]+)$")
    def deal(self, message, deal_type):
        """
        deal ___: Get a hot UK deal!
        """
        return self.reply(message, self.dealer.get_deal(deal_type))
