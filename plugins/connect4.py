from will.plugin import WillPlugin
from will.decorators import respond_to

from helpers.connect4 import Connect4


class Connect4Plugin(WillPlugin):
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
            self.games[id] = Connect4()
        return self.games[id]

    @respond_to("^connect4 me$")
    def hangman_me(self, message):
        """
        connect4 me: Start a new game of connect4
        """
        game = self.get_game(message)
        self.say(game.new_game(), message=message, html=True)

    @respond_to("^connect4 status$")
    def hangman_status(self, message):
        """
        connect4 status: Check the progress of the current game
        """
        game = self.get_game(message)
        self.say(game.get_status(), message=message, html=True)

    @respond_to("^connect4 move (?P<move>.*)$")
    def hangman_guess(self, message, move):
        """
        connect4 move ___: Make a move in the current connect4 game
        """
        game = self.get_game(message)
        self.say(game.move(move), message=message, html=True)
