import re
import numpy as np


OUTPUT_TEMPALTE = """<pre>
=========
|{0}|
|{1}|
|{2}|
|{3}|
|{4}|
|{5}|
=========
</pre>"""


class Connect4(object):
    def __init__(self):
        # Game variables
        self.state = 'NOT_PLAYING'
        self.board = None
        self.x_to_play = None

    def new_game(self):
        """
        Start a new game of hangman
        """
        if self.state == 'PLAYING':
            return 'You have to finish the current game first!'

        # Setup a new game
        self.state = 'PLAYING'
        self.board = [['-' for i in range(6)] for j in range(7)]

        # Show the user what's going on
        return self.get_status()

    def get_status(self):
        """
        Get the text represenation of the current game state
        """
        # Check we're currently playing
        if self.state == 'NOT_PLAYING':
            return 'Sorry, it doesn\'t look like you\'ve started a game yet?'

        rows = []
        for i in range(5, -1, -1):
            rows.append(
                ''.join([x[i] for x in self.board])
            )
        output = OUTPUT_TEMPALTE.format(*rows)

        # Check if the game is over
        if self.state != 'PLAYING':
            output += '<br/>' + 'GAME OVER!'

        # Send back the message
        return output

    def play(self, move):
        """
        Make a guess
        """
        # Check we're currently playing
        if self.state == 'NOT PLAYING':
            return 'It looks like you finished already :('
        if self.state != 'PLAYING':
            return 'Sorry, it doesn\'t look like you\'re currently playing a game'

        # Check this is a guess we're interested in
        move = move.strip().upper()
        if len(move) != 2 or not re.match('^[OX][1-7]$', move):
            return '{move} is not in correct format! (O or X followed by a number from 1-7)'.format(
                move=move,
            )

        # Check the input
        letter = move[0]
        if letter == 'X' and self.x_to_play == False:
            return 'Wait for your turn O!'
        elif letter == 'O' and self.x_to_play == True:
            return 'Wait for your turn X!'

        number = int(move[1])
        column = self.board[number-1]
        empty_space_index = None
        for i in range(len(column)):
            if column[i] == '-':
                empty_space_index = i
                break

        if empty_space_index == None:
            return 'That column is full!'

        column[empty_space_index] = letter

        winner = self.check_board()
        if winner:
            self.state = 'NOT PLAYING'
            return self.get_status() + '<br/>Player ' + winner + ' wins!'

        if letter == 'X':
            self.x_to_play = False
        elif letter == 'O':
            self.x_to_play = True

        return self.get_status()

    def check_four_in_a_row(self, spaces):
        if len(spaces) < 4:
            return None
        count = 0
        potential_winner = None
        for space in spaces:
            if potential_winner == None and space != '-':
                potential_winner = space
                count = 1
            elif potential_winner and space == potential_winner:
                count += 1
                if count == 4:
                    return potential_winner
            elif potential_winner and space != potential_winner:
                count = 0
                potential_winner = None
        return None

    def check_board(self):
        #check columns
        for column in self.board:
            winner = self.check_four_in_a_row(column)
            if winner:
                return winner

        #check rows
        for i in range(6):
            row = [x[i] for x in self.board]
            winner = self.check_four_in_a_row(row)
            if winner:
                return winner

        #check diagonals
        matrix = np.array(self.board)
        diags = [matrix[::-1,:].diagonal(i) for i in range(-matrix.shape[0]+1,matrix.shape[1])]
        diags.extend(matrix.diagonal(i) for i in range(matrix.shape[1]-1,-matrix.shape[0],-1))
        for diag in diags:
            winner = self.check_four_in_a_row(diag.tolist())
            if winner:
                return winner

        return None

if __name__ == '__main__':
    hm = Connect4()
    print hm.get_status()
    print hm.new_game()
    print hm.play('O1')
    print hm.play('x2')
    print hm.play('O2')
    print hm.play('x3')
    print hm.play('O4')
    print hm.play('x3')
    print hm.play('O3')
    print hm.play('x4')
    print hm.play('O5')
    print hm.play('x4')
    print hm.play('o4')
