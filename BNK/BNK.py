'''
Author: Justin Yu
Date: August 15, 2024
Purpose: Checkmate with Bishop, Knight, and King
'''

#Global Variables
knight = "knight"
bishop = "bishop"
yourKing = "your king"
theirKing = "their king"
columnLetters = "abcdefgh"
letterDictionary = {} 


'''
Methods that pertain to the relation of pieces on a board
'''
class Board:
    def __init__(self):
        '''1'''
        self.pieces = {}#1. holds chess piece objects
        '''2'''
        self.recommendedMoves = {knight:[],bishop:[],yourKing:[],theirKing:[]} #2. recommended moves for each piece
        '''3'''
        self.min = 1#3. minimum board size
        '''4'''
        self.max  = 8#4. maximum board size
    
    '''
    updates board with the pieces, saves the board to each of those pieces, returns the pieces in a list
    '''
    def updateBoard(self, listOfPieces): 
        for piece in listOfPieces:
            self.pieces[piece.pieceName] = piece
        for piece in listOfPieces:
            piece.Board1 = self
        return listOfPieces

    '''
    returns true is the coordinate point is not within the dimensions of the board
    '''
    def offBoard(self, point):#returns true if the point is off the board, returns false otherwise
        if (point[0]<self.min or point[0]>self.max or point[1]<self.min or point[1]>self.max):
            return True
        else:
            return False    

    '''
    calcualtes how many steps it would take a king to travel between two coordinate points
    '''
    def stepsBetween(self, point1, point2):#calculates the minimum number of steps between two points moving 1 square at a time
        dx = abs(point1[0]-point2[0])
        dy = abs(point1[1] - point2[1])
        #the minimum is always one less than the maximum distance along an axis
        if (dx >= dy):
            return dx - 1
        else:
            return dy - 1

    '''
    returns the square's name of a coordinate point
    '''
    def convertToPoint(self, squareName):#can convert square's name to a coordinate point ie. a1 is [1,1]
        point = [None]*2
        point[0] = letterDictionary[squareName[0]]
        point[1] = int(squareName[1])
        return point

    '''
    returns the coordinate point of a square's name
    '''
    def convertToName(self, point): #can convert coordinate point to a square name ie. [1,1] is a1
        for l in letterDictionary:
            if (letterDictionary[l]==point[0]):
                return (l + str(point[1]))
            
    '''
    returns true when two points are 0 steps away from eachother
    '''
    def adjacent(self, point1, point2): #determine if any 2 points are adjacent
        if (self.stepsBetween(point1,point2)== 0):
            return True
        else:
            return False
        
    '''
    returns true if two points are 1 step away from eachother
    '''
    def withinOneStep(self, point1, point2): #determine if any 2 points are within 1 step
        if (self.stepsBetween(point1,point2) <= 1):
            return True
        else:
            return False

    '''
    returns true if the bishop can get from point 1 to point 2 in one move
    '''
    def oneStepBishopMove(self, point1, point2): #determines if the bishop can get from point 1 to point 2 in 1 step
        if (abs(point1[0])-abs(point2[0])) == (abs(point1[1])-abs(point2[1])):
            return True
        return False
            

    '''
    #1. check that K2 is adjacent to B1 and N1
    #2. check that K1 is not defending B1 nor N1 --> must move B1 or N1
    #3. check that N1 and B1 are on same-colored squares 
    #3a. check if N1 and B1 are adjacent --> move B1, N1, or K1
    #3b. check if B1 is on edge square
    #3c. check if B1 is on corner square
    #4. N1 and B1 on different-colored squares --> check if N1 defends B1
    
    def knightBishopTrapped(self):#check if knight and bishop are under attack
        k1 = self.pieces[yourKing].currentPoint
        k2 = self.pieces[theirKing].currentPoint
        n1 = self.pieces[knight].currentPoint
        b1 = self.pieces[bishop].currentPoint

        if (self.adjacent(k2,n1) and self.adjacent(k2,b1)):#1
            if (not self.adjacent(k1,n1) and not self.adjacent(k1,b1)):#2
                if (self.lightOrDark(n1)==self.lightOrDark(b1)):#3  
                    if (self.adjacent(n1,b1)):#3a.1
                        if (self.bishopOnEdge()):#3b.1
                            self.knightDefendBishop()
                        else: #3b.2
                            self.bishopDefendKnight()
                            self.knightDefendBishop()
                    else: #3a.2
                          self.bishopDefendKnight()
                          #determines which moves (if any) allow the bishop to defend knight
                else:#if the knight and bishop are on different colours, the only way they can be saved is if the knight defends the bishop already
                    #and the king steps in to defend the knight
                    pass
            else:#K1 is adjacent to N1 or adjacent to B1 meaning one of them is under attack by K2
                if (self.adjacent(k1, b1)):#N1 under attack
                    self.knightEscape()
                    self.bishopDefendKnight()
                elif (self.adjacent(k1, n1)):#B1 under attack
                    self.bishopTrapped()
                    self.knightDefendBishop()
    '''
    '''
    Goal: defend knight
    Action: move bishop to square that defends knight
    '''
    def bishopDefendKnight(self):#determine which moves (if any) allow the bishop to defend the knight, may need help of king or may not
        bOptimized = []
        k1 = self.pieces[yourKing].currentPoint
        k2 = self.pieces[theirKing].currentPoint
        n1 = self.pieces[knight].currentPoint
        b1 = self.pieces[bishop].currentPoint
        if (self.lightOrDark(n1) == self.lightOrDark(b1)):#knight and bishop are on same color square --> check if bishop can move to defend knight
            for move in self.pieces[bishop].validMoves:
                if n1 in self.pieces[bishop].getMoves(move, capture=True):
                    if (self.adjacent(move,k2)):
                        if (self.adjacent(move, k1)):
                            bOptimized.append(move)
                    else:
                        bOptimized.append(move)
            self.recommendedMoves[bishop] = bOptimized

    '''
    Goal: defend Bishop
    Action: move Knight to a square that defends bishop
    '''
    def knightDefendBishop(self):#determine which (if any) moves allow the knight to defend bishop with help of the king
        moves = self.pieces[knight].validMoves
        k1 = self.pieces[yourKing].currentPoint
        b1 = self.pieces[bishop].currentPoint
        nOptimized = []
        for move in moves:#check each recommended move to see if any of its next moves lands on bishop, if it does, check if the king is able to defend knight next, if so, can add to new list of optimized recommended moves
                if (b1 in self.pieces[knight].getMoves(move, capture=True) and self.withinOneStep(move,k1)):
                        nOptimized.append(move)
        self.recommendedMoves[knight] = nOptimized #add the move that defends the knight and bishop
    
    '''1. return True if B1 pinned to a corner square by K2 and N1'''
    def bishopTrapped(self):#determine if the bishop is trapped in the corner, if so the game ends in a draw
        if (len(self.pieces[bishop].validMoves)!=0):#if the bishop has moves, then it is not in 
            #the corner and is not trapped by your knight and their king
            for move in self.pieces[bishop].validMoves:
                self.recommendedMoves[bishop].append(move)

    '''
    To save the knight
    '''
    def knightEscape(self):#check if the knight is under attack, check if it is trapped, recommend moves if it is trapped
        k1 = self.pieces[yourKing].currentPoint
        k2 = self.pieces[theirKing].currentPoint
        n1 = self.pieces[knight].currentPoint
        b1 = self.pieces[bishop].currentPoint
        '''#1'''
        if (self.adjacent(k2, n1)):#if the knight is under attack
            '''#2'''
            if (not self.adjacent(n1,k1)):#move K1 to defend N1
                '''K1 moves to defend N1'''
                for move in self.pieces[yourKing].validMoves: 
                    if (self.adjacent(move, n1)):#check if king can move to defend the knight
                        self.recommendedMoves[yourKing].append(move)
                '''#3'''
                if (not n1 in self.pieces[bishop].getMoves(b1, capture = True)):#if the knight is not guarded by the bishop 
                    '''N1 moves away from K2 or moves to be defended by K1'''
                    for move in self.pieces[knight].validMoves:#if the knight can save itself
                        if (not self.adjacent(move, k2)): #if knight has valid move away from their king, it is not trapped 
                            self.recommendedMoves[knight].append(move)
                        if (self.adjacent(move, k1)): #if the knight has a valid move adjacent to your king, it is not trapped
                            self.recommendedMoves[knight].append(move)
                        if (move in self.pieces[bishop].getMoves(b1,capture=True)):#if the next move is guarded by bishop
                            self.recommendedMoves[knight].append(move)
        self.removeDuplicates()#remove any duplicate points added        
    

    '''1. return True if B1 is on edge square'''
    def bishopOnEdge(self):#determines whether the bishop is trapped on the edge
        onEdge = False
        b1 = self.pieces[bishop].currentPoint
        if (b1[0] == self.max or b1[0] == self.min or b1[1] == self.max or b1[1] == self.min):#if any of the bishop's coordinate values are max or min, then the bishop is on the edge
            onEdge = True
        return onEdge

    '''1. return True if coordinate point is on light square'''
    def lightOrDark(self, point):#determines whether point falls on light square or dark square
        light = True
        if ((point[0] + point[1]) % 2 == 0): #ie. bishop is on dark square if on sum of x and y are even ie. [1,1] --> (1 + 1) % 2 == 0
            light = False
        return light
    
    '''1. remove duplicated key values from property #2'''
    def removeDuplicates(self):#removes duplicate points in recommended moves dictionary
        for piece in self.recommendedMoves:
            nonDuplicates = []
            for move in self.recommendedMoves[piece]:
                if (move not in nonDuplicates):
                    nonDuplicates.append(move)
            self.recommendedMoves[piece] = nonDuplicates

    '''1. checks if the game is over based on how many recommended moves there are'''
    def checkGameOver(self):
        gameOver = True
        for piece in self.recommendedMoves:
            if len(self.recommendMoves[piece])!=0:
                gameOver = False

    '''1. clear all key values of property #2'''
    def clearAll(self):#clears all points in recommended moves dictionary
        for piece in self.recommendedMoves:
            self.recommendedMoves[piece] = []
    
    '''1. display keys and values of property #2'''
    def printRecommendedMoves(self):
        print("{0:<10s}{1:<5s}{2:<20s}".format("Piece","","Recommended moves"))#headings
        print("{0:-<10s}{1:<5s}{2:-<20s}".format("","",""))
        for piece in Board1.recommendedMoves:
            allMoves = ""
            if (len(Board1.recommendedMoves[piece]) != 0):
                for move in Board1.recommendedMoves[piece]:
                    allMoves = allMoves + Board1.convertToName(move) + ", "
                allMoves = allMoves[:-2]
                print("{0:<10s}{1:<5s}{2:<20s}".format(piece,"",allMoves))#table entries

    '''1. Select from options the farthest coordinate points to a coordinate point
    def farthestMoveAway(self, moves, point):#selects a piece's farthest moves from a point from a list of moves
        farthest = 0
        farthestMoves = []
        for move in moves:#finds farthest distance reachable by next move to another piece
            dist = self.stepsBetween(move, point)
            if (dist > farthest):
                farthest = dist 
        for move in moves:#filters for all next move squares that have farthest distance
            dist = self.stepsBetween(move, point)
            if (dist == farthest): 
                farthestMoves.append(move)
        return farthestMoves
    '''
    '''1. Select from options the closest coordinate points to a coordinate point
    def closestMoveTo(self, moves, point):#selects a piece's closest moves to a point from a list of moves
        closest = 100
        closestMoves = []
        for move in moves:
            dist = self.Board1.stepsBetween(move, point) #find the steps between piece 2 and all the valid moves for piece 1
            if (dist < closest):
                closest = dist #finds closest distance reachable by next move to another piece
        for move in moves:
            dist = self.Board1.stepsBetween(move, point) 
            if (dist == closest):  #filters for all next move squares that have closest distance
                closestMoves.append(move)#use that option as the recommended
        return closestMoves
    '''
'''class that pertain to the creation and behaviour of a new piece'''
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
        return self.Board1.convertToPoint(entry)
    
    
'''methods that pertain to the behaviour of a king''' 
class King(ChessPiece):
    def __init__(self, Board1, name):
        ChessPiece.__init__(self, name, Board1)

    def getMoves(self,point, capture):
        validMoves = []
        for i in range(-1,2):#0 or 1 step horizontal
            for j in range(-1,2):
                newPoint = [point[0]+i, point[1]+j]#0 or 1 step vertical
                if not self.Board1.offBoard(newPoint):
                        if (not self.Board1.adjacent(newPoint, self.Board1.pieces[theirKing].currentPoint)):
                            if (capture):
                                validMoves.append(newPoint)
                        else:
                            if ((newPoint !=self.Board1.pieces[bishop].currentPoint) and (newPoint!=self.Board1.pieces[knight].currentPoint)):
                                validMoves.append(newPoint) 
        validMoves.remove(point)#remove 0 steps vertical, zero steps horizontal
        return validMoves





class Knight(ChessPiece):
    def __init__(self, Board1):
        ChessPiece.__init__(self, knight, Board1)
    
    def getMoves(self, point, capture):
        validMoves = []
        for i in range(-1,2,2):
            for j in range(-2,3,4): 
                newPoint1 = [point[0]+i, point[1]+j] #1 square horizontal, 2 squares vertical
                if (not self.Board1.offBoard(newPoint1)):
                    if (capture):#all moves are valid when capture is on
                        validMoves.append(newPoint1)
                    else:
                        if ((newPoint1 != self.Board1.pieces[yourKing].currentPoint) and 
                            (newPoint1 != self.Board1.pieces[bishop].currentPoint)): #only moves that are not blocked by king and bishop are valid
                            validMoves.append(newPoint1)
                newPoint2 = [point[0]+j, point[1]+i]#2 squares horizontal, 1 square vertical
                if (not self.Board1.offBoard(newPoint2)):
                    if (capture):#all moves are valid when capture is on
                        validMoves.append(newPoint2)
                    else:
                        if ((newPoint2 != self.Board1.pieces[yourKing].currentPoint) and 
                            (newPoint2 != self.Board1.pieces[bishop].currentPoint)): #only moves that are not blocked by king and bishop are valid
                            validMoves.append(newPoint2)

        return validMoves



class Bishop(ChessPiece):
    def __init__(self, Board1):
        ChessPiece.__init__(self, bishop, Board1)
    
    def getMoves(self, point, capture):
        validMoves = []
        for x in range(-1,2,2): #move left or right
            for y in range(-1,2,2): #move up or down
                valid = True
                i = 1
                while(valid):
                    newPoint = [point[0]+ x * i, point[1]+ y * i] #move one step on diagonal
                    if not Board1.offBoard(newPoint):
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





# Main Program 
# Main Program 
# Main Program

'''initialize game state variables'''
gameOver = True
win = False

'''create a dictionary for mapping letters to numbers'''
i = 1
for c in columnLetters:#populate the dictionary that maps letter columns to number values
    letterDictionary[c] = i
    i+=1



#to test the program try using this visualizer:
# https://lichess.org/editor/8/3K4/8/4N3/3k4/1B6/8/8_w_HAha_-_0_1?color=white 
# ie. Place your bishop on g2, your knight on h8, your king on d7, and their king on g7
# ie. Place your bishop on b3, your knight on e5, your king on d7, and their king on d4

'''initialize the board and pieces'''
Board1 = Board() 
B1 = Bishop(Board1)
N1 = Knight(Board1)
K1 = King(Board1, yourKing) 
K2 = King(Board1, theirKing) 
B1,N1,K1,K2 = Board1.updateBoard([B1,N1,K1,K2]) 

'''get a list of moves given the current piece position, save those moves in the property of the piece'''
B1.validMoves = B1.getMoves(B1.currentPoint, capture = False)
N1.validMoves = N1.getMoves(N1.currentPoint, capture=False)
K1.validMoves = K1.getMoves(K1.currentPoint, capture = False)

'''updating pieces and board'''
B1,N1,K1,K2 = Board1.updateBoard([B1,N1,K1,K2]) 

''' determine if the knight and bishop are trapped'''
Board1.knightBishopTrapped()

'''decide necessity of determining if knight is trapped'''
skip = False
for piece in Board1.recommendedMoves: #determines if we need to run the next function or not 
    #(knight trapped is redundant if both knight and bishop are trapped)
    if len(Board1.recommendedMoves[piece]):
        skip = True

'''if knight and bishop are trapped, no need to check if knight is trapped, game is already over'''
if (not skip):
    Board1.knightEscape()


'''update board and pieces'''
B1,N1,K1,K2 = Board1.updateBoard([B1,N1,K1,K2]) 

'''display the recommended moves or inform the user that the game is over'''
if (not gameOver):
    Board1.printRecommendedMoves() 
else:
    print("\nYou are going to lose a piece. The result is a draw by way of insufficient material.")





