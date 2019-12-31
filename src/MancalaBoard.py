from random import *
from copy import *
from play import *
import datetime

class MancalaBoard:
    def __init__(self):
        #Initilize mancala board
        self.reset()
        
    def reset(self):
        #Reset the mancala board for a new game
        self.Npits = 6       # pits per side
        self.stores = [0, 0] #0 stones in a store to start with
        self.P1pits = [4]*self.Npits #4 stones in each pit to start with
        self.P2pits = [4]*self.Npits

    def __repr__(self):
        ret = "P L A Y E R  2\n"
        ret += "\t6\t5\t4\t3\t2\t1\n"
        ret += "------------------------------------------------------------\n"
        ret += str(self.stores[1]) + "\t"
        for elem in range(len(self.P2pits)-1, -1, -1):
            ret += str(self.P2pits[elem]) + "\t"
        ret += "\n\t"
        for elem in self.P1pits:
            ret += str(elem) + "\t"
        ret += str(self.stores[0])
        ret += "\n------------------------------------------------------------"
        ret += "\n\t1\t2\t3\t4\t5\t6\n"
        ret += "P L A Y E R  1\n"        
        return ret
        
    def legalMove( self, players, pit ):
        #Assess if a move is legal
        if players.no == 1:
            pits = self.P1pits
        else:
            pits = self.P2pits
        return pit > 0 and pit <= len(pits) and pits[pit-1] > 0

    def legalMoves( self, players ):
        #Returns a list of legal moves for a given player
        if players.no == 1:
            pits = self.P1pits
        else:
            pits = self.P2pits
        moves = []
        for m in range(len(pits)):
            if pits[m] != 0:
                moves += [m+1]
        return moves


    def makeMove( self, players, pit ):
        again = self.makeMoveHelp(players, pit)
        if self.gameOver():
            # clear the pits
            for i in range(len(self.P1pits)):
                self.stores[0] += self.P1pits[i]
                self.P1pits[i] = 0
            for i in range(len(self.P2pits)):
                self.stores[1] += self.P2pits[i]
                self.P2pits[i] = 0
            return False
        else:
            return again
            
    def makeMoveHelp( self, players, pit ):
        #Make a move and see if a player gets another turn
        if players.no == 1:
            pits = self.P1pits
            opppits = self.P2pits
        else:
            pits = self.P2pits
            opppits = self.P1pits
        initpits = pits
        nstones = pits[pit-1]  # Pick up stones
        pits[pit-1] = 0        # Empty that pit
        pit += 1
        playAgain = False # No extra turn
        while nstones > 0:
            playAgain = False    
            while pit <= len(pits) and nstones > 0:
                pits[pit-1] += 1
                nstones = nstones - 1
                pit += 1
            if nstones == 0:
                break    # If no more stones
            if pits == initpits:   # If we're on our own side
                self.stores[players.no-1] += 1
                nstones = nstones - 1
                playAgain = True
            # now switch sides and keep going
            temppits = pits
            pits = opppits
            opppits = temppits
            pit = 1

        if playAgain:
            return True # Gets extra turn if final stone lands in store
        
        # Check if stone ends in an empty pit on our side
        if pits == initpits and pits[pit-2] == 1:
            # Capture opposite stones 
            self.stores[players.no-1] += opppits[(self.Npits-pit)+1] 
            opppits[(self.Npits-pit)+1] = 0
            self.stores[players.no-1] += 1
            pits[pit-2] = 0
        return False # No extra turn

    def hasWon( self, playersno ):
        # Chech if a player has won
        if self.gameOver():
            opp = 2 - playersno + 1
            return self.stores[playersno-1] > self.stores[opp-1]
        else:
            return False

    def getplayersspits( self, playersno ):
        #Return the pits for a given player
        if playersno == 1:
            return self.P1pits
        else:
            return self.P2pits
        
    def gameOver(self):
        # Check if game is over
        over = True
        for elem in self.P1pits:
            if elem != 0:
                over = False
        if over:
            return True
        over = True
        for elem in self.P2pits:
            if elem != 0:
                over = False
        return over   

    def hostGame(self, players1, players2):
        # Host a game between two players
        self.reset()
        currplayers = players1 
        waitplayers = players2
        while not(self.gameOver()):
            again = True
            while again:
                print (self)
                move = currplayers.selectmoves( self )
                while not(self.legalMove(currplayers, move)):
                    print (move, " is not legal")
                    move = currplayers.selectmoves(self)
                again = self.makeMove( currplayers, move )
            temp = currplayers
            currplayers = waitplayers
            waitplayers = temp

        print (self)
        if self.hasWon(currplayers.no):
            print ("player", currplayers, " wins!")
        elif self.hasWon(waitplayers.no):
            print ("player", waitplayers, " wins!")
        else:
            print ("Draw")
        
