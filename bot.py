HUMAN = 'x'
BOT = 'o'
KEY_SCORE = "score"
KEY_INDEXES = "indexes"



def get_move_cords(player,field):
    moves = []
    available_spots = empty_indexies(field)
    if is_winner(field,HUMAN):
        return {KEY_SCORE: -10}
    if is_winner(field,BOT):
        return {KEY_SCORE: 10}
    if len(available_spots) == 0:
        return {KEY_SCORE: 0}
    for spot in available_spots:
        move = {}
        x,y = spot
        move[KEY_INDEXES] = spot
        field[x][y] = player
        if player == BOT:
            result = get_move_cords(field, HUMAN)
        else:
            result = get_move_cords(field, BOT)
        move[KEY_SCORE] = result[KEY_SCORE]
        field[x][y] = "-"
        moves.append(move)

    best_move = None
    if player == BOT:
        best_score = -10000
        for move in moves:
            if move[KEY_SCORE] > best_score:
                best_score = move[KEY_SCORE]
                best_move = move
    else:
        best_score = 10000
        for move in moves:
            if move[KEY_SCORE] < best_score:
                best_score = move[KEY_SCORE]
                best_move = move
    return best_move


def empty_indexies(field):
    result = []
    for i in range(3):
        for j in range(3):
            if field[i][j] == '-':
                result.append((i,j))
    return result


def is_winner(field,player):
    if (
            (field[0][0] == player and field[0][1] == player and field[0][2] == player) or
            (field[1][0] == player and field[1][1] == player and field[1][2] == player) or
            (field[2][0] == player and field[2][1] == player and field[2][2] == player) or
            (field[0][0] == player and field[1][0] == player and field[2][0] == player) or
            (field[0][1] == player and field[1][1] == player and field[2][1] == player) or
            (field[0][2] == player and field[1][2] == player and field[2][2] == player) or
            (field[0][0] == player and field[1][1] == player and field[2][2] == player) or
            (field[0][2] == player and field[1][1] == player and field[2][0] == player)
    ):
        return True
    return False