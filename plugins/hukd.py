from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings

from helpers.hot_deals import Dealer


class HUKDPlugin(WillPlugin):
    def __init__(self, *args, **kwargs):
        self.dealer = Dealer()
        return WillPlugin.__init__(self, *args, **kwargs)

    @respond_to("^deal me ?(?P<deal_type>[a-zA-Z]*)$")
    def deal(self, message, deal_type=None):
        """
        deal me [___]: Get a hot UK deal!
        """
        # Set the default here because I'm not sure how deal_type is set if the capture group is empty
        if not deal_type:
            deal_type = 'random'
        return self.reply(message, self.dealer.get_deal(deal_type))
