import json
import os
import requests, urllib

class UrbanDictionary(object):
    def get_definition(self, word):
        word = urllib.quote(word.lower())
        req = requests.get('http://urbanscraper.herokuapp.com/define/%s' % word)
        defn = req.json()
        if 'message' in defn:
            return "That's not slang fool!"
        return "%s: %s" % (defn['term'], defn['definition'])

if __name__ == '__main__':
    dm = UrbanDictionary()
    print dm.get_definition('janky')
    print dm.get_definition('asdfasdfzzz')
