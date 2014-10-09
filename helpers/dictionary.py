import json
import os
import random


class Dictionary(object):
    def __init__(self):
        # Work out the path to the dictionary
        dict_path = './dict/dictionary.json'
        if os.path.abspath('.').endswith('helpers'):
            dict_path = '.' + dict_path

        # Load the dictionary
        with open(os.path.abspath(dict_path), 'r') as f:
            self._dict = json.load(f)

    def get_dict(self):
        return self._dict

    def get_random_definition(self):
        word = random.choice(self._dict.keys())
        return self.get_definition(word)

    def get_definition(self, word):
        if word.upper() in self._dict:
            return '{0}: {1}'.format(word.title(), self._dict[word.upper()])
        else:
            return '{0} isn\'t a word you numpty'.format(word.title())

if __name__ == '__main__':
    dm = Dictionary()
    print dm.get_definition('diploblastic')
    print dm.get_definition('asdfasdf')
    print dm.get_random_definition()
