from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings

from helpers.gif_scott_heron import GifMeUpScotty


class GifPlugin(WillPlugin):

    def __init__(self, *args, **kwargs):
        self.gmus = GifMeUpScotty()
        return WillPlugin.__init__(self, *args, **kwargs)

    @respond_to('gif me(?P<search_query>.*)$')
    def youtube_me(self, message, search_query):
        """gif me ___ : Search google imaghes for ___, and post a random gif."""

        result = self.gmus.find(search_query.strip())
        if result:
            self.reply(message, result)
        else:
            self.reply(message, 'Why would anyone want a gif about that?!')
