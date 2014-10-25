import random

from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings

from helpers.coffee import Coffee
import settings


class CoffeePlugin(WillPlugin):

    def __init__(self, *args, **kwargs):
        self.coffee = Coffee(
            self.load,
            self.save,
            settings.HIPCHAT_SERVER,
            settings.V2_TOKEN,
        )
        return WillPlugin.__init__(self, *args, **kwargs)

    @respond_to("^coffee me$")
    def coffee_me(self, message):
        "coffee me: Show the orders for everyone in the room"
        # Try to get the room from the mesage
        room = self.get_room_from_message(message)
        if not room:
            # This is a pm
            return self.coffee_get(message)

        room_id = room['room_id']

        self.reply(
            message,
            self.coffee.get_all(
                room_id
            )
        )

    @respond_to("^coffee set (?P<order>.+?)$")
    def coffee_set(self, message, order):
        "coffee set ___: Save ___ as your coffee order"
        user = message.sender['nick']
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
        user = message.sender['nick']
        self.reply(
            message,
            self.coffee.get(
                user
            )
        )

    @respond_to("^coffee clear$")
    def coffee_clear(self, message):
        "coffee clear: Clear your coffee order"
        user = message.sender['nick']
        self.reply(
            message,
            self.coffee.clear(
                user
            )
        )

    @respond_to("^coffee all$")
    def coffee_all(self, message):
        "coffee all: Show all existing coffee orders"
        self.reply(
            message,
            self.coffee.get_all()
        )

    @respond_to("^coffee RESET$")
    def coffee_reset(self, message):
        self.coffee.reset()
        self.reply(message, 'All coffee orders removed')
