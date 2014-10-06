import random
import re
import json

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


SECRETS_TEMPLATE = """
    word_count    : {word_count}
    state         : {state}
    word          : {word}
    word_revealed : {word_revealed}
    guesses_right : {guesses_right}
    guesses_wrong : {guesses_wrong}
"""


STATUS_TEMPLATE = """
    {board[0]}
    {board[1]}
    {board[2]}
    {board[3]}
    {board[4]}
    {board[5]}
    {board[6]}
    {board[7]}

    Word: {word}

    Right guesses: {guesses_right}
    Wrong guesses: {guesses_wrong}
"""

SECRETS_TEMPLATE = """
    word_count    : {word_count}
    state         : {state}
    word          : {word}
    word_revealed : {word_revealed}
    guesses_right : {guesses_right}
    guesses_wrong : {guesses_wrong}
"""


STATUS_TEMPLATE = """
    {board[0]}
    {board[1]}
    {board[2]}
    {board[3]}
    {board[4]}
    {board[5]}
    {board[6]}
    {board[7]}

    Word: {word}
    Guessed: {guesses_wrong}
"""

class HangmanMixin(object):
    def __init__(self):
        # Load the dictionary
        with open('/app/plugins/dict/dictionary.json', 'r') as f:
            self.dict = json.load(f)
        # ditch the shit words
        bad_keys = [k for k in self.dict if not re.match('^[a-zA-Z]{4,10}$', k)]
        for k in bad_keys:
            self.dict.pop(k)
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
        self.word = random.choice(self.dict.keys())
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

        # Prepare the output
        output = STATUS_TEMPLATE.format(
            board=HANGMAN_STATES[len(self.guesses_wrong)],
            word=self.word_revealed,
            guesses_right=', '.join(self.guesses_right),
            guesses_wrong=', '.join(self.guesses_wrong),
        )

        # Check if the game is over
        if self.state == 'WON':
            output += '\n YOU WON! \n'
            output += '{word}: {definition}'.format(word=self.word, definition=self.dict[self.word])
        elif self.state == 'LOST':
            output += '\n GAME OVER! The word was %s \n' % self.word
            output += '{word}: {definition}'.format(word=self.word, definition=self.dict[self.word])

        # Send back the message
        return output

    def get_secrets(self):
        """
        Reveal all my inner secrets...
        """
        return SECRETS_TEMPLATE.format(
            word_count=len(self.dict),
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

        # Check the input
        guess = guess.strip().upper()
        if not re.match('^[A-Z]$', guess):
            return 'That\'s not a letter!'

        # Check it hasnt been tried before
        if guess in self.guesses_right or guess in self.guesses_wrong:
            return 'You already tried {guess}!'.format(
                guess=guess,
            )

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

        return self.get_status()

if __name__ == '__main__':
    hm = HangmanMixin()
    print hm.get_secrets()
    print hm.get_status()
    print hm.get_secrets()
    print hm.new_game()
    print hm.get_secrets()
    print hm.guess('1')
    print hm.guess('e')
    print hm.guess('t')
    print hm.guess('a')
    print hm.guess('o')
    print hm.guess('i')
    print hm.guess('n')
    print hm.guess('s')
    print hm.guess('c')
    print hm.guess('h')
    print hm.guess('r')
    print hm.guess('d')
    print hm.guess('l')
    print hm.guess('u')
    for letter in 'abcdefghijklmnopqrstuvwxyz':
        if hm.status() == 'PLAYING':
            hm.guess(letter)
        else:
            break
