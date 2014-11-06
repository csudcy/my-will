import requests
import random

class GifMeUpScotty(object):

    def find(self, search_query):
        data = {
            'tag': search_query,
            'api_key': 'dc6zaTOxFJmzC'
        }

        r = requests.get("http://api.giphy.com/v1/gifs/random", params=data)
        results = r.json()['data'] if r.status_code == 200 else {'image_original_url': 'GIPHY API IS BORKED'}
        return None if not results else results['image_original_url']


if __name__ == '__main__':
    gm = GifMeUpScotty()
    print gm.find('nic cage')
    print gm.find('asa sdfads fads fdsaf dasf adsf adsf dsaf adsfsadF ASDGEWAdfasdf')
    print gm.find('extreme sports')
