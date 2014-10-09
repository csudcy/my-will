import json
import random

def acquire_business():
    buzzwords_file = open('buzzwords.json')
    buzzwords = json.load(buzzwords_file)
    business = random.choice(buzzwords['before']) + ' ' + random.choice(buzzwords['before']) + ' ' + random.choice(buzzwords['nouns']) + ' '  + random.choice(buzzwords['after'])
    return business

if __name__ == '__main__':
    print acquire_business()