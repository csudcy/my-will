import json
import os
import requests, urllib

class UrbanDictionary(object):
    def get_definition(self, word):
        req = requests.get('http://urbanscraper.herokuapp.com/define/%s' % word.lower().strip().replace(' ', '+'))
        defn = req.json()
        if 'message' in defn:
            if 'Something went wrong along the way.' in defn['message']:
                return "idk urbanscraper.herokuapp is broken or some shit"
            return "That's not slang fool!"
        return "%s: %s\nUsage: %s" % (word.title(), defn['definition'], defn['example'])

if __name__ == '__main__':
    dm = UrbanDictionary()
    print dm.get_definition('janky')
    print dm.get_definition('asdfasdfzzz')
    print dm.get_definition('food press')
