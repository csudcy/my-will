import requests


RESPONSE_TEMPLATE = """{Title} ({Year}) - {tomatoRating}/10
http://imdb.com/title/{imdbID}
Director: {Director}
{Plot}

Review: {tomatoConsensus}
"""

class Films(object):

    def search(self, search_query):
        data = {
            't': search_query,
            'tomatoes': True
        }
        r = requests.get('http://www.omdbapi.com/', params=data)

        try:
            results = r.json()
            return RESPONSE_TEMPLATE.format(**results)
        except TypeError:
            return 'Sorry, I can\'t find any info for "{0}" right now'.format(search_query)

if __name__ == '__main__':
    f = Films()
    print f.search('Superman')
    print f.search('Avatar')
