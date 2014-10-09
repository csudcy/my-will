from datetime import datetime

from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings


class FarmersMarketPlugin(WillPlugin):

    @periodic(hour='12', minute='0', day_of_week='thu-fri')
    def farmers_market_reminder(self, message, word):
        now = datetime.now()
        if now.weekday() == 3:
            food = 'pulled pork baps'
        else:
            food = 'cheeky burgers'
        return self.say(
            "It's farmers' market day. Get your {food} now!".format(food=food)
        )

    @hear("market")
    def is_it_farmers_market_day(self, message):
        now = datetime.now()
        if now.weekday() in [3, 4]:
            return self.reply(message, "YES IT'S FARMERS' MARKET DAY!")
        else:
            return self.reply(message, "No, it's not farmers' market day :(")
