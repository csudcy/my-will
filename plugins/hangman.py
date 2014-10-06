from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings

from hangman_mixin import HangmanMixin


class HangmanPlugin(WillPlugin, HangmanMixin):
    def __init__(self, *args, **kwargs):
        HangmanMixin.__init__(self)
        WillPlugin.__init__(self, *args, **kwargs)

    @respond_to("^hangman me$")
    def hangman_me(self, message):
        """
        Start a new game of hangman
        """
        self.reply(message, self.new_game())

    @respond_to("^hangman status$")
    def hangman_status(self, message):
        """
        Check the progress of the current game
        """
        self.reply(message, self.get_status())

    @respond_to("^hangman reveal$")
    def hangman_reveal(self, message):
        # Reveal hangmans inner secrets
        self.reply(message, 'Here are all my secrets:')
        self.reply(message, self.get_secrets())

    @respond_to("^hangman guess (?P<guess>.)$")
    def hangman_guess(self, message, guess):
        """
        Make a guess in the current hangman game
        """
        return self.reply(message, self.guess(guess))
