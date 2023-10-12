import tkinter as tk
from functools import partial
from random import randint

logfile = open('logs.txt', 'w')

class GameInfo:
    '''Used for the logic of the game'''
    def __init__(self, length, width):

        #In advanced mode the board is 16x16 and there are 40 mines
        self.length = length
        self.width = width
        self.numberOfMines = 99
        
        self.mines = []
        self.uncoveredCells = []
        self.moves = 0


    def setupMines(self):
        self.mines = []
        #Create mines
        for i in range(self.numberOfMines):
            x = randint(0, self.length - 1)
            y = randint(0, self.width - 1)
            while (x, y) in self.mines:
                x = randint(0, self.length - 1)
                y = randint(0, self.width - 1)
            self.mines.append((x, y))


    def addUncoveredCell(self, coordinate):
        self.uncoveredCells.append(coordinate)

    def isUncoveredCell(self, coordinate):
        if coordinate in self.uncoveredCells:
            return True
        return False
    
    def isMine(self, coordinate):
        if coordinate in self.mines:
            return True
        return False

    def getNeighbours(self, coordinate):

        ##################################
        # (x-1, y+1) (x, y+1) (x+1, y+1) #
        # (x-1, y)   (x, y)   (x+1, y)   #
        # (x-1, y-1) (x, y-1) (x+1, y-1) #
        ##################################

        x, y = coordinate

        neighbours = [(x - 1, y + 1), (x, y + 1), (x + 1, y + 1), (x - 1, y), (x + 1, y), (x - 1, y - 1), (x, y - 1), (x + 1, y - 1)]

        total = 0
        for neighbor in neighbours:
            if self.isMine(neighbor):
                total += 1

        return total
    
    def isEmpty(self, coordinate):
        if (self.getNeighbours(coordinate) == 0):
            return True
        return False

class Board:
    '''Used for the GUI'''
    def __init__(self, length, width):
        self.cells = {}
        self.master = tk.Tk()
        for x in range(length):
            for y in range(width):
                self.cells[(x, y)] = None
                self.cells[(x, y)] = tk.Button(self.master, text=" ", bg="white", command=partial(self.click, (x, y)))
                self.cells[(x, y)].grid(row=x, column=y)
                self.cells[(x, y)].coordinate = (x, y)

        self.gameInfo = GameInfo(length, width)
        self.gameInfo.setupMines()
        self.master.mainloop()

    def firstClick(self, cell):
        print(str(cell), file=logfile)

        while not (self.gameInfo.isEmpty(cell)):
            self.gameInfo.setupMines()

        return


    def click(self, cell):
        if (self.gameInfo.uncoveredCells == []):
            self.firstClick(cell)

        x, y = cell
        if (x == -1 or x == self.gameInfo.length or y == -1 or y == self.gameInfo.width):
            return
        cell = self.cells[cell]

        if self.gameInfo.isUncoveredCell(cell.coordinate):
            return 

        self.uncover(cell)
        # TODO
        # Check if already uncovered
        # Check if the cell is a flag
        # Check if the cell is a mine
        # If not any of those:
        # Get # of neighbours -> uncover
        # recursive ---
        # if no neighbours:
        # uncover, cycle neighbors, repeat

    def uncover(self, cell):

        if self.gameInfo.isMine(cell.coordinate):
            for mine in self.gameInfo.mines:
                self.cells[mine].config(background="red")
        elif self.gameInfo.isEmpty(cell.coordinate):
            def recursive(cell):
                x, y = cell.coordinate

                if self.gameInfo.isUncoveredCell((x, y)):
                    return
                
                self.gameInfo.addUncoveredCell(cell.coordinate)

                neighbours = [(x - 1, y + 1), (x, y + 1), (x + 1, y + 1), (x - 1, y), (x + 1, y), (x - 1, y - 1), (x, y - 1), (x + 1, y - 1)]
                for neighbour in neighbours:
                    self.click(neighbour)
            cell.config(background="#cccccc")
            recursive(cell)
        else:
            cell.config(background="#cccccc", text=str(self.gameInfo.getNeighbours(cell.coordinate)))
            
        self.gameInfo.addUncoveredCell(cell.coordinate)


Board(16, 30)