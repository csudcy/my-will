from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings

from helpers.hot_deals import Dealer


class HUKDPlugin(WillPlugin):
    def __init__(self, *args, **kwargs):
        self.dealer = Dealer()
        return WillPlugin.__init__(self, *args, **kwargs)

    @respond_to("^deal me$")
    def deal_random(self, message):
        """deal me: Get a random hot UK deal!"""
        return self.reply(message, self.dealer.get_deal('random'))

    @respond_to("^deal me hot$")
    def deal_hot(self, message):
        """deal me hot: Get me the hottest hot UK deal!"""
        return self.reply(message, self.dealer.get_deal('hot'))

    @respond_to("^deal me new$")
    def deal_new(self, message):
        """deal me new: Get me the latest hot UK deal!"""
        return self.reply(message, self.dealer.get_deal('new'))
