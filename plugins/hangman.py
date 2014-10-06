from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings

from mixins.hangman_mixin import HangmanMixin


class HangmanPlugin(WillPlugin, HangmanMixin):
    def __init__(self, *args, **kwargs):
        HangmanMixin.__init__(self)
        WillPlugin.__init__(self, *args, **kwargs)

    @respond_to("^hangman me$")
    def hangman_me(self, message):
        """
        hangman me: Start a new game of hangman
        """
        self.say('/code '+self.new_game(), message=message)

    @respond_to("^hangman status$")
    def hangman_status(self, message):
        """
        hangman status: Check the progress of the current game
        """
        self.say('/code '+self.get_status(), message=message)

    @respond_to("^hangman reveal$")
    def hangman_reveal(self, message):
        # Reveal hangmans inner secrets
        self.reply(message, 'Here are all my secrets:')
        self.say('/code '+self.get_secrets(), message=message)

    @respond_to("^hangman guess (?P<guess>.*)$")
    def hangman_guess(self, message, guess):
        """
        hangman guess ___: Make a guess in the current hangman game
        """
        return self.say('/code '+self.guess(guess), message=message)
