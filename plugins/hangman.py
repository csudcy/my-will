import random
import re

from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings


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


REVEAL_TEMPLATE = """
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

class HangmanPlugin(WillPlugin):
    def __init__(self, *args, **kwargs):
        # Load the dictionary
        with open('/usr/share/dict/words', 'r') as f:
            contents = f.read()
        words = contents.splitlines()
        self.words = [word.upper() for word in words if re.match(word, '^[a-zA-Z]{4,10}$')]

        # Game variables
        self.state = 'NOT_PLAYING'
        self.word = None
        self.word_revealed = None
        self.guesses_right = None
        self.guesses_wrong = None

    @respond_to("^hangman me$")
    def hangman_me(self, message):
        """
        Start a new game of hangman
        """
        if self.state == 'PLAYING':
            return self.reply(message, 'You have to finish the current game first!')

        # Setup a new game
        self.state = 'PLAYING'
        self.word = random.choice(self.words)
        self.guesses_right = []
        self.guesses_wrong = []

        # Show the user what's going on
        self.output_status(message)

    @respond_to("^hangman status$")
    def hangman_status(self, message):
        """
        Check the progress of the current game
        """
        self.output_status(message)

    def output_status(self, message):
        # Check we're currently playing
        if self.state == 'NOT_PLAYING':
            return self.reply(message, 'Doesn\'t look like you\'ve started a game yet?')

        # Prepare the output
        output = STATUS_TEMPLATE.format(
            board=HANGMAN_STATES[len(self.guesses_wrong)],
            word='word',
            guesses_right=', '.join(guesses_right),
            guesses_wrong=', '.join(guesses_wrong),
        )

        # Check if the game is over
        if self.state == 'WON':
            output += '\n YOU WON! \n'
        elif self.state == 'LOST':
            output += '\n GAME OVER! \n'

        # Send back the message
        self.reply(message, output)

    @respond_to("^hangman reveal$")
    def hangman_reveal(self, message):
        # Reveal hangmans inner secrets
        self.reply(message, 'Here is my current state:')
        self.reply(message, REVEAL_TEMPLATE.format(
            word_count=len(self.words),
            state=self.state,
            word=self.word,
            word_revealed=self.word_revealed,
            guesses_right=self.guesses_right,
            guesses_wrong=self.guesses_wrong,
        ))

    @respond_to("^hangman guess (?P<guess>.)$")
    def hangman_guess(self, message, guess):
        """
        Make a guess in the current hangman game
        """
        # Prepare the input
        guess = guess.strip().upper()

        # Check it hasnt been tried before
        if guess in guesses_right or guess in guesses_wrong:
            return self.reply(message, 'You already tried {guess}!'.format(
                guess=guess,
            ))

        if guess in self.word:
            guesses_right.append(guess)
            # Update word revealed
            self.word_revealed = ' '.join([w for w in self.word if w in self.guesses_right else '_'])
        else:
            guesses_wrong.append(guess)

        self.output_status(message)
