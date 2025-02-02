#Justin Yu
#August 7, 2024
#BNK: the start of a program that can checkmate with bishop, knight, and king (the most technical endgame to execute successfully). So far, this program's purpose is to prevent the draw situation which can occur by trapping the knight in the corner and capturing it. This program instructions provides options for the user to save their knight in such situations and prevent a draw from resulting out of a garaunteed win.

#global program variables that all classes can use
knight = "knight"
bishop = "bishop"
yourKing = "your king"
theirKing = "their king"
columnLetters = "abcdefgh"
letterDictionary = {} 
moveAway = 1
moveToward = 2
defendKnight = 3
gameOver = False
win = False

# functions that are unique to a board
# update board updates the board with all the pieces (and their positions) and updates each piece with a copy of the board
# off board determines if a point falls off the board
# steps between determines the number of steps between two points
# convert to point returns the coordinate point of a name ie. a1 --> [1,1]
# convert to name returns the name of a coordinate point ie. [1,2] --> a2
# knight trapped determines whether the knight is under attack and facing capture
# light or dark determines whether a coordinate point is a light square or dark square ie. a1 --> dark
class Board:
    def __init__(self):
        self.pieces = {}
        self.recommendedMoves = {knight:[],bishop:[],yourKing:[],theirKing:[]}
        self.min = 1
        self.max  = 8
    
    def updateBoard(self, listOfPieces): #update the positions of all pieces on board, and make sure each piece has a copy of updated positions
        for piece in listOfPieces:
            self.pieces[piece.pieceName] = piece
            piece.Board1 = self
        return listOfPieces


    def offBoard(self, point):#returns true if the point is off the board, returns false otherwise
        if (point[0]<self.min or point[0]>self.max or point[1]<self.min or point[1]>self.max):
            return True
        else:
            return False    

    def stepsBetween(self, point1, point2):#calculates the minimum number of steps between two points moving 1 square at a time
        dx = abs(point1[0]-point2[0])
        dy = abs(point1[1] - point2[1])
        #the minimum is always one less than the maximum distance along an axis
        if (dx >= dy):
            return dx - 1
        else:
            return dy - 1

    def convertToPoint(self, squareName):#can convert square's name to a coordinate point ie. a1 is [1,1]
        point = [None]*2
        point[0] = letterDictionary[squareName[0]]
        point[1] = int(squareName[1])
        return point

    def convertToName(self, point): #can convert coordinate point to a square name ie. [1,1] is a1
        for l in letterDictionary:
            if (letterDictionary[l]==point[0]):
                return (l + str(point[1]))
            
    def adjacent(self, point1, point2): #determine if any 2 points are adjacent
        if (self.stepsBetween(point1,point2)== 0):
            return True
        else:
            return False

    def oneStepBishopMove(self, point1, point2): #determines if the bishop can get from point 1 to point 2 in 1 step
        if (point1[0]==point2[0] or point1[1]==point2[1]):
            return False
        else:
            return True 

    def knightTrapped(self):#check if the knight is under attack, check if it is trapped, recommend moves if it is trapped
        trapped = False
        k1 = self.pieces[yourKing].currentPoint
        k2 = self.pieces[theirKing].currentPoint
        n1 = self.pieces[knight].currentPoint
        b1 = self.pieces[bishop].currentPoint
        if (self.adjacent(k2, n1)):#if the knight is under attack
            if (not n1 in self.pieces[bishop].getMoves(b1, capture = True) and not n1 in self.pieces[yourKing].getMoves(k1, capture = True)):#if the knight is guarded by the bishop, or the king, it is not trapped
                trapped = True
                for move in self.pieces[yourKing].validMoves: 
                    if (self.adjacent(move, n1)):#check if king can move to defend the knight
                        self.recommendedMoves[yourKing].append(move)
                        trapped=False

                for move in self.pieces[knight].validMoves:#if the knight can save itself
                    if (not self.adjacent(move, k2)): #if knight has valid move away from their king, it is not trapped 
                        self.recommendedMoves[knight].append(move)
                        trapped = False
                    if (self.adjacent(move, k1)): #if the knight has a valid move adjacent to your king, it is not trapped
                        self.recommendedMoves[knight].append(move)
                        trapped = False      
                if (self.lightOrDark(n1) == self.lightOrDark(b1)):#knight and bishop are on same color square --> check if bishop can move to defend knight
                    for bMove in self.pieces[bishop].validMoves: 
                        nextValidMoves = self.pieces[bishop].getMoves(bMove, capture=True)
                        if n1 in nextValidMoves:
                            self.recommendedMoves[bishop].append(bMove)
                            trapped = False
                else: #knight and bishop are on different color square --> check if knight can move to a point defended by bishop
                    for nMove in self.pieces[knight].validMoves:
                        if nMove in self.pieces[bishop].validMoves:
                            self.recommendedMoves[knight].append(nMove)
                            trapped = False
        self.recommendedMoves = self.removeDuplicates()
        return trapped
    
    def lightOrDark(self, point):#determines whether point falls on light square or dark square
        light = True
        if ((point[0] + point[1]) % 2 == 0): #ie. bishop is on dark square if on sum of x and y are even ie. [1,1] --> (1 + 1) % 2 == 0
            light = False
        return light
    
    def removeDuplicates(self):#removes duplicate points in recommended moves dictionary
        for piece in self.recommendedMoves:
            nonDuplicates = []
            for move in self.recommendedMoves[piece]:
                if (move not in nonDuplicates):
                    nonDuplicates.append(move)
            self.recommendedMoves[piece] = nonDuplicates
        return self.recommendedMoves

        
# functions unique to a chess piece, parent of king, knight, bishop          
# get input recieves the point on the board from when the program starts running
# remove occupied removes the squares occupied by pieces from a list of possible moves
# closest move to finds a pieces closest move to a point on the board
# farthest move away fings a pieces farthest move from a point on the board
# remove duplicates removes the repeated points in a list of possible moves
class ChessPiece:
    def __init__(self, pieceName, Board1):
        self.pieceName = pieceName
        self.Board1 = Board1
        self.currentPoint = self.getInput()
        self.validMoves = []

    def getInput(self):

        repeat = True
        
        while (repeat==True):
            entry = input("What square is %s on (ie. a1)? \n"%(self.pieceName)).rstrip().lstrip().lower() #get user input using piece name and ownership
            
            repeat = False #switch repeat to on when a condition fails

            if (len(entry)!=2): #condition 1: entry is not two characters long
                 repeat = True
            else:
                if (entry[0] not in columnLetters): #condition 2: 1st character is not letter a-h
                    repeat = True 
                else:
                    try: #condition 3: 2nd character is not integer
                        int(entry[1])
                    except:
                        repeat=True

                    if (repeat == False):
                        if (int(entry[1])>Board1.max and int(entry[1])<Board1.min):#condition 4: 2nd character is not in range of board
                            repeat=True

            if (repeat == True):#at least one condition failed, repeat loop
                print("Sorry that is an invalid entry. Please try again.")
        #end while loop
        return Board1.convertToPoint(entry)
    
        
    def removeOccupied(self, pieces):#removes squares occupied from the pieces in the dictionary from the possible valid moves  
        for p in pieces:
            if pieces[p].currentPoint in self.validMoves:
                self.validMoves.remove(p)
    
    '''
        def calculateBestMove(self, strategy):#determines the best move based on positions of the pieces (order: Bishop, Knight, Your King, Their king) and strategy at that moment 
        if (strategy==moveAway):
            self.farthestMoveAway(self, K2.currentPoint)#move away for bishop/knight
        elif (strategy==moveToward):
            self.closestMoveTo(self,K1.currentPoint)#move toward king for bishop/knight
        elif (strategy==defendKnight):
            self.Board1.saveKnight()
        self.removeDuplicates()   
    '''

    def closestMoveTo(self, piece1, point2):#selects from the piece 1's valid moves the closest square to point 2
        closest = 100
        for move in piece1.validMoves:
            dist = self.Board1.stepsBetween(move, point2) #find the steps between piece 2 and all the valid moves for piece 1
            if (dist < closest):
                closest = dist #finds closest distance reachable by next move to another piece
        for move in piece1.validMoves:
            dist = self.Board1.stepsBetween(move, point2) 
            if (dist == closest):  #filters for all next move squares that have closest distance
                Board1.recommendedMoves[piece1.pieceName].append(move)#use that option as the recommended
            
    def farthestMoveAway(self,piece1, point2):#selects from piece 1's valid moves the farthest from point 2
        farthest = 0
        for move in piece1.validMoves:#finds farthest distance reachable by next move to another piece
            dist = self.Board1.stepsBetween(move, point2)
            if (dist > farthest):
                farthest = dist 
        for move in piece1.validMoves:#filters for all next move squares that have farthest distance
            dist = self.Board1.stepsBetween(move, point2)
            if (dist == farthest): 
                Board1.recommendedMoves[piece1.pieceName].append(move)

#the functions that are unique to the king
#includes:
#king's next move 
class King(ChessPiece):
    def __init__(self, Board1, name):
        ChessPiece.__init__(self, name, Board1)

    def getMoves(self,point, capture):#to get all king's moves, place the king in the center of a 3x3 square
        validMoves = []
        for i in range(-1,2):
            for j in range(-1,2):
                newPoint = [point[0]+i, point[1]+j]
                if not Board1.offBoard(newPoint): #check the next move is within boundaries of board and not adjacent to their king
                        if (capture):#if the king intends to capture with it's next move (aka it is defend the knight) then add every new point
                            validMoves.append(newPoint)
                        else:
                            if (not self.Board1.adjacent(newPoint, self.Board1.pieces[theirKing].currentPoint)):#otherwise, only add the new point if it is not adjacent to their king
                                validMoves.append(newPoint) 
        validMoves.remove(point)#remove the current square (not a move)
        return validMoves




#functions that are unqiue to knight
#include:
#get next move, which runs 2 calls of function L group
class Knight(ChessPiece):
    def __init__(self, Board1):
        ChessPiece.__init__(self, knight, Board1)
    
    def getMoves(self, point, capture):#to get horse's L shape moves, simultaneously move 2 steps vertically with 1 step horizontally (and vice versa)
        validMoves = []
        for i in range(-1,2,2): #loop repeats 4 times 
            for j in range(-2,3,4): 
                newPoint1 = [point[0]+i, point[1]+j]
                newPoint2 = [point[0]+j, point[1]+i]
                if (capture):
                    validMoves.append(newPoint1)
                    validMoves.append(newPoint2)
                else:
                    if ((not self.Board1.offBoard(newPoint1)) and (newPoint1 != self.Board1.pieces[yourKing].currentPoint) and (newPoint1 != self.Board1.pieces[bishop].currentPoint)): #check the next move is still within boundaries of board and not on any off your pieces
                        validMoves.append(newPoint1)
                    if ((not self.Board1.offBoard(newPoint2)) and (newPoint2 != self.Board1.pieces[yourKing].currentPoint) and (newPoint2 != self.Board1.pieces[bishop].currentPoint)): #check the next move is still within boundaries of board and not on any off your pieces 
                        validMoves.append(newPoint2)    
        return validMoves
    
# functions unique to bishop
# include:
# get moves which runs 1 call of function quadrant diagonal
class Bishop(ChessPiece):
    def __init__(self, Board1):
        ChessPiece.__init__(self, bishop, Board1)
    
    def getMoves(self, point, capture):#to get all diagonally moves, place bishop in origin and move 1 step vertical & horizontal from origin in each quadrant
        validMoves = []
        for x in range(-1,2,2):#x=-1,1
            for y in range(-1,2,2):#y=-1,1
                valid = True
                i = 1
                while(valid):
                    newPoint = [point[0]+ x * i, point[1]+ y * i] #to get new point, add/subtract increments of 1 to x and y repeatedly until you bump into another piece, land adjacent to their king, or fall off board ie. x + 1 * i, y - 1 * i,  i = 1,2,3...
                    if not Board1.offBoard(newPoint): #check the next move is still within boundaries of board, 
                        if ((newPoint != self.Board1.pieces[yourKing].currentPoint) and (newPoint != self.Board1.pieces[knight].currentPoint)): #and is not on one of its own pieces
                            validMoves.append(newPoint)
                            i+=1
                        else:
                            if (capture): #if we are computing moves to capture, then we have to add the square that a piece occupied
                                validMoves.append(newPoint)
                            valid = False
                    else:
                        valid = False
        return validMoves





#Main Program
i = 1
for c in columnLetters:#populate the dictionary that maps letter columns to number values
    letterDictionary[c] = i
    i+=1

print("Please start with your move to play\n")
#create board and pieces
Board1 = Board() 
B1 = Bishop(Board1)
N1 = Knight(Board1)
K1 = King(Board1, yourKing) 
K2 = King(Board1, theirKing) 
B1,N1,K1,K2 = Board1.updateBoard([B1,N1,K1,K2]) 
#compute next moves
B1.validMoves = B1.getMoves(B1.currentPoint, capture = False)
N1.validMoves = N1.getMoves(N1.currentPoint, capture=False)
K1.validMoves = K1.getMoves(K1.currentPoint, capture = False)
#synchronize board and pieces after each update
B1,N1,K1,K2 = Board1.updateBoard([B1,N1,K1,K2]) 

#to test the program try using this visualizer:
# https://lichess.org/editor/8/3K4/8/4N3/3k4/1B6/8/8_w_HAha_-_0_1?color=white 
# ie. Place your bishop on g2, your knight on h8, your king on d7, and their king on g7
# ie. Place your bishop on b3, your knight on e5, your king on d7, and their king on d4
     
print("{0:-<35s}".format(""))

if (Board1.knightTrapped()):
    gameOver = True
    win = False
else:
    B1,N1,K1,K2 = Board1.updateBoard([B1,N1,K1,K2]) 
    print("{0:<10s}{1:<5s}{2:<20s}".format("Piece","","Recommended moves"))#headings
    print("{0:-<10s}{1:<5s}{2:-<20s}".format("","",""))
    for piece in Board1.recommendedMoves:
        allMoves = ""
        if (len(Board1.recommendedMoves[piece]) != 0):
            for move in Board1.recommendedMoves[piece]:
                allMoves = allMoves + Board1.convertToName(move) + ", "
            allMoves = allMoves[:-2]
            print("{0:<10s}{1:<5s}{2:<20s}".format(piece,"",allMoves))#table entries

if (gameOver):
    if (win):
        print("\nYou won by checkmate.")
    else:
        print("\nYou are going to lose your knight. The result is a draw by way of insufficient material.")
else: 
    print("\nThe game is still in play.")


