"""
Alpha-beta pruning algorithm to play a game of TicTacToe.

Takes input file that describes a generalized version of TicTacToe, with weighted win states.
The input file contains the number of total nodes in the game, and a series of paths with scores.  Completing a path will grant a player a number of points, dictated by the input file.

Players take turns playing the game on n nodes, with players taking turns to cla
im nodes.  If a player completes a winning path, as described in the input file, that player wins the game.

The input file should consist of the number of nodes on the first line.  Each following line will begin with a number, representing the score of that particular path, and follows with a list of nodes, delimited by spaces, each representing a winning path.
"""

import sys
import sets
import string

#constants
infinity = sys.maxint
negative_infinity = -sys.maxint - 1

#returns number of nodes, and a set of all objective paths 
def parse_file():
    if len(sys.argv) < 2:
        print "Error: no input"
        exit()
    f = open(sys.argv[1],'r')
    node_count = int(f.readline())
    scores = dict()
    paths = []
    for ln in f.readlines():
        nums = map(int,ln.split())
        p = sets.ImmutableSet(nums[1:])
        scores[p] = int(nums[0])
        paths.append( p )
    return node_count, paths, scores

"""
board state should be an n+1-tuple
The first n contain a O if player 1 has has claimed space i (resp X if player 2 claimed it) or the number of the space (i.e. i+1), 
and the last contains the number of unclaimed spaces

player variable is 0 or 1, so need to +1 to access player_i's moves

We use alpha-beta pruning.
"""

#maximize, meant for player 1
def alphabeta_max(alpha,beta,state,node_count,paths,player,depth,scores):
    #print "max",state
    if state[node_count] == 0 or depth == 0:
        p1,p2 = score_board(state,paths,scores)
        return p1 - p2,state
    v = negative_infinity
    best_child = None
    for move in [ space for space in state[:node_count] if type(space)==int  ] : #for each possible moves player 1 can make
        child = commit_move(state,player,move)
        u,_ = alphabeta_min(alpha,beta,child,node_count,paths,1-player,depth-1,scores)
        if(v <= u):
            v=u
            best_child = child
        if(v > beta):
            return v,best_child
        alpha = max(alpha,v)
    return v,best_child

#minmize function, meant for player 2
def alphabeta_min(alpha,beta,state,node_count,paths,player,depth,scores):
    #print "min"+str(state)
    if state[node_count] == 0 or depth == 0:
        p1,p2 = score_board(state,paths,scores)
        return p1 - p2,state
    v = infinity
    best_child = None
    for move in [ space for space in state[:node_count] if type(space)==int  ] : #for each possible moves player 1 can make
        child = commit_move(state,player,move)
        #print child
        u,_ = alphabeta_max(alpha,beta,child,node_count,paths,1-player,depth-1,scores)
        if v >= u:
            best_child = child
            v = u
        if(v < alpha):
            return v,best_child
        beta = min(beta,v)
    return v,best_child

#check whether player has won on the board s 
def in_terminal(state,terminals,player):
    for path in terminals:
        if all( state[ path[0] ] == state[i] for i in path ):
            return True
    return False

#get scores of both players
def score_board(state,paths,scores):
    player1_score = 0
    player2_score = 0
    for path in paths:
        if all( 'O' == state[i] for i in path ):
            player1_score+=scores[path]
    for path in paths:
        if all( 'X' == state[i] for i in path ):
            player2_score+=scores[path]
    return player1_score, player2_score

#updates state with player making move
def commit_move(state,player,move):
    if player == 0:
        state = state[:move-1] + tuple(['O']) + state[move:]
    else:
        state = state[:move-1] + tuple(['X']) + state[move:]
    state = state[:len(state)-1] + tuple([state[len(state)-1]-1])
    return state

#prints board
def print_board(state,node_count):
    for i in range(node_count):
        sys.stdout.write(str(state[i]))
        sys.stdout.write("|")
    print ""

#The game itself
def game():
    #intialize things
    node_count, paths,scores = parse_file() #paths = terminal paths
    s = tuple(range(1,node_count+1)+[node_count]) #s is the state of the board
    player = 1 #player 2, AI starts

    print_board(s,node_count)    

    #play until no moves are left, or someone wins
    while(s[node_count]>0):
        if player == 0: #human player
            move = raw_input("Please make a move:")
            try: 
                move = int(move)
                s = commit_move(s,player,move)
            except:
                print "Error: Try again"
                continue            
        elif player == 1: #AI player
            _,best_move = alphabeta_min(negative_infinity,infinity,s,node_count,paths,1,10,scores) 
            s = best_move
        print_board(s,node_count)
        player = 1-player                    

    print "Final scores:"
    p1score,p2score = score_board(s,paths,scores)
    print "Player 1: " + str(p1score)
    print "Player 2: " + str(p2score)


def main():
    #intialize variables
    node_count, paths,scores = parse_file() #paths = terminal paths
    s = tuple(range(1,node_count+1)+[node_count]) #s is the state of the board
    player = 1 #player 2, AI starts

    #play until no moves are left, or someone wins
    while(s[node_count]>0):
        if player == 0: #AI player 1
            _,best_move = alphabeta_max(negative_infinity,infinity,s,node_count,paths,0,10,scores) 
            s = best_move
            #print best_move
        elif player == 1: #AI player 2
            _,best_move = alphabeta_min(negative_infinity,infinity,s,node_count,paths,1,10,scores) 
            s = best_move
        print "Move #"+str(node_count-s[node_count])
        print_board(s,node_count)
        player = 1-player                    

    print "Final scores:"
    p1score,p2score = score_board(s,paths,scores)
    print "Player 1: " + str(p1score)
    print "Player 2: " + str(p2score)


if __name__=="__main__":
    if len(sys.argv)<3:
        game()
    elif sys.argv[2] == "game":
        game()
    elif sys.argv[2] == "auto":
        main()
    else:
        print "2nd argument must be \"game\" or \"auto\""
