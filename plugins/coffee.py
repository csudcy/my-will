import random

from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings

from helpers.coffee import Coffee


class coffeePlugin(WillPlugin):

    def __init__(self, *args, **kwargs):
        self.coffee = Coffee(
            self.load,
            self.save
        )
        return WillPlugin.__init__(self, *args, **kwargs)

    @respond_to("^coffee me$")
    def coffee_me(self, message):
        "coffee me: Show the orders for everyone in the room"
        self.reply(message, 'TODO: Get everyone in the room')

    @respond_to("^coffee set (?P<order>.+?)$")
    def coffee_set(self, message, order):
        "coffee set ___: Save ___ as your coffee order"
        user = message.sender['name']
        self.reply(
            message,
            self.coffee.set(
                user,
                order
            )
        )

    @respond_to("^coffee get$")
    def coffee_get(self, message):
        "coffee get: Show your current coffee order"
        user = message.sender['name']
        self.reply(
            message,
            self.coffee.get(
                user
            )
        )

    @respond_to("^coffee clear$")
    def coffee_clear(self, message):
        "coffee clear: Clear your coffee order"
        user = message.sender['name']
        self.reply(
            message,
            self.coffee.clear(
                user
            )
        )

    @respond_to("^coffee RESET$")
    def coffee_reset(self, message):
        self.coffee.reset()
        self.reply(message, 'All coffee orders removed')
