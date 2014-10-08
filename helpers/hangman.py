import random
import re
from dict_mixin import Dictionary

HANGMAN_STATES = [
    [
        '        ',
        '        ',
        '        ',
        '        ',
        '        ',
        '        ',
        '        ',
        '________'
    ], [
        '        ',
        '        ',
        '        ',
        '        ',
        '        ',
        '        ',
        '        ',
        '__\_____'
    ], [
        '        ',
        ' |      ',
        ' |      ',
        ' |      ',
        ' |      ',
        ' |      ',
        ' |      ',
        '_|\_____'
    ], [
        '        ',
        ' |/     ',
        ' |      ',
        ' |      ',
        ' |      ',
        ' |      ',
        ' |      ',
        '_|\_____'
    ], [
        ' _____  ',
        ' |/     ',
        ' |      ',
        ' |      ',
        ' |      ',
        ' |      ',
        ' |      ',
        '_|\_____'
    ], [
        ' _____  ',
        ' |/  |  ',
        ' |      ',
        ' |      ',
        ' |      ',
        ' |      ',
        ' |      ',
        '_|\_____'
    ], [
        ' _____  ',
        ' |/  |  ',
        ' |   O  ',
        ' |      ',
        ' |      ',
        ' |      ',
        ' |      ',
        '_|\_____'
    ], [
        ' _____  ',
        ' |/  |  ',
        ' |   O  ',
        ' |  /   ',
        ' |      ',
        ' |      ',
        ' |      ',
        '_|\_____'
    ], [
        ' _____  ',
        ' |/  |  ',
        ' |   O  ',
        ' |  / \ ',
        ' |      ',
        ' |      ',
        ' |      ',
        '_|\_____'
    ], [
        ' _____  ',
        ' |/  |  ',
        ' |   O  ',
        ' |  /|\ ',
        ' |   |  ',
        ' |      ',
        ' |      ',
        '_|\_____'
    ], [
        ' _____  ',
        ' |/  |  ',
        ' |   O  ',
        ' |  /|\ ',
        ' |   |  ',
        ' |  /   ',
        ' |      ',
        '_|\_____'
    ], [
        ' _____  ',
        ' |/  |  ',
        ' |   O  ',
        ' |  /|\ ',
        ' |   |  ',
        ' |  / \ ',
        ' |      ',
        '_|\_____'
    ],
]


SECRETS_TEMPLATE = u"""
    total_words   : {total_words}
    valid_words   : {valid_words}
    state         : {state}
    word          : {word}
    word_revealed : {word_revealed}
    guesses_right : {guesses_right}
    guesses_wrong : {guesses_wrong}
"""


STATUS_TEMPLATE = u"""    {board[0]}
    {board[1]}
    {board[2]}
    {board[3]}
    {board[4]}
    {board[5]}
    {board[6]}
    {board[7]}

    {word}
    {guesses_wrong}
    Could be {possible_words} of {total_words} words I know
"""

# Load the dictionary
dictionary = Dictionary()

# Only use good words
valid_words = [k for k in dictionary.get_dict() if re.match('^[a-zA-Z]{4,20}$', k)]

class Hangman(object):
    def __init__(self):
        # Game variables
        self.state = 'NOT_PLAYING'
        self.word = None
        self.word_revealed = None
        self.guesses_right = None
        self.guesses_wrong = None

    def new_game(self):
        """
        Start a new game of hangman
        """
        if self.state == 'PLAYING':
            return 'You have to finish the current game first!'

        # Setup a new game
        self.state = 'PLAYING'
        self.word = random.choice(valid_words)
        self.word_revealed = ('_ ' * len(self.word)).strip()
        self.guesses_right = []
        self.guesses_wrong = []

        # Show the user what's going on
        return self.get_status()

    def get_status(self):
        """
        Get the text represenation of the current game state
        """
        # Check we're currently playing
        if self.state == 'NOT_PLAYING':
            return 'Sorry, it doesn\'t look like you\'ve started a game yet?'

        # Find how many words match
        revealed_re = '^%s$' % self.word_revealed
        revealed_re = revealed_re.replace(' ', '')
        if self.guesses_right or self.guesses_wrong:
            remaining_letters_re = '[^%s%s]' % (
                ''.join(self.guesses_right),
                ''.join(self.guesses_wrong),
            )
        else:
            remaining_letters_re = '.'
        revealed_re = revealed_re.replace('_', remaining_letters_re)
        possible_words = [k for k in valid_words if re.match(revealed_re, k)]

        # Prepare the output
        output = STATUS_TEMPLATE.format(
            board=HANGMAN_STATES[len(self.guesses_wrong)],
            word=self.word_revealed,
            guesses_right=', '.join(self.guesses_right),
            guesses_wrong=', '.join(self.guesses_wrong),
            possible_words=len(possible_words),
            total_words=len(valid_words),
        )

        # Check if the game is over
        if self.state != 'PLAYING':
            output += '\n        '
            if self.state == 'WON':
                output += 'YOU WON!'
            elif self.state == 'LOST':
                output += 'GAME OVER!'
            output += '\n\n    {definition}'.format(
                definition=dictionary.get_definition(self.word)
            )

        # Send back the message
        return output

    def get_secrets(self):
        """
        Reveal all my inner secrets...
        """
        return SECRETS_TEMPLATE.format(
            total_words=len(dictionary.get_dict()),
            valid_words=len(valid_words),
            state=self.state,
            word=self.word,
            word_revealed=self.word_revealed,
            guesses_right=self.guesses_right,
            guesses_wrong=self.guesses_wrong,
        )

    def guess(self, guess):
        """
        Make a guess
        """
        # Check we're currently playing
        if self.state == 'WON':
            return 'It looks like you won already - congratulations!'
        if self.state == 'LOST':
            return 'Sorry, it looks like you already lost :('
        if self.state != 'PLAYING':
            return 'Sorry, it doesn\'t look like you\'re currently playing a game?'

        # Check this is a guess we're interested in
        guess = guess.strip().upper()
        if not re.match('^[A-Z]+$', guess):
            if len(guess) == 1:
                return '{guess} is not a letter!'.format(
                    guess=guess,
                )
            else:
                return '"{guess}" is not all letters!'.format(
                    guess=guess,
                )

        # Check the input
        if len(guess) == 1:
            # Single letter guess

            # Check it hasnt been tried before
            if guess in self.guesses_right or guess in self.guesses_wrong:
                return 'You already tried {guess}!'.format(
                    guess=guess,
                )

            # Check if it's right or wrong
            if guess in self.word:
                self.guesses_right.append(guess)

                # Update word revealed
                self.word_revealed = ' '.join([w if w in self.guesses_right else '_' for w in self.word])

                # Check if they won
                if not '_' in self.word_revealed:
                    self.state = 'WON'
            else:
                self.guesses_wrong.append(guess)

                # Check if they lost
                if len(self.guesses_wrong) + 1 == len(HANGMAN_STATES):
                    self.state = 'LOST'
        else:
            # Full word guess

            # Check if the word is correct
            if len(guess) != len(self.word):
                return 'Wat? {guess} isnt even the same number of letters!'.format(
                    guess=guess,
                )
            if guess != self.word:
                return 'Nope, the word is not {guess}!'.format(
                    guess=guess,
                )

            # The guess is correct, you win!
            self.state = 'WON'
            self.word_revealed = self.word

        # Show the final status
        return self.get_status()

if __name__ == '__main__':
    hm = Hangman()
    print hm.get_secrets()
    print hm.get_status()
    print hm.get_secrets()
    print hm.new_game()
    print hm.get_secrets()
    print hm.guess('1')
    print hm.guess('e')
    for letter in 'etaoin schrdlu abcdefghijklmnopqrstuvwxyz':
        print hm.guess(letter)
