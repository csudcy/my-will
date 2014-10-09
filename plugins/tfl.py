import json
import random

from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings

from helpers.tfl import TFL


class TFLPlugin(WillPlugin):

    def __init__(self, *args, **kwargs):
        self.emoticons = TFL()
        return WillPlugin.__init__(self, *args, **kwargs)


    @respond_to("^get line status$")
    def line_status(self, message):
        """
        line status: Get the status of the current line
        """
        line_status = self.tfl.get_line_status(message)
        self.say(line_status)
