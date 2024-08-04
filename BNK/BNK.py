#Justin Yu
#August 5, 2024
#BNK: a fool-proof way to checkmate with bishop, knight, and king (the hardest endgame to execute).

#static variables that all classes can use
min = 1
max = 8
knight = "knight"
bishop = "bishop"
king = "king"
yours = "your"
theirs = "their"
ColumnLetters = "abcdefgh"
letterDictionary = {}

class Board:
    def __init__(self):
        self.points = []
    
    def update(self, point, remove): #update the positions of all pieces
        if (remove):
            self.points.remove(point)
        else:
            self.points.append(point)

class ChessPiece:
    def __init__(self, pieceName, owner):
        self.pieceName = pieceName
        self.owner = owner
        self.currentPoint = self.getInput()
        self.validMoves = []
        Board1.update(self.currentPoint, remove=False)

    def getInput(self):

        repeat = True
        
        while (repeat==True):
            entry = input("What square is %s %s on (ie. a1)? \n"%(self.owner, self.pieceName)).rstrip().lstrip().lower() #get user input using piece name and ownership
            
            repeat = False #switch repeat to on when a condition fails

            if (len(entry)!=2): #condition 1: entry is not two characters long
                 repeat = True
            else:
                if (entry[0] not in ColumnLetters): #condition 2: 1st character is not letter a-h
                    repeat = True 
                else:
                    try: #condition 3: 2nd character is not integer
                        int(entry[1])
                    except:
                        repeat=True

                    if (repeat == False):
                        if (int(entry[1])>max and int(entry[1])<min):#condition 4: 2nd character is not in range 1-8
                            repeat=True

            if (repeat == True):#at least one condition failed, repeat loop
                print("Sorry that is an invalid entry. Please try again.")
        #end while loop
        return self.convertToPoint(entry)
    
    def convertToPoint(self, squareName):#can convert any square name to a coordinate point ie. a1 is [1,1]
        point = [None]*2
        point[0] = letterDictionary[squareName[0]]
        point[1] = int(squareName[1])
        return point
    
    def convertToName(self, point): #can convert any point to a square name ie. [1,1] is a1
        for l in letterDictionary:
            if (letterDictionary[l]==point[0]):
                return (l + str(point[1]))
        
    def offBoard(self, point):#returns true if the point is off the board, returns false otherwise
        if (point[0]<min or point[0]>max or point[1]<min or point[1]>max):
            return True
        else:
            return False
        
    def removeOccupied(self, points):#removes occupied squares from possible moves
        for point in points:
            if point in self.validMoves:
                self.validMoves.remove(point)
    
    def stepsBetween(point1, point2):#calculates the minimum number of steps between two points moving 1 square at a time
        dx = abs(point1[0]-point2[0])
        dy = abs(point1[1] - point2[1])
        #the minimum is always one less than the maximum distance along an axis
        if (dx >= dy):
            return dx - 1
        else:
            return dy - 1


class King(ChessPiece):
    def __init__(self, owner):
        ChessPiece.__init__(self, king, owner)

    def GetMoves(self):#to get all king's moves, place the king in the center of a 3x3 square
        for i in range(-1,2):
            for j in range(-1,2):
                newPoint = [self.currentPoint[0]+i, self.currentPoint[1]+j]
                if not self.offBoard(newPoint): #check the next move is still within boundaries of board
                        self.validMoves.append(newPoint)
        self.validMoves.remove(self.currentPoint)#remove the center square (not a move)
        self.removeOccupied(Board1.points)

class Knight(ChessPiece):
    def __init__(self, owner):
        ChessPiece.__init__(self, knight, owner)
    
    def GetMoves(self):#to get horse's L shape moves, simultaneously move 2 steps vertically with 1 step horizontally (and vice versa)
        self.Lgroup(verticalTwo=True)
        self.Lgroup(verticalTwo=False)
        self.removeOccupied(Board1.points)

    def Lgroup(self, verticalTwo):
        for i in range(-1,2,2): #i covers 1 step
            for j in range(-2,3,4): #j covers 2 steps
                if (verticalTwo): #implement 2 steps vertical and 1 step horizontal or vice versa
                    newPoint = [self.currentPoint[0]+i, self.currentPoint[1]+j]
                else:
                    newPoint = [self.currentPoint[0]+j, self.currentPoint[1]+i]
                if not self.offBoard(newPoint): #check the next move is still within boundaries of board
                    self.validMoves.append(newPoint)

class Bishop(ChessPiece):
    def __init__(self, owner):
        ChessPiece.__init__(self, bishop, owner)
    
    def GetMoves(self):#to get all diagonally moves, place bishop in origin and move 1 step vertical & horizontal from origin in each quadrant
        self.quadrantDiagonal(1,1)#quadrant 1
        self.quadrantDiagonal(-1,1)#quadrant 2
        self.quadrantDiagonal(-1,-1)#quadrant 3
        self.quadrantDiagonal(1,-1)#qudrant 4
        self.removeOccupied(Board1.points)

    def quadrantDiagonal(self, x, y):
        onboard = True
        i = 1
        while(onboard):
            newPoint = [self.currentPoint[0]+ x * i, self.currentPoint[1]+ y * i]
            if not self.offBoard(newPoint): #check the next move is still within boundaries of board
                self.validMoves.append(newPoint)
                i+=1
            else:
                onboard = False
        
#Main Program
#populate the dictionary for easy future mapping
i = 1
for c in ColumnLetters:
    letterDictionary[c] = i
    i+=1


Board1 = Board()
K1 = King(yours)
N1 = Knight(yours)
B1 = Bishop(yours)
K2 = King(theirs)
#Debugging
'''
print(K1.convertToName(K1.currentPoint))
print(N1.convertToName(N.currentPoint))
print(B1.convertToName(B.currentPoint))
print(K2.convertToName(K2.currentPoint))
print("----------")

print("----------")
print("Your king: ")
print(K1.validMoves)
print("Your knight: ")
print(N1.validMoves)
print("Your bishop")
print(B1.validMoves)
print("Their king")
print(K2.validMoves)
print("----------")
#print(Board1.points)
print("----------")
'''
K1.GetMoves()
K2.GetMoves()
N1.GetMoves()
B1.GetMoves()
print("----------")
print("%d"%(ChessPiece.stepsBetween(N1.currentPoint, K2.currentPoint)))
print("%d"%(ChessPiece.stepsBetween(K1.currentPoint, K2.currentPoint)))