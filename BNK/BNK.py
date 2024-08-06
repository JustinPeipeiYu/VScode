#Justin Yu
#August 5, 2024
#BNK: a fool-proof way to checkmate with bishop, knight, and king (the hardest endgame to execute).

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
            
    def knightTrapped(self):#checks if all recommended moves for a knight result in capture, if so optimizes the recommendations by moving to a defended square
        trapped = True
        for move in self.recommendedMoves[knight]:
            if (self.stepsBetween(move, K2.currentPoint) > 0):
                trapped = False
        return trapped
    
    def lightOrDark(self, point):#determines whether point falls on light square or dark square
        light = True
        if ((point[0] + point[1]) % 2 == 0): #ie. bishop is on dark square if on [1,1] --> (1 + 1) % 2 == 0
            light = False
        return False

    def saveKnight(self): #returns true if the knight can be saved, returns false if it is destined to be captured resulting in draw
        if (self.Board1.lightOrDark(self.currentPoint)==self.Board1.lightOfDark(self.pieces[bishop])):#they are on same color square so bishop can move to defend     
            for bMove in self.pieces[bishop].validMoves:
                pass
        else: #they are on different color square so knight can move to a point defended by bishop
            for bMove in self.pieces[bishop].validMoves:
                if bMove == self.pieces[Knight].currentPoint:
                    self.recommendedMoves[knight] = bMove
                    return True
            





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
    
    
    def calculateBestMove(self, strategy):#determines the best move based on positions of the pieces (order: Bishop, Knight, Your King, Their king) and strategy at that moment 
        B1.GetMoves()
        N1.GetMoves()
        if (strategy==moveAway):
            self.farthestMoveAway(self, K2.currentPoint)#move away for bishop/knight
        elif (strategy==moveToward):
            self.closestMoveTo(self,K1.currentPoint)#move toward king for bishop/knight
        elif (strategy==defendKnight):
            self.Board1.saveKnight()
        self.removeDuplicates()    

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

    def removeDuplicates(self):#removes duplicate points in recommended moves
        for piece in Board1.recommendedMoves:
            nonDuplicates = []
            for move in Board1.recommendedMoves[piece]:
                if (move not in nonDuplicates):
                    nonDuplicates.append(move)
            Board1.recommendedMoves[piece] = nonDuplicates






class King(ChessPiece):
    def __init__(self, Board1, name):
        ChessPiece.__init__(self, name, Board1)

    def GetMoves(self):#to get all king's moves, place the king in the center of a 3x3 square
        for i in range(-1,2):
            for j in range(-1,2):
                newPoint = [self.currentPoint[0]+i, self.currentPoint[1]+j]
                if not Board1.offBoard(newPoint): #check the next move is still within boundaries of board
                        self.validMoves.append(newPoint)
        self.validMoves.remove(self.currentPoint)#remove the center square (not a move)







class Knight(ChessPiece):
    def __init__(self, Board1):
        ChessPiece.__init__(self, knight, Board1)
    
    def GetMoves(self):#to get horse's L shape moves, simultaneously move 2 steps vertically with 1 step horizontally (and vice versa)
        self.Lgroup(v2h1=True) #2 steps vertical, 1 step horizontal
        self.Lgroup(v2h1=False) #1 step vertical, 2 steps horizontal
        self.removeOccupied(self.Board1.pieces)

    def Lgroup(self, v2h1):
        for i in range(-1,2,2): #i covers 1 step
            for j in range(-2,3,4): #j covers 2 steps
                if (v2h1): #implement 2 steps vertical and 1 step horizontal or vice versa
                    newPoint = [self.currentPoint[0]+i, self.currentPoint[1]+j]
                else:
                    newPoint = [self.currentPoint[0]+j, self.currentPoint[1]+i]
                if not Board1.offBoard(newPoint): #check the next move is still within boundaries of board
                    self.validMoves.append(newPoint)
    
                




class Bishop(ChessPiece):
    def __init__(self, Board1):
        ChessPiece.__init__(self, bishop, Board1)
    
    def GetMoves(self):#to get all diagonally moves, place bishop in origin and move 1 step vertical & horizontal from origin in each quadrant
        self.quadrantDiagonal(self.Board1.pieces[yourKing].currentPoint, self.Board1.pieces[knight].currentPoint)

    def quadrantDiagonal(self,point1, point2): #x & y specify the quadrant we are computing for
        for x in range(-1,2,2):#x=-1,1
            for y in range(-1,2,2):#y=-1,1
                valid = True
                i = 1
                while(valid):
                    newPoint = [self.currentPoint[0]+ x * i, self.currentPoint[1]+ y * i] #to get new point, add/subtract increments of 1 to x and y repeatedly until you bump into another piece or fall off board ie. x + 1 * i, y - 1 * i
                    if not Board1.offBoard(newPoint): #check the next move is still within boundaries of board, 
                        if (self.Board1.stepsBetween(newPoint, point1)!=-1 and self.Board1.stepsBetween(newPoint, point2)!=-1): #and is not blocked by one of its own pieces
                            self.validMoves.append(newPoint)
                            i+=1
                        else:
                            valid = False
                    else:
                        valid = False






#Main Program
i = 1
for c in columnLetters:#populate the dictionary that maps letter columns to number values
    letterDictionary[c] = i
    i+=1

print("Please start with your move to play\n")
Board1 = Board() #create board
B1 = Bishop(Board1)
N1 = Knight(Board1)
K1 = King(Board1, yourKing) 
K2 = King(Board1, theirKing) 
B1,N1,K1,K2 = Board1.updateBoard([B1,N1,K1,K2]) #synchronize board with the pieces

#Debugging
'''
print(K1.convertToName(K1.currentPoint))
print(N1.convertToName(N.currentPoint))
print(B1.convertToName(B.currentPoint))
print(K2.convertToName(K2.currentPoint))
print("----------")

print("----------")
print("Your king: ")
print("Your knight: ")
print("Your bishop: ")
print("Their king: ")
print("----------")
print(K1.validMoves)
print(N1.validMoves)
print(B1.validMoves)
print(K2.validMoves)
print("----------")
#print(Board1.points)
print("----------")
K1.GetMoves()
K2.GetMoves()
print("----------")
print("%d"%(ChessPiece.stepsBetween(N1.currentPoint, K2.currentPoint)))
print("%d"%(ChessPiece.stepsBetween(K1.currentPoint, K2.currentPoint)))
'''
print("----------")
#start the computation
N1.calculateBestMove(strategy=moveAway)#calculate best move to move away from their king
#ChessPiece.calculateBestMove(strategy=moveToward)#calculate the best move to move toward your king
print(Board1.recommendedMoves)
print("Knight trapped: ")
print(Board1.knightTrapped())
print("Bishop on light: ")
print(Board1.lightOrDark(B1.currentPoint))
#print(N1.Board1.positions)



