import json

class DictMixin(object):
    def __init__(self):
        # Load the dictionary
        with open('/app/plugins/dict/dictionary.json', 'r') as f:
            self.dict = json.load(f)

    def get_definition(self, word):
        if word.upper() in self.dict:
            return '{0}: {1}'.format(word.title(), self.dict[word.upper()])
        else:
            return '{0} isn\'t a word you numpty'.format(word.title())

if __name__ == '__main__':
    dm = DictMixin()
    print dm.get_definition('diploblastic')
    print dm.get_definition('asdfasdf')
