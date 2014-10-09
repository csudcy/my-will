import random

import requests


class Youtube(object):

    def find(self, search_query=None):
        # Query the API
        data = {
            'v': 2,
            'alt': 'json',
            'racy': 'exclude',
            "max-results": 1,
            'start-index': random.randint(1, 100)
        }
        if search_query:
            data['q'] = search_query
        response = requests.get('http://gdata.youtube.com/feeds/api/videos/', params=data)

        # Find the video id
        try:
            result = response.json()['feed']['entry'][0]['id']['$t']
        except Exception:
            return None

        # Return the full URL
        id = result.split(':')[-1]
        return 'http://www.youtube.com/v/{id}?autoplay=1'.format(id=id)

if __name__ == '__main__':
    yt = Youtube()
    print yt.find()
    print yt.find()
    print yt.find('how')
    print yt.find('sparta')
