from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings
import requests


class FilmsPlugin(WillPlugin):

    @respond_to("^film me (?P<search_query>.*)$")
    def film_me(self, message, search_query):
        data = {
            't': search_query,
            'tomatoes': True
        }

        r = requests.get('http://www.omdbapi.com/', params=data)
        try:
            results = r.json()
            response = """Here's my info for "{Title}":
Year: {Year}
Director: {Director}
Plot: {Plot}
Rotten Tomatoes Consensus: {tomatoConsensus}
Rotten Tomatoes Rating: {tomatoRating}""".format(results)
        except TypeError:
            response = """Sorry I can't find any info for "{0}" right now""".format(search_query)

        self.reply(message, response)
