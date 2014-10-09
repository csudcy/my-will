import requests

# So apparently there's a whole website dedicated to chuck norris jokes.
#(It's also the only joke site with a decent api that you don't have to pay for, which I could find in five minutes)
CHUCK_NORRIS_JOKE_URL = "http://api.icndb.com/jokes/random"
JOKE_WITH_NAME_URL = "http://api.icndb.com/jokes/random?firstName=%(first_name)s&lastName=%(last_name)s"


class ChuckNorris(object):
    def __init__(self):
        self.cn_url = CHUCK_NORRIS_JOKE_URL
        self.joke_with_name_url = JOKE_WITH_NAME_URL

    def get_joke(self, url):
        headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
        response = requests.get(url, headers=headers)
        return response.json()['value']['joke']

    def get_chuck_norris_joke(self):
        return self.get_joke(self.cn_url)

    def get_joke_with_name(self, first_name, last_name):
        url = self.joke_with_name_url % {
            "first_name": first_name,
            "last_name": last_name
        }
        return self.get_joke(url)

if __name__ == '__main__':
    cn = ChuckNorris()
    print cn.get_chuck_norris_joke()
    print cn.get_joke_with_name('Will', 'Bot')
