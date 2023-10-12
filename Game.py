from random import randint

class GameInfo:
    def __init__(self, length, width):

        #In advanced mode the board is 16x16 and there are 40 mines
        self.length = length
        self.width = width
        numberOfMines = 40
        
        self.mines = []

        #Create mines
        for i in range(numberOfMines):
            x = randint(0, self.length - 1)
            y = randint(0, self.width - 1)
            while (x, y) in self.mines:
                x = randint(0, self.length - 1)
                y = randint(0, self.width - 1)
            self.mines.append((x, y))

        print(self.mines)


GameInfo(16, 16)
            
