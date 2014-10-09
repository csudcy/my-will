from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings

from helpers.tfl import TFL


class TFLPlugin(WillPlugin):

    def __init__(self, *args, **kwargs):
        self.tfl = TFL()
        return WillPlugin.__init__(self, *args, **kwargs)

    @respond_to("^tfl me (?P<line>.*)$")
    def tfl_me(self, message, line):
        """
        tfl me __: Get the status of the given line
        """
        line_status = self.tfl.get_line_status(line)
        self.reply(message, line_status)
