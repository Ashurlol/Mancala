from tkinter import *
from MancalaBoard import *
from play import *
import datetime

class MancalaWindow:
    """# A very simple GUI for playing the game of Mancala."""

    def __init__(self, master, p1, p2):
        self.CUPW = 75
        self.HEIGHT = 200
        self.BOARDW = 400
        self.PAD = 0
        self.game = MancalaBoard()
        self.p1 = p1
        self.p2 = p2
        self.BINW = self.BOARDW / self.game.Npits

        self.turn = p1
        self.wait = p2
        self.root = master
        
        frame = Frame(master)
        frame.pack()

        # Create the board
        self.makeBoard( frame )
        
        displayStr = "Welcome to Mancala"
            
        self.status = Label(frame, text=displayStr)
        self.status.pack(side=BOTTOM)
        
    def enableBoard(self):
        """ Allow a human player to make moves by clicking"""
        for i in [0, 1]:
            for j in range(self.game.Npits):
                self.pits[i][j].bind("<Button-1>", self.callback)

    def disableBoard(self):
        """ Prevent the human player from clicking while the computer thinks"""
        for i in [0, 1]:
            for j in range(self.game.Npits):
                self.pits[i][j].unbind("<Button-1>")

    def makeBoard( self, frame ):
        """ Create the board """
        boardFrame = Frame(frame)
        boardFrame.pack(side=TOP)

        self.button = Button(frame, text="Start New Game", command=self.newgame)
        self.button.pack(side=BOTTOM)

        gamef = Frame(boardFrame)
        topRow = Frame(gamef)
        bottomRow = Frame(gamef)
        topRow.pack(side=TOP)
        bottomRow.pack(side=TOP)
        tmppits = []
        tmppits2 = []

        binW = self.BOARDW/self.game.Npits
        binH = self.HEIGHT/2

        for i in range(self.game.Npits):
            c = Canvas(bottomRow, width=binW, height=binH)
            c.pack(side=LEFT)
            tmppits += [c]
            c = Canvas(topRow, width=binW, height=binH)
            c.pack(side=LEFT)
            tmppits2 += [c]

        self.pits = [tmppits, tmppits2]
        self.p1pit = Canvas(boardFrame, width=self.CUPW, height=self.HEIGHT)
        self.p2pit = Canvas(boardFrame, width=self.CUPW, height=self.HEIGHT)

        self.p2pit.pack(side=LEFT)
        gamef.pack(side=LEFT)
        self.p1pit.pack(side=LEFT)

        self.drawBoard()


    def drawBoard( self ):
        """ Draw the board on the canvas """
        self.p2pit.create_oval(self.PAD, self.PAD, self.CUPW, 0.9*self.HEIGHT, width=2 )
        binW = self.BOARDW/self.game.Npits
        binH = self.HEIGHT/2
        for j in [0, 1]:
            for i in range(self.game.Npits):
                
                self.pits[j][i].create_rectangle(self.PAD, self.PAD, binW, binH)
        self.p1pit.create_oval(self.PAD, self.PAD+0.1*self.HEIGHT, self.CUPW, self.HEIGHT, width=2 )
        

    def newgame(self):
        """ Start a new game between the players """
        self.game.reset()
        print ('current time is', datetime.datetime.now().time())
        self.turn = self.p1
        self.wait = self.p2
        s = "player " + str(self.turn.no) + "'s turn"
        if self.turn.tp != players.HUMAN:
            s += " Please wait..."
        self.status['text'] = s
        self.resetStones()
        self.continueGame()

    # Board must be disabled to call continueGame
    def continueGame( self ):
        """ Find out what to do next.  If the game is over, report who
            won.  If it's a human players's turn, enable the board for
            a click.  If it's a computer players's turn, choose the next move."""
        self.root.update()
        if self.game.gameOver():
            if self.game.hasWon(self.p1.no):
                self.status['text'] = "player " + str(self.p1.no) + " wins"
                print("player " + str(self.p1.no) + " wins")
                print ('current time is', datetime.datetime.now().time())
            elif self.game.hasWon(self.p2.no):
                self.status['text'] = "player " + str(self.p2.no) + " wins"
                print("player " + str(self.p2.no) + " wins")
                print ('current time is', datetime.datetime.now().time())
            else:
                self.status['text'] = "Draw"
                print('Draw')
                print ('current time is', datetime.datetime.now().time())
            return
        if self.turn.tp == players.HUMAN:
            self.enableBoard()
        else:
            move = self.turn.selectmoves( self.game )
            playAgain = self.game.makeMove( self.turn, move )
            if not playAgain:
                self.swapTurns()
            self.resetStones()
            self.continueGame()

    def swapTurns( self ):
        """ Change whose turn it is"""
        temp = self.turn
        self.turn = self.wait
        self.wait = temp
        statusstr = "player " + str(self.turn.no) + "\'s turn "
        if self.turn.tp != players.HUMAN:
            statusstr += "Please wait..."
        self.status['text'] = statusstr
        
        
    def resetStones(self):
        """ Clear the stones and redraw them """
        # Put the stones in the pits
        for i in range(len(self.game.P2pits)):
            index = (len(self.game.P2pits)-i)-1
            self.clearCup(self.pits[1][index])
            # put the nober of stones at the top of the canvas
            self.pits[1][index].create_text(self.BINW/2, 0.05*self.HEIGHT, text=str(self.game.P2pits[i]), tag="no")
        for i in range(len(self.game.P1pits)):
            # put the nober of stones at the bottom of the canvas
            self.clearCup(self.pits[0][i])
            self.pits[0][i].create_text(self.BINW/2, 0.05*self.HEIGHT, text=str(self.game.P1pits[i]), tag="no")
        self.clearCup(self.p1pit)
        self.clearCup(self.p2pit)
        self.p2pit.create_text(self.CUPW/2, 10, text=str(self.game.stores[1]), tag="no")
        self.p1pit.create_text(self.CUPW/2, 10+0.1*self.HEIGHT, text=str(self.game.stores[0]), tag="no")
        
    
    def clearCup( self, cup ):
        """ Clear the stones in the given cup"""
        titems = cup.find_withtag("no")
        stones = cup.find_withtag("stone")
        cup.delete(titems)
        cup.delete(stones)
            

    def callback(self, event):
        """ Handle the human player's move"""
        # calculate which box the click was in
        moveAgain = True
        self.disableBoard()
        if self.turn.no == 1:
            for i in range(len(self.pits[0])):
                if self.pits[0][i] == event.widget:
                    if self.game.legalMove( self.turn, i+1 ):
                        moveAgain = self.game.makeMove( self.turn, i+1 )
                        if not moveAgain:
                            self.swapTurns()
                        self.resetStones()
        else:
            for i in range(len(self.pits[1])):
                if self.pits[1][i] == event.widget:
                    index = self.game.Npits - i
                    if self.game.legalMove( self.turn, index ):
                        moveAgain = self.game.makeMove( self.turn, index )
                        if not moveAgain:
                            self.swapTurns()
                        self.resetStones()
        if moveAgain:
            self.enableBoard()
        else:
            self.continueGame()
        

def startGame(p1, p2):
    """ Start the game of Mancala with two players """
    root = Tk()

    app = MancalaWindow(root, p1, p2)

    root.mainloop()

print('Please select player type with corresponding integers',
     'RANDOM = 0, MINIMAX = 1, ABPRUNE = 2, HUMAN = 3')

player1 = int(input('Please input player 1 type  '))

player2 = int(input('Please input player 2 type  '))

startGame(players(1, player1), players(2, player2))