import random as r
from time import sleep

# Board starts empty
board = {i: ' ' for i in range(1, 10)}
# Information board
boardI = {i: str(i) for i in range(1, 10)}

width = 3  # board width

boardMM = (set(), set(), width)


def draw_board(b):
    print('', b[1], '|', b[2], '|', b[3],
          '\n-----------\n',
          '', b[4], '|', b[5], '|', b[6],
          '\n-----------\n',
          '', b[7], '|', b[8], '|', b[9],
          '\n')


def available(space):
    """
    Checks if space is available
    """
    if board[space] == ' ':
        return True

    return False


def valid(space):
    """
    Checks if space is available
    """
    if 0 < space < 10:
        return True

    return False


def draw_move(space, symbol, b):
    """
    Draw symbol in space of board b
    """
    board[space] = symbol


def end_game():
    for row in range(1, 10, 3):
        if not available(row):
            if board[row] == board[row + 1] and board[row] == board[row + 2]:
                return True
    for column in range(1, 4):
        if not available(column):
            if board[column] == board[column + 3] and board[column] == board[column + 6]:
                return True
    for diagonal in range(1, 10, 2):
        if not available(diagonal):
            if (diagonal == 1 and board[diagonal] == board[diagonal + 4]
                    and board[diagonal] == board[diagonal + 8]):
                return True
            elif (diagonal == 3 and board[diagonal] == board[diagonal + 2]
                  and board[diagonal] == board[diagonal + 4]):
                return True
    # if board.values().count('X') + board.values().count('O') == 9:
    if list(board.values()).count('X') + list(board.values()).count('O') == 9:
        return 'Tie'


def printInfo():
    print("This is the tic tac toe game in a 3x3 board.")
    draw_board(boardI)
    print("You have to give a number between 1-9, if available in the board.")


def user_turn(symbol):
    while True:
        move = int(
            input('Where would you like to move? (Enter an available place from 1-9): '))
        if valid(move):
            if not available(move):
                draw_board(boardI)
                continue
            else:
                board[move] = symbol
                return move


def computer_turn(symbol, move):
    while True:
        if available(move):
            board[move] = symbol
            return
        move = r.randint(1, 9)


def switch_turn(i):
    return not i


def two_players():
    printInfo()
    symbol = ['X', 'O']
    i = 0
    while True:
        draw_board(board)
        user_turn(symbol[i])
        if end_game() == 'Tie':
            draw_board(board)
            print("The game is a tie.")
            return
        elif end_game():
            draw_board(board)
            print(symbol[i] + " is the winner.")
            return

        i = switch_turn(i)


def one_playerR():
    printInfo()
    symbol = ['X', 'O']
    i = 0
    while True:
        draw_board(board)

        if symbol[i] == 'X':
            computer_turn(symbol[i], r.randint(1, 9))
        else:
            user_turn(symbol[i])

        if end_game() == 'Tie':
            draw_board(board)
            print("The game is a tie.")
            return
        elif end_game():
            draw_board(board)
            print(symbol[i] + " is the winner.")
            return

        i = switch_turn(i)


def checkWinner(board):
    """Return 'X' if X won in the given board, 'O' if O won, None if the game
    ended with a tie, False if the game didn't end yet, and raise an exception
    if it looks like X and O won both (the board cannot be reached using a
    legal game)."""
    x_squares, o_squares, width = board
    rows = [{width * row + col + 1 for col in range(width)} for row in range(width)]
    cols = [{width * row + col + 1 for row in range(width)} for col in range(width)]
    diagonals = [{width * i + i + 1 for i in range(width)},
                 {width * i + width - i for i in range(width)}]
    lines = rows + cols + diagonals

    x_won = any(line.issubset(x_squares) for line in lines)
    o_won = any(line.issubset(o_squares) for line in lines)
    if x_won:
        if o_won:
            raise ValueError("Illegal board")
        return 'X'
    if o_won:
        return 'O'
    if x_squares | o_squares == set(range(1, width ** 2 + 1)):
        # Nobody won, but the board is full
        return None  # Tie
    return False


def minimax_player(board, turn):
    """Return a square where it's worthwhile to play according to the minimax
    algorithm."""
    return minimax_best_square(board, turn)[0]


def minimax_score_board(board, turn, rand):
    """Return 1, 0 or -1 according to the minimax algorithm -- 1 if the player
    that has the given turn has a winning strategy, 0 if he doesn't have a
    winning strategy but he has a tie strategy, and -1 if he will lose anyway
    (assuming his opponent is playing a perfect game)."""
    if checkWinner(board) == turn:
        return 1
    if checkWinner(board) is None:
        return 0
    if checkWinner(board):
        return -1
    if rand:
        return minimax_best_squareRand(board, turn)[1]
    return minimax_best_square(board, turn)[1]


def minimax_best_square(board, turn):
    """Choose a square where it's worthwhile to play in the given board and
    turn, and return a tuple of the square's number and it's score according
    to the minimax algorithm."""
    x_squares, o_squares, width = board
    max_score = -2
    opponent = list({'X', 'O'} - set([turn]))[0]
    squares = list(set(range(1, width ** 2 + 1)) - (x_squares | o_squares))
    # r.shuffle(squares)
    for square in squares:
        # Iterate over the blank squares, to get the best square to play
        new_board = (x_squares | set([square] if turn == 'X' else []),) + \
                    (o_squares | set([square] if turn == 'O' else []), width)
        print(new_board)
        score = -minimax_score_board(new_board, opponent, False)
        print(score)
        if score == 1:
            return square, 1
        if score > max_score:
            max_score, max_square = score, square
    return max_square, max_score


# ---------------Random-----------------------

def minimax_best_squareRand(board, turn):
    """Choose a square where it's worthwhile to play in the given board and
    turn, and return a tuple of the square's number and it's score according
    to the minimax algorithm."""
    x_squares, o_squares, width = board
    max_score = -2
    max_square = None
    # EXPLICACION TALLER: Creamos un diccionario para guardar los hijos como clave y la puntuacion como el valor
    hijos = {}
    opponent = list({'X', 'O'} - set([turn]))[0]
    squares = list(set(range(1, width ** 2 + 1)) - (x_squares | o_squares))
    r.shuffle(squares)
    for square in squares:
        # Iterate over the blank squares, to get the best square to play
        new_board = (x_squares | set([square] if turn == 'X' else []),) + \
                    (o_squares | set([square] if turn == 'O' else []), width)
        #Nuevo parametro para saber si es rand o no
        score = -minimax_score_board(new_board, opponent, True)
        # EXPLICACION TALLER: Agregamos el hijo con su puntuacion al diccionario
        hijos[square] = score
        # EXPLICACION TALLER: Sacamos un movimiento aleatorio de los hijos con el r.choice()
        rmax = r.choice(squares)
        if score == 1:
            # EXPLICACION TALLER: Retornamos el movimiento aleatorio que sacamos previamente
            max_score, max_square = score, square
            return (rmax, score)
        if score > max_score:
            max_score, max_square = score, square
    # EXPLICACION TALLER: Imprimimos los valores para validar que sea aleatorio
    print('Hijos y su valor: ', hijos)
    print('Hijos: ', squares)
    print('mejor movimiento:', max_square)
    print('movimiento aleatorio', rmax)
    # EXPLICACION TALLER: Retornamos el movimiento aleatorio que sacamos previamente
    return rmax, max_score


def minimax_playerRand(board, turn):
    """Return a square where it's worthwhile to play according to the minimax
    algorithm."""
    return minimax_best_squareRand(board, turn)[0]


def one_playerMM():
    printInfo()
    symbol = ['X', 'O']
    i = 0
    while True:
        draw_board(board)

        if symbol[i] == 'O':
            move = minimax_player(boardMM, 'O')
            computer_turn(symbol[i], move)
            boardMM[1].add(move)
        else:
            move = user_turn(symbol[i])
            boardMM[0].add(move)

        print(boardMM)

        if end_game() == 'Tie':
            draw_board(board)
            print("The game is a tie.")
            return
        elif end_game():
            draw_board(board)
            print(symbol[i] + " is the winner.")
            return

        i = switch_turn(i)


# EXPLICACION TALLER: Funcion para que la computadora juegue con si misma
def computerAlone():
    printInfo()
    symbol = ['X', 'O']
    i = 0
    while True:
        draw_board(board)
        sleep(0.2)
        # EXPLICACION TALLER: Sin importar quien tenga el turno siempre se llama a la funcion para el turno de la
        # computadora
        if symbol[i] == 'X':
            move = minimax_player(boardMM, 'X')
            computer_turn(symbol[i], move)
            # EXPLICACION TALLER: Guardamos el movimiento
            boardMM[0].add(move)
        else:
            move = minimax_player(boardMM, 'O')
            computer_turn(symbol[i], move)
            # EXPLICACION TALLER: Guardamos el movimiento
            boardMM[1].add(move)

        if end_game() == 'Tie':
            draw_board(board)
            print("The game is a tie.")
            return
        elif end_game():
            draw_board(board)
            print(symbol[i] + " is the winner.")
            return

        i = switch_turn(i)


# EXPLICACION TALLER: Funcion para que la computadora juegue con si misma de manera randomica
def computerAloneRandom():
    printInfo()
    symbol = ['X', 'O']
    i = 0
    while True:
        draw_board(board)
        sleep(0.2)
        if symbol[i] == 'X':
            move = minimax_playerRand(boardMM, 'X')
            computer_turn(symbol[i], move)
            boardMM[0].add(move)
        else:
            move = minimax_playerRand(boardMM, 'O')
            computer_turn(symbol[i], move)
            boardMM[1].add(move)

        if end_game() == 'Tie':
            draw_board(board)
            print("The game is a tie.")
            return
        elif end_game():
            draw_board(board)
            print(symbol[i] + " is the winner.")
            return

        i = switch_turn(i)


computerAlone()
