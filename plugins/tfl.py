from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings

from helpers.tfl import TFL


class TFLPlugin(WillPlugin):

    def __init__(self, *args, **kwargs):
        self.tfl = TFL()
        return WillPlugin.__init__(self, *args, **kwargs)


    @respond_to("^tfl me$")
    def tfl_me(self, message):
        """
        tfl_me: Get the status of the current line
        """
        line_status = self.tfl.get_line_status(message)
        self.say(line_status)
