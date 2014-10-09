from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings

from helpers.ascii_art import ASCIIArt


class ASCIIPlugin(WillPlugin):

    def __init__(self, *args, **kwargs):
        self.asii_art = ASCIIArt()
        return WillPlugin.__init__(self, *args, **kwargs)

    @respond_to("^ascii me (?P<text>.*?)$")
    def ascii_me(self, message, text):
        "ascii me ___: Say ___ using a random ascii font"
        self.reply(message, self.asii_art.render(text))
