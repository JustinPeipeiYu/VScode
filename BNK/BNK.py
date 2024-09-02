'''
Author: Justin Yu
Date: September 2, 2024
Purpose: Checkmate with Bishop, Knight, and King
'''
import random

####### GLOBAL VARIABLES ########
knight = "knight"
bishop = "bishop"
yourKing = "your king"
theirKing = "their king"
columnLetters = "abcdefgh"
letterDictionary = {} 
prompt = "prompt"
preset = "preset"
rand = "random"
min = 1
max = 8

######## BOARD class ########
class Board:
    def __init__(self, B1, N1, K1, K2):
        self.pieces = [B1, N1, K1, K2]
        self.occupiedSquares = []
        self.guardedSquares = []

    def updateOccupiedSquares(self):
        o = []
        for p in self.pieces:
            o.append(p.currentPosition)
        self.occupiedSquares = o
    
    def checkRandomPlacement(self):
        listOfPositions = []
        for piece in self.pieces:
            while (True):
                if piece.currentPosition not in listOfPositions:
                    listOfPositions.append(piece.currentPosition)
                    break
                else:
                    piece.currentPosition = generateRandomPoint()  

        self.getGuardedSquares()
        listOfPositions += self.guardedSquares

        while (True):
            if (self.pieces[3].currentPosition in listOfPositions):
                self.pieces[3].currentPosition = generateRandomPoint()  
            else:
                break
        self.updateOccupiedSquares()
        
    def getGuardedSquares(self):
        guardedSquares = []
        for i in range(3):
            guardedSquares = guardedSquares + self.pieces[i].validMoves
        self.guardedSquares = guardedSquares

    def printBoard(self):
        for piece in self.pieces:
            print(piece.pieceName, ": ", convertToName(piece.currentPosition))
        print("Occupied Squares", convertToName(self.occupiedSquares))
        print("Guarded Squares", convertToName(self.guardedSquares))

####### CHESS PIECE class ########
class ChessPiece:
    def __init__(self, pieceName, option, point):
        self.pieceName = pieceName
        self.option = option
        self.currentPosition = self.setPosition(point)
        self.validMoves = []
        

    def setPosition(self, point):
        repeat = True
        if (self.option == prompt):#prompt for position
            while (repeat==True):
                entry = input("What square is %s on (ie. a1)? \n"%(self.pieceName)).rstrip().lstrip().lower() #get user input using piece name and ownership
                repeat = False
                if (len(entry)!=2): #check condition 1: entry is not two characters long
                    repeat = True
                else:
                    if (entry[0] not in columnLetters): #check condition 2: 1st character is not letter a-h
                        repeat = True 
                    else:
                        try: #check condition 3: 2nd character is not integer
                            int(entry[1])
                        except:
                            repeat=True
                        if (repeat == False):
                            if (int(entry[1])>max and int(entry[1])<min):#check condition 4: 2nd character is not in range of 1-8
                                repeat=True
                if (repeat == True):#at least one condition failed, redo prompt
                    print("Sorry that is an invalid entry. Please try again.")
            return convertToPoint(entry)
        elif (self.option == preset):#preset position
            return convertToPoint(point)
        else: #generate random position
            return generateRandomPoint()
    
    def printValidMoves(self): #print all valid moves for a piece
        print(self.pieceName, "'s valid moves: ", convertToName(self.validMoves))

####### KING class #########
class King(ChessPiece):
    def __init__(self, name, option, point):
        ChessPiece.__init__(self, name, option, point)

    def getMoves(self,board):
        validMoves = []
        for i in range(-1,2):
            for j in range(-1,2):
                newPoint = [self.currentPosition[0]+i, self.currentPosition[1]+j]
                #cannot be off board, adjacent to other king, or on top of another piece
                if (not offBoard(newPoint)):
                    if (not newPoint in board.occupiedSquares):
                        if (not (adjacent(newPoint, board.pieces[-1].currentPosition) and adjacent(newPoint, board.pieces[-2].currentPosition))):
                            validMoves.append(newPoint) 
        self.validMoves = validMoves

####### YOUR KING class ##########
class YourKing(King):
    def __init__(self, option, point):
        King.__init__(self, yourKing, option, point)

####### THEIR KING class #########
class TheirKing(King):
    def __init__(self, option, point):
        King.__init__(self, theirKing, option, point)

####### KNIGHT class ########
class Knight(ChessPiece):
    def __init__(self, option, point):
        ChessPiece.__init__(self, knight, option, point)
    
    def getMoves(self, board):
        validMoves = []
        for i in range(-1,2,2):
            for j in range(-2,3,4): 
                newPoint1 = [self.currentPosition[0]+i, self.currentPosition[1]+j] 
                if (not offBoard(newPoint1)):
                    if (newPoint1 not in board.occupiedSquares):
                        validMoves.append(newPoint1)
                
                newPoint2 = [self.currentPosition[0]+j, self.currentPosition[1]+i]
                if (not offBoard(newPoint2)):
                    if (newPoint2 not in board.occupiedSquares):
                        validMoves.append(newPoint2)
        self.validMoves = validMoves
    
 ####### BISHOP class ########
class Bishop(ChessPiece):
    def __init__(self, option, point):
        ChessPiece.__init__(self, bishop, option, point)
    
    def getMoves(self, board):
        validMoves = []
        for x in range(-1,2,2):
            for y in range(-1,2,2):
                i = 1
                while(True):
                    newPoint = [self.currentPosition[0]+ x * i, self.currentPosition[1]+ y * i] 
                    if (not offBoard(newPoint)):
                        if newPoint not in board.occupiedSquares:
                            validMoves.append(newPoint)
                            i+=1
                        else:
                            break
                    else:
                        break
        
        self.validMoves = validMoves
    
###### MAIN PROGRAM FUNCTIONS ########
def offBoard(point):
    if (point[0]<min or point[0]>max or point[1]<min or point[1]>max):
        return True
    else:
        return False 
    
def generateRandomPoint():
    x = random.randint(min, max)
    y = random.randint(min, max)
    point = [x,y]
    return point

def stepsBetween(point1, point2):
    dx = abs(point1[0]-point2[0])
    dy = abs(point1[1] - point2[1])
    if (dx >= dy):
        return dx - 1
    else:
        return dy - 1

def adjacent(point1, point2):
    if (stepsBetween(point1,point2)== 0):
        return True
    else:
        return False
    
def convertToPoint(squareName):
    point = [None]*2
    point[0] = letterDictionary[squareName[0]]
    point[1] = int(squareName[1])
    return point

def convertToName(points):
    if (type(points[0])==int):
        for l in letterDictionary:
            if (letterDictionary[l]==points[0]):
                return (l + str(points[1]))
    else:
        namedPoints = []
        for p in points:
            for l in letterDictionary:
                if (letterDictionary[l]==p[0]):
                        namedPoints.append(l + str(p[1]))
        return namedPoints

def getGuardedSquares(B1, N1, K1):
    guardedSquares = []
    guardedSquares = guardedSquares + B1.validMoves + N1.validMoves + K1.validMoves
    return guardedSquares



######## MAIN PROGRAM  #######
gameOver = True
win = False

i = 1
for c in columnLetters:
    letterDictionary[c] = i
    i+=1

# randomly initializing all piece positions
B1 = Bishop(preset, "b5")
N1 = Knight(preset, "e5")
K1 = YourKing(preset, "a1") 
K2 = TheirKing(preset, "b6") 
Board1 = Board(B1, N1, K1, K2) 

#get valid moves for each piece
B1.getMoves(Board1)
N1.getMoves(Board1)
K1.getMoves(Board1)
K2.getMoves(Board1)
Board1.checkRandomPlacement()

#print board and piece properties
Board1.printBoard()
K1.printValidMoves()
B1.printValidMoves()
N1.printValidMoves()
K2.printValidMoves()




