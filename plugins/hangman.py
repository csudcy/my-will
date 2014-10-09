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
        self.say(game.new_game(), message=message, html=True)

    @respond_to("^hangman status$")
    def hangman_status(self, message):
        """
        hangman status: Check the progress of the current game
        """
        game = self.get_game(message)
        self.say(game.get_status(), message=message, html=True)

    @respond_to("^hangman reveal$")
    def hangman_reveal(self, message):
        # Reveal hangmans inner secrets
        game = self.get_game(message)
        self.say('Here are all my secrets:')
        self.say(game.get_secrets(), message=message, html=True)

    @respond_to("^hangman guess (?P<guess>.*)$")
    def hangman_guess(self, message, guess):
        """
        hangman guess ___: Make a guess in the current hangman game
        """
        game = self.get_game(message)
        self.say(game.guess(guess), message=message, html=True)

    @respond_to("^hangman cheat (?P<guess>.*)$")
    def hangman_cheat(self, message, guess):
        game = self.get_game(message)
        for letter in guess:
            output = game.guess(letter)
            if game.state != 'PLAYING':
                break
        self.say(output, message=message, html=True)
