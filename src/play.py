from copy import *
from random import *
from decimal import *
from MancalaBoard import *

Constant = 9999

class players: #define different types of players

    #each type of players are represented by a integer
    RANDOM = 0
    MINIMAX = 1
    ABPRUNE = 2
    HUMAN = 3
    
    def __init__(self, playersno, playerstp, ifplay=0):
        #define initials for player number (1 or 2) and tp (0, 1, 2 or 3) and set if play to be 0 for a game

        self.no = playersno
        self.oppo = 2 - playersno + 1
        self.tp = playerstp
        self.ifplay = ifplay

    def __repre__(self):
        #represents players
        return str(self.no)

    def minimaxplays(self, board, ifplay):
        #define how minimax plays showing its moves and scores
        move = -1
        score = -Constant
        turn = self
        for m in board.legalMoves(self):
            #if a legal move is made then game goes on
            if ifplay == 0:
                #return evaluation function
                return (self.score(board), m)
             #if no moves can be made then game is over   
            if board.gameOver():
                return (-1, -1)
            nb = deepcopy(board)
            #new board made
            nb.makeMove(self, m)
            #try moves
            oppo = players(self.oppo, self.tp, self.ifplay)
            #opponent plays min value
            s = oppo.minval(nb, ifplay-1, turn)
            #show the opponent's move
            print ('move: {} score : {}'.format(m, s))
            #if it is a better move with higher score, save the move
            if s > score:
                move = m
                score = s
        #return the best score and move 
        return score, move

    def maxval(self, board, ifplay, turn):
        #Calculates the minimax value for the next move at a state
        if board.gameOver():
            return turn.score(board)
        score = -Constant
        for m in board.legalMoves(self):
            if ifplay == 0:
                #if a game is playing show score
                return turn.score(board)
            # define opponent
            opponent = players(self.oppo, self.tp, self.ifplay)
            # Copy the board
            copyboard = deepcopy(board)
            copyboard.makeMove(self, m)
            s = opponent.minval(copyboard, ifplay-1, turn)
            #show score
            if s > score:
                score = s
        return score
    
    def minval(self, board, ifplay, turn):
        #Calculates the minimax value for the next move at a state
        #if a game is over, return  score
        if board.gameOver():
            return turn.score(board)
        score = Constant
        #if there are more moves available, a game can go on
        for m in board.legalMoves(self):
            if ifplay == 0:
                #show score
                return turn.score(board)
            # define opponent
            opponent = players(self.oppo, self.tp, self.ifplay)
            # Copy the board
            copyboard = deepcopy(board)
            copyboard.makeMove(self, m)
            #opponent plays max value
            s = opponent.maxval(copyboard, ifplay-1, turn)
            #show score
            if s < score:
                score = s
        return score
   
    def score(self, board):
        #Define scores at a state for a player
        #Winner gets 100
        if board.hasWon(self.no):
            return 100.0
        #Loser gets 0
        elif board.hasWon(self.oppo):
            return 0.0
        #Tie gets 50
        else:
            return 50.0


    def abpruneplays(self, board, ifplay):
        #define how minimax with alphabeta pruning plays showing its moves and scores
        move = -1
        alpha = -Constant
        beta  = Constant
        score = -Constant
        turn = self
        #for any legal moves, game goes on
        for m in board.legalMoves(self):
            if ifplay == 0:
                #return evaluation function
                return (self.score(board), m)
            # if no more available moves, game is over
            if board.gameOver():
                return (-1, -1)
            #copy the board
            nb = deepcopy(board) 
            #make a new board
            nb.makeMove(self, m) 
            #test the move on copied board to see how oppoonent would play
            opponent = players(self.oppo, self.tp, self.ifplay)
            s = opponent.minabprune(nb, ifplay-1, turn, alpha, beta)
            #if it is a better move with higher score, save the move
            if s > score:
                move = m
                score = s
            alpha = max(score, alpha)
        #return best score and move
        return score, move

    def minabprune(self, state, ifplay, turn, alpha, beta):
        #Find the ABpruning value for the next move at a state
        #check if game is over
        if state.gameOver():
            return turn.score(state)
        score = Constant
        #create opponent player
        opponent = players(self.oppo, self.tp, self.ifplay)
        #loop through possible legal moves for a given state
        for m in state.legalMoves(self):
            if ifplay == 0:
                return turn.score(state)
            #copy board
            copyboard = deepcopy(state)
            #test move to see score
            copyboard.makeMove(self, m)
            score = min(score, opponent.maxabprune(copyboard, ifplay-1, turn, alpha, beta))
            #prune if score is smaller than alpha
            if score <= alpha:
                return score
            else:
                beta = min(beta, score)
        return score

    def maxabprune(self, state, ifplay, turn, alpha, beta):
        #Find the ABpruning value for the next move at a state
        #check if game is over
        if state.gameOver():
            return turn.score(state)
        score = -Constant
        #create opponent player
        opponent = players(self.oppo, self.tp, self.ifplay)
        #loop through possible legal moves for a given state
        for m in state.legalMoves(self):
            if ifplay == 0:
                return turn.score(state)
            #copy board
            copyboard = deepcopy(state)
            #test move to see score
            copyboard.makeMove(self, m)   
            score = max(score, opponent.minabprune(copyboard, ifplay-1, turn, alpha, beta))
            #prune if score is larger than beta
            if score >= beta:
                return score
            else:
                alpha = max(alpha, score)
        return score

    def selectmoves(self, board):
        #select the next move
        #for a human player, input moves
        if self.tp == self.HUMAN:
            move = input('Please enter your move:')
            while not board.legalMove(self, move):
                print (move, 'is not valid')
                move = input( 'Please enter your move' )
            return move
        #for a random player, select moves from all legal moves randomly
        elif self.tp == self.RANDOM:
            move = choice(board.legalMoves(self))
            print ('Random player chose move', move)
            return move
        #for a minimax player, select moves by the minimax rules
        elif self.tp == self.MINIMAX:
            val, move = self.minimaxplays(board, self.ifplay)
            print ('Minimax player chose move', move)
            return move
        #for a abpruning player, select moves by the rule of minimax with abpruning
        elif self.tp == self.ABPRUNE:
            val, move = self.abpruneplays(board, self.ifplay)
            print ('Abpruning player chose move', move)
            return move
        #if player is not defined, let user know
        else:
            print ('Unknown player type')
            return -1



class play(players):
    
    def score(self, board):
        #define evaluation function to assess potential moves
        
        #sets variable for total stones for player 1 and 2, and the total on the board
        players1stones = sum(board.P1pits)
        players2stones = sum(board.P2pits)
        total_stones = players1stones + players2stones

        #for player one
        if self.no == 1:           
            #if stores are not empty, calculate percent of the stones that is players 1's store out of the total
            if board.stores[0]+ board.stores[1] != 0:
                store_percent = (float(board.stores[0])/float(board.stores[0]+ board.stores[1]))*100
            else:
                store_percent = 0
            
            #if the board is not empty
            if total_stones != 0:
                #calculate percent of remaining stones on player 1's side
                boardpits_percent = (float(players1stones)/float(total_stones))*100
            else:
                boardpits_percent = 0

            #calculate total score accounting both factors
            total_score = store_percent * .5 + boardpits_percent * .5 
            return total_score

        #for player two
        elif self.no == 2:
            #if stores are not empty, calculate percent of the stones that is players 2's store out of the total
            if board.stores[0]+ board.stores[1] != 0:
                store_percent = (float(board.stores[1])/float(board.stores[0]+ board.stores[1]))*100
            else:
                store_percent = 0
            
            #if the board is not empty
            if total_stones != 0:
                #calculate percent of remaining stones on player 1's side
                boardpits_percent = (float(players2stones)/float(total_stones))*100
            else:
                boardpits_percent = 0
            
            #calculate total score accounting both factors
            total_score = store_percent * .5 + boardpits_percent * .5
            return total_score
