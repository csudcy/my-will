from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings

from helpers.tube_tfl import TUBETFL
from helpers.road_tfl import ROADTFL


class TFLPlugin(WillPlugin):

    def __init__(self, *args, **kwargs):
        self.tube_tfl = TUBETFL()
        self.road_tfl = ROADTFL()
        return WillPlugin.__init__(self, *args, **kwargs)

    @respond_to("^tfl tube me (?P<line>.*)$")
    def tfl_tube_me(self, message, line):
        """
        tfl tube me __: Get the status of the given tube line
        """
        line_status = self.tube_tfl.get_line_status(line)
        self.reply(message, line_status)

    @respond_to("^tfl road me(?P<road>.*)$")
    def tfl_road_me(self, message, road):
        """
        tfl road me __: Get the status of the given road
        """
        road_status = self.road_tfl.get_road_status(road)
        self.reply(message, road_status)

