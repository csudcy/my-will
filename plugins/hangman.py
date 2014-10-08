from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings

from helpers.hangman import Hangman


class HangmanPlugin(WillPlugin):
    games = {}

    def get_game(self, message):
        """
        Get the game for the room specified in message
        """
        room = self.get_room_from_message(message)
        if room:
            id = room['xmpp_jid']
        else:
            # This is a pm
            id = message.sender["hipchat_id"]

        if id not in self.games:
            self.games[id] = Hangman()
        return self.games[id]

    @respond_to("^hangman me$")
    def hangman_me(self, message):
        """
        hangman me: Start a new game of hangman
        """
        game = self.get_game(message)
        self.say('/code '+game.new_game(), message=message)

    @respond_to("^hangman status$")
    def hangman_status(self, message):
        """
        hangman status: Check the progress of the current game
        """
        game = self.get_game(message)
        self.say('/code '+game.get_status(), message=message)

    @respond_to("^hangman reveal$")
    def hangman_reveal(self, message):
        # Reveal hangmans inner secrets
        game = self.get_game(message)
        self.reply(message, 'Here are all my secrets:')
        self.say('/code '+game.get_secrets(), message=message)

    @respond_to("^hangman guess (?P<guess>.*)$")
    def hangman_guess(self, message, guess):
        """
        hangman guess ___: Make a guess in the current hangman game
        """
        game = self.get_game(message)
        return self.say('/code '+game.guess(guess), message=message)
