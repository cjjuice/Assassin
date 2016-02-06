import os
import sys
import time


class Assassin:
    def __init__(self, folder_path, file_path):
        self.folder_path = folder_path
        self.file_path = file_path

    # BASIC OPERATIONS

    def make_matrix(self, count):
        columns = 3
        rows = count
        matrix = [[0 for x in range(columns)] for x in range(rows)]

        for row in range(rows):
            for col in range(columns):
                matrix[row][col] = '*'

        for row in range(rows):
            player_name = str(raw_input('Name of player ' + str(row + 1) + ': '))
            matrix[row][1] = player_name

        active_file = open(self.file_path, 'w')
        for row in range(rows):
            for col in range(columns):
                active_file.write(str(matrix[row][col]) + ' ')
            active_file.write('\n')

    def load_matrix(self):
        with open(self.file_path) as file:
           matrix = [[str(item) for item in line.split()] for line in file]
        return matrix

    def save_matrix(self, matrix):
        active_file = open(self.file_path, 'w')
        for row in range(len(matrix)):
            for col in range(len(matrix[0])):
                active_file.write(str(matrix[row][col]) + ' ')
            active_file.write('\n')

    def player_exists(self, matrix, player, col):
        exists = False
        for row in range(len(matrix)):
            if matrix[row][col] == player:
                exists = True
                break
        return exists

    def view_target(self, matrix, player):
        response = ''
        for row in range(len(matrix)):
            if matrix[row][1] == player:
                if matrix[row][2] == '*':
                    response = 'TARGET: unidentified'
                else:
                    response = 'TARGET: ' + matrix[row][2]
                break
        return response

    def view_hitman(self, matrix, player):
        response = ''
        for row in range(len(matrix)):
            if matrix[row][1] == player:
                if matrix[row][0] == '*':
                    response = 'HITMAN: unidentified'
                else:
                    response = 'HITMAN: ' + matrix[row][0]
                break
        return response

    def assign_target(self, matrix, player, target):
        for row in range(len(matrix)):
            if matrix[row][1] == player:
                matrix[row][2] = target
                break
        for row in range(len(matrix)):
            if matrix[row][1] == target:
                matrix[row][0] = player
                break
        print 'Assignment added.'
        time.sleep(1.5)
        sys.stderr.write("\x1b[2J\x1b[H")

    def assign_hitman(self, matrix, player, hitman):
        for row in range(len(matrix)):
            if matrix[row][1] == player:
                matrix[row][0] = hitman
                break
        for row in range(len(matrix)):
            if matrix[row][1] == hitman:
                matrix[row][2] = player
                break
        print 'Assignment added.'
        time.sleep(1.5)
        sys.stderr.write("\x1b[2J\x1b[H")

    def eliminate_player(self, matrix, player, hitman):
        new_hitman = '*'
        new_target = '*'

        for row in range(len(matrix)):
            if matrix[row][1] == player:
                new_hitman = matrix[row][0]
                new_target = matrix[row][2]
                matrix[row][0] = '*'
                matrix[row][1] = '*'
                matrix[row][2] = '*'
        for row in range(len(matrix)):
            if matrix[row][1] == hitman:
                matrix[row][2] = new_target
        for row in range(len(matrix)):
            if matrix[row][1] == new_target:
                matrix[row][0] = new_hitman

        print 'Player eliminated; game updated.'
        time.sleep(1.5)
        sys.stderr.write("\x1b[2J\x1b[H")

    def winner(self, matrix):
        winner = False
        for row in range(len(matrix)):
            if matrix[row][0] == matrix[row][1] and matrix[row][1] == matrix[row][2]:
                if matrix[row][0] != '*':
                    winner = True
                    print 'The game is over. ' + matrix[row][1] + ' has won.'
                    break
        return winner

    # INTELLIGENCE OPERATIONS

    def view_active_players(self, matrix):
        active = []
        for row in range(len(matrix)):
            if matrix[row][1] != '*':
                active.append(matrix[row][1])
        return active

def main():
    sys.stderr.write("\x1b[2J\x1b[H")
    print 'GAME IDENTIFIER TERMINAL'
    print ''
    master_directory = '/Users/dbordeleau/Desktop/Assassin/Games'
    print 'Existing games: ' + str(os.listdir(master_directory))

    game_name = raw_input('Identify an existing game or type the name of new one: ')
    folder_path = '/Users/dbordeleau/Desktop/Assassin/Games/' + game_name
    file_path = '/Users/dbordeleau/Desktop/Assassin/Games/' + game_name + '/' + game_name + '.txt'

    game = Assassin(folder_path, file_path)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        open(file_path, 'w')

        player_count = int(raw_input('Number of players in ' + game_name + ': '))
        game.make_matrix(player_count)

    matrix = game.load_matrix()
    sys.stderr.write("\x1b[2J\x1b[H")

    if not game.winner(matrix):
        print 'GAME OPERATIONS TERMINAL'
        print ''

        while True:
            print '*** BASIC OPERATIONS ***'
            print 'View existing assignment:'
            print "1. View target"
            print "2. View hitman"
            print ''
            print 'Alter assignment or status:'
            print "3. Assign target"
            print "4. Assign hitman"
            print '5. Eliminate player'
            print ''

            print '*** INTELLIGENCE OPERATIONS ***'
            print '6. View active players'
            print ''

            print '*** SYSTEM OPERATIONS ***'
            print '00. Exit program'
            print ''

            print ''

            operation = str(raw_input('Function number: '))
            sys.stderr.write("\x1b[2J\x1b[H")

            if operation == '1':
                player = str(raw_input('Player: '))
                if game.player_exists(matrix, player, 1):
                    print game.view_target(matrix, player)
                    time.sleep(1.5)
                    sys.stderr.write("\x1b[2J\x1b[H")
                else:
                    print player + ' is not in game'
                    time.sleep(1.5)
                    sys.stderr.write("\x1b[2J\x1b[H")

            if operation == '2':
                player = str(raw_input('Player: '))
                if game.player_exists(matrix, player, 1):
                    print game.view_hitman(matrix, player)
                    time.sleep(1.5)
                    sys.stderr.write("\x1b[2J\x1b[H")
                else:
                    print player + ' is not in game'
                    time.sleep(1.5)
                    sys.stderr.write("\x1b[2J\x1b[H")

            if operation == '3':
                player = str(raw_input('Player: '))
                target = str(raw_input('Target: '))
                if game.player_exists(matrix, player, 1) and game.player_exists(matrix, target, 1):
                    game.assign_target(matrix, player, target)
                    game.save_matrix(matrix)
                else:
                    print 'Either ' + player + ' or ' + target + ' is not in the game'
                    time.sleep(1.5)
                    sys.stderr.write("\x1b[2J\x1b[H")

            if operation == '4':
                player = str(raw_input('Player: '))
                hitman = str(raw_input('Hitman: '))
                if game.player_exists(matrix, player, 1) and game.player_exists(matrix, hitman, 1):
                    game.assign_hitman(matrix, player, hitman)
                    game.save_matrix(matrix)
                else:
                    print 'Either ' + player + ' or ' + hitman + ' is not in the game'
                    time.sleep(1.5)
                    sys.stderr.write("\x1b[2J\x1b[H")

            if operation == '5':
                player = str(raw_input('Player: '))
                hitman = str(raw_input('Hitman: '))
                if game.player_exists(matrix, player, 1) and game.player_exists(matrix, hitman, 1):
                    game.eliminate_player(matrix, player, hitman)
                    game.save_matrix(matrix)
                else:
                    print 'Either ' + player + ' or ' + hitman + ' is not in the game'
                    time.sleep(1.5)
                    sys.stderr.write("\x1b[2J\x1b[H")

            if operation == '6':
                print game.view_active_players(matrix)
                time.sleep(5)
                sys.stderr.write("\x1b[2J\x1b[H")

            if operation == '00':
                sys.stderr.write("\x1b[2J\x1b[H")
                break

main()
