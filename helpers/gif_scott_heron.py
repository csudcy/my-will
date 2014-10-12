import requests
import random

class GifMeUpScotty(object):

    def find(self, search_query):
        data = {
            "q": search_query + " filetype:gif",
            "v": "1.0",
            "safe": "active",
            "rsz": "8"
        }
        r = requests.get("http://ajax.googleapis.com/ajax/services/search/images", params=data)

        try:
            results = r.json()["responseData"]["results"]
        except TypeError:
            return None

        return random.choice(results)["unescapedUrl"]

if __name__ == '__main__':
    gm = GifMeUpScotty()
    print gm.gif_me('nic cage')
    print gm.gif_me('asdfasdf')
