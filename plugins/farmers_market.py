from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings
from datetime import datetime


class FarmersMarketPlugin(WillPlugin):

    @periodic(hour='12', minute='0', day_of_week='thu-fri')
    def farmers_market_reminder(self, message, word):
        now = datetime.now()
        if now.weekday() == 3:
            msg = "Get your pulled pork baps today!"
        else:
            msg = "Get your cheeky burgers today!"
        return self.say("It's farmers' market day. {0}".format(msg))

    @respond_to("market")
    def is_it_farmers_market_day(self, message, word):
        now = datetime.now()
        if now.weekday() in [3, 4]:
            return self.say("YES IT'S FARMERS' MARKET DAY")
        else:
            return self.say("No it's not farmers' market day")
