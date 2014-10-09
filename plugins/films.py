from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings

from helpers.films import Films


class FilmsPlugin(WillPlugin):

    def __init__(self, *args, **kwargs):
        self.films = Films()
        return WillPlugin.__init__(self, *args, **kwargs)

    @respond_to("^film me (?P<search_query>.*)$")
    def film_me(self, message, search_query):
        """
        film me ___: Find info about ___ from rotten tomatoes
        """
        self.reply(message, self.films.search(search_query))
