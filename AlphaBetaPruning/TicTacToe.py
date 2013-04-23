"""
Alpha-beta pruning algorithm to play a game of TicTacToe.

Takes input file that describes a generalized version of TicTacToe.
The input file contains the number of total nodes in the game, and all winning paths.

Players take turns playing the game on n nodes, with players taking turns to cla
im nodes.  If a player completes a winning path, as described in the input file, that player wins the game.

The input file should consist of the number of nodes on the first line.  Each following line will have a list of nodes, delimited by spaces, each representing a winning path. The example of regular TicTacToe is provided.
"""
import sys
import sets

#constants
infinity = sys.maxint
negative_infinity = -sys.maxint - 1


#reads file from argv[1]
#returns number of nodes, and a set of all objective paths 
def parse_file():
    if len(sys.argv) < 2:
        print "Error: no input"
        exit()
    f = open(sys.argv[1],'r')
    node_count = int(f.readline())
    paths = []
    for ln in f.readlines():
        paths.append(sets.ImmutableSet(map(int,ln.split())))
    return node_count, paths


"""
board states should be 3-tuples, each tuple containing a list of values
s[0] = unplayed moves
s[1] = spots player 1 has taken
s[2] = spots player 2 has taken

player variable is 0 or 1, so need to +1 to access player_i's moves

We use alpha-beta pruning, with the heuristic measuring only whether the game has been won, lost, or tied for player 0.  The 

"""

#maximize, meant for player 1
def alphabeta_max(alpha,beta,s,node_count,terminals,player):
    if len(s[0]) == 0:
        return 0,s
    v = negative_infinity
    best_child = None
    for child in [(s[0][0:i]+s[0][i+1:],s[1]+[ s[0][i] ],s[2]) for i in xrange( len(s[0]) )] : #for each possible moves player 1 can make
        if( in_terminal(child,terminals,player) ):
            return 1,child
        u,_ = alphabeta_min(alpha,beta,child,node_count,terminals,1-player)
        if(v <= u):
            v=u
            best_child = child
        if(v > beta):
            return v,best_child
        alpha = max(alpha,v)
    return v,best_child

#minmize function, meant for player 2
def alphabeta_min(alpha,beta,s,node_count,terminals,player):
    if len(s[0]) == 0:
        return 0,s
    v = infinity
    best_child = None
    for child in [ (s[0][0:i]+s[0][i+1:], s[1], s[2]+[s[0][i]]) for i in xrange(len(s[0])) ] : #for each possible moves player 1 can make
        if( in_terminal(child,terminals,player) ):
            return -1,child
        u,_ = alphabeta_max(alpha,beta,child,node_count,terminals,1-player)
        if v >= u:
            best_child = child
            v = u
        if(v < alpha):
            return v,best_child
        beta = min(beta,v)
    return v,best_child

#check whether player has won on the board s 
def in_terminal(s,terminals,player):
    if any( all(move in s[player+1] for move in path ) for path in terminals ):
        return True
    else:
        return False

#updates state with player making move
def commit_move(state,player,move):
    state[0].remove(move)
    state[player+1].append(move)
    return state

#prints board
def print_board(state,node_count):
    for i in range(1,node_count+1):
        if i in state[0]:
            sys.stdout.write(str(i))
        if i in state[1]:
            sys.stdout.write('O')
        if i in state[2]:
            sys.stdout.write('X')
        if i % 3 == 0:
            print ""
        else:
            sys.stdout.write("|")
    print ""

#The game itself
def game():
    #intialize things
    node_count, paths = parse_file() #paths = terminal paths
    s = (range(1,node_count+1),[],[]) #s is the state of the board
    player = 1 #player 2, AI starts

    print_board(s,node_count)    
    #play until no moves are left, or someone wins
    while(len(s[0])>0):
        if player == 0: #human player
            move = raw_input("Please make a move:")
            try: 
                move = int(move)
                s = commit_move(s,player,move)
            except:
                print "Error: Try again"
                continue            
        elif player == 1: #AI player
            _,best_move = alphabeta_min(negative_infinity,infinity,s,node_count,paths,1) 
            s = best_move
        print_board(s,node_count)
        if in_terminal(s,paths,player):
            print "Player " + str(player+1) + " Wins!"
            exit()
        player = 1-player                    
    print "It's a tie!"


if __name__=="__main__":
    game()
