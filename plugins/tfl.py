from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings

from helpers.tfl_tube import TFLTube
from helpers.tfl_road import TFLRoad


class TFLPlugin(WillPlugin):

    def __init__(self, *args, **kwargs):
        self.tfl_tube = TFLTube()
        self.tfl_road = TFLRoad()
        return WillPlugin.__init__(self, *args, **kwargs)

    @respond_to("^tfl tube me (?P<line>.*)$")
    def tfl_tube_me(self, message, line):
        """
        tfl tube me ___: Get the status of the given tube line
        """
        line_status = self.tfl_tube.get_line_status(line)
        self.reply(message, line_status)

    @respond_to("^tfl road me (?P<road>.*)$")
    def tfl_road_me(self, message, road):
        """
        tfl road me ___: Get the status of the given road
        """
        road_status = self.tfl_road.get_road_status(road)
        self.reply(message, road_status)

