import json
import os
import random


class Business(object):
    def __init__(self, *args, **kwargs):
        # Work out the path to the dictionary
        if os.path.abspath('.').endswith('helpers'):
            buzzwords_path = './buzzwords.json'
        else:
            buzzwords_path = './helpers/buzzwords.json'

        with open(buzzwords_path) as f:
            self.buzzwords = json.load(f)

    def acquire_business(self):
        business = '{before1} {before2} {noun} {after} '.format(
            before1=random.choice(self.buzzwords['before']),
            before2=random.choice(self.buzzwords['before']),
            noun=random.choice(self.buzzwords['nouns']),
            after=random.choice(self.buzzwords['after']),
        ).title()
        return business

if __name__ == '__main__':
    b = Business()
    print b.acquire_business()
    print b.acquire_business()
    print b.acquire_business()
