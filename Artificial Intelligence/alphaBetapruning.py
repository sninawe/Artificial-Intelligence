
import copy

#n = sys.argv[1]
#Player = sys.argv[2]
#current_board = sys.argv[3]
#time = sys.argv[4]


n=8

current_board=[]
for i in range(0,64):
    current_board.append('.')


def get_board(input_board,n):
    positions=0
    board={}
    for i in range(1,(n+1)):
        for j in range(1,(n+1)):
            board[(i,j)]= input_board[positions]
            positions += 1
    return(board)

board=get_board(current_board,n)


board[(2,7)] = 'b'
board[(3,3)] = 'w'
board[(5,2)] = 'b'
board[(5,6)] = 'b'
board[(5,7)] = 'b'
board[(7,5)] = 'w'
board[(1,7)] = 'B'
board[(3,8)] = 'w'
board[(6,2)] = 'b'
board[(2,6)] = 'b'
board[(5,1)] = 'b'
board[(4,5)] = 'w'




def print_board(board):
    for dim1 in range(1,(n+1)):
        for dim2 in range(1,(n+1)):
            print board[(dim1,dim2)],
        print("\n")


#print_board(board)

def get_pieces(player):
    if player == 'w':
        return('w','W')
    elif player == 'b':
        return ('b','B')

def get_opponent(player):
    if player == 'w':
        return('b')
    elif player == 'b':
        return('w')

def get_moves(board,piece):
    player=piece[0]
    pos=piece[1]

    pos1 = pos2 = pos3 = None
    rem1 = rem2 = rem3 = None

    if board[pos] == get_pieces(player)[1]:
        steps = 0
        counter=0
        for next in range(1,(n+1-pos[1])):
            if (pos[0],pos[1]+next) in board.keys() and board[(pos[0],pos[1]+next)] in (get_pieces(get_opponent(player))):
                counter += 1
                if counter > 1:
                    break
                if (pos[0],pos[1]+next+1) in board.keys() and board[(pos[0],pos[1]+next+1)] == '.':
                    steps += 1
                    rem1 = (pos[0],pos[1]+next)
            elif board[(pos[0],pos[1]+next)] == '.':
                steps += 1
            else:
                break
        if steps != 0:
            pos1=(pos[0],pos[1]+steps)

        steps = 0
        counter=0
        for next in range(1,pos[1]):
            if (pos[0],pos[1]-next) in board.keys() and board[(pos[0],pos[1]-next)] in (get_pieces(get_opponent(player))):
                counter += 1
                if counter > 1:
                    break
                if (pos[0],pos[1]-next-1) in board.keys() and board[(pos[0],pos[1]-next-1)] == '.':
                    steps += 1
                    rem2 = (pos[0],pos[1]-next)
            elif board[(pos[0],pos[1]-next)] == '.':
                steps += 1
            else:
                break
        if steps != 0:
            pos2=(pos[0],pos[1]-steps)


        if player in get_pieces('w'):
            steps = 0
            counter=0
            for next in range(1,n+1-pos[0]):
                if (pos[0]+next,pos[1]) in board.keys() and board[(pos[0]+next,pos[1])] in (get_pieces(get_opponent(player))):
                    counter += 1
                    if counter > 1:
                        break
                    if (pos[0]+next+1,pos[1]) in board.keys() and board[(pos[0]+next+1,pos[1])] == '.':
                        steps += 1
                        rem3 = (pos[0]+next,pos[1])
                elif board[(pos[0]+next,pos[1])] == '.':
                    steps += 1
                else:
                    break
            if steps != 0:
                pos3=(pos[0]+steps,pos[1])
        else:
            steps = 0
            counter=0
            for next in range(1,pos[0]):
                if (pos[0]-next,pos[1]) in board.keys() and board[(pos[0]-next,pos[1])] in (get_pieces(get_opponent(player))):
                    counter += 1
                    if counter > 1:
                        break
                    if (pos[0]-next-1,pos[1]) in board.keys() and board[(pos[0]-next-1,pos[1])] == '.':
                        steps += 1
                        rem3 = (pos[0]-next,pos[1])
                elif board[(pos[0]-next,pos[1])] == '.':
                    steps += 1
                else:
                    break
            if steps != 0:
                pos3=(pos[0]-steps,pos[1])
        return((pos,pos1,rem1),(pos,pos2,rem2),(pos,pos3,rem3))

    else:
        if (pos[0],pos[1]+1) in board.keys() and (pos[0],pos[1]+2) in board.keys() and board[(pos[0],pos[1]+1)] in get_pieces(get_opponent(player)) and board[(pos[0],pos[1]+2)] == '.':
            pos1 = (pos[0],pos[1]+2)
            rem1= (pos[0],pos[1]+1)
        elif (pos[0],pos[1]+1)in board.keys() and board[(pos[0],pos[1]+1)] == '.':
            pos1 = (pos[0],pos[1]+1)
        if (pos[0],pos[1]-1) in board.keys() and (pos[0],pos[1]-2) in board.keys() and board[(pos[0],pos[1]-1)] in get_pieces(get_opponent(player)) and board[(pos[0],pos[1]-2)] == '.':
            pos2 = (pos[0],pos[1]-2)
            rem2 = (pos[0],pos[1]-1)
        elif (pos[0],pos[1]-1) in board.keys() and board[(pos[0],pos[1]-1)] == '.':
            pos2 = (pos[0],pos[1]-1)
        if player in get_pieces('w'):
            if (pos[0]+1,pos[1]) in board.keys() and (pos[0]+2,pos[1]) in board.keys() and board[(pos[0]+1,pos[1])] in get_pieces(get_opponent(player)) and board[(pos[0]+2,pos[1])] == '.':
                pos3 = (pos[0]+2,pos[1])
                rem3 = (pos[0]+1,pos[1])
            elif (pos[0]+1,pos[1]) in board.keys() and board[(pos[0]+1,pos[1])] == '.':
                pos3 = (pos[0]+1,pos[1])
        else:
            if (pos[0]-1,pos[1]) in board.keys() and (pos[0]-2,pos[1]) in board.keys() and board[(pos[0]-1,pos[1])] in get_pieces(get_opponent(player)) and board[(pos[0]-2,pos[1])] == '.':
                pos3 = (pos[0]-2,pos[1])
                rem3 = (pos[0]-1,pos[1])
            elif (pos[0]-1,pos[1]) in board.keys() and board[(pos[0]-1,pos[1])] == '.':
                pos3 = (pos[0]-1,pos[1])
        return((pos,pos1,rem1),(pos,pos2,rem2),(pos,pos3,rem3))




def score(board,player):
    player_score = 0
    opponent_score = 0
    player_pieces=get_pieces(player)
    opponent_pieces=get_pieces(get_opponent(player))

    for piece in board.keys():
        if board[piece] in player_pieces:
            player_score += 1
        if board[piece] in opponent_pieces:
            opponent_score += 1
    return(player_score-opponent_score)



def board_upgrade(board,move,player):
    pos=move[0]
    new_pos=move[1]
    remove=move[2]
    board[new_pos]=board[pos]
    board[pos]='.'
    if remove:
        board[remove]='.'
    for key in board.keys():
        if key[0] == 1 and board[key] == (get_pieces('b')[0]):
            board[key] = get_pieces('b')[1]
        elif key[0] == n and board[key] == (get_pieces('w')[0]):
            board[key] = get_pieces('w')[1]
    return(board)


def successors(board,player):
    pichus=[]
    for piece in board.keys():
        if board[piece] in get_pieces(player):
            pichus.append(piece)

    moves=[]
    for piece in range(0,len(pichus)):
        next_moves=get_moves(board,(player,pichus[piece]))
        for next in range(0,len(next_moves)):
            if next_moves[next][1]:
                moves.append(next_moves[next])
    return(moves)

for piece in board.keys():
    board[piece] = '.'



print_board(board)


def Is_Terminal(board):
    score1 = 0
    score2 = 0
    pieces1=get_pieces('w')
    pieces2=get_pieces('b')

    for piece in board.keys():
        if board[piece] in pieces1:
            score1 += 1
        if board[piece] in pieces2:
            score2 += 1
    return(score1 == 0 or score2 == 0)



def SortedSuccessors(board,player):
    moves = successors(board, player)

    sortedsuccessors={}
    for move in moves:
        board_temp = copy.deepcopy(board)
        sortedsuccessors[move] = score(board_upgrade(board_temp,move,player),player)


    if player == Player:
        sortedsuccessors = sorted(sortedsuccessors,key = sortedsuccessors.get, reverse=True)
    else:
        sortedsuccessors = sorted(sortedsuccessors,key = sortedsuccessors.get)
    return(sortedsuccessors)

def alphabeta(player, board, alpha, beta, depth):


    if depth == 0 or Is_Terminal(board):
        return score(board, player), None

    def value(board, alpha, beta):
        return -alphabeta(get_opponent(player), board, -beta, -alpha, depth-1)[0]


    moves = SortedSuccessors(board,player)
    if not moves:
        if not successors(board,get_opponent(player)):
            return score(board, player), None
        return value(board, alpha, beta), None

    best_move = moves[0]
    for move in moves:
        if alpha >= beta:
            break
        val = value(board_upgrade(copy.deepcopy(board),move,player), alpha, beta)
        if val > alpha:
            alpha = val
            best_move = move
    return alpha, best_move

Player='w'
strategy=alphabeta('w',copy.deepcopy(board),-999,999,5)
print_board(board_upgrade(board,strategy[1],Player))
