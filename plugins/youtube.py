from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings

from helpers.youtube import Youtube


class ImagesPlugin(WillPlugin):

    def __init__(self, *args, **kwargs):
        self.youtube = Youtube()
        return WillPlugin.__init__(self, *args, **kwargs)

    @respond_to('youtube me (?P<search_query>.*)$')
    def youtube_me(self, message, search_query):
        """youtube me ___ : Search youtube for ___, and post a random one."""

        result = self.youtube.find(search_query)
        if result:
            self.reply(message, result)
        else:
            self.reply(message, 'Why would anyone make a video about that?!')
