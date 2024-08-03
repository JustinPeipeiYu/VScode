#Justin Yu
#August 5, 2024
#BNK: a program to checkmate with bishop, knight, and king


min = 1
max = 8
knight = "knight"
bishop = "bishop"
king = "king"
ColumnLetters = "abcdefgh"

class ChessPiece:
    def __init__(self, pieceName):
        self.PieceName = pieceName
        self.point = self.getInput(pieceName)

    def getInput(self,pieceName):#uses the piece name for the prompt, otherwise same for all new pieces. Asks for a position ie.a1 and returns corresponding coordinate ie.[1,1]
        #loop will repeat when repeat is true
        repeat = True
        while (repeat):
            #get user input
            entry = input("What square is your %s on (ie. a1)? \n"%(pieceName)).rstrip().lstrip().lower() 
            repeat = False
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

                    if (repeat):
                        if (int(entry[1])>max and int(entry[1])<min):#condition 4: 2nd character is not in range 1-8
                            repeat=True
            if (repeat == True):
                print("Sorry that is an invalid entry. Please try again.")
        #end while loop
        return self.convertToPoint(entry)
    
    def convertToPoint(self, squareName):
        point = [None]*2
        #convert a square to a cartesian point ie. a1 is (1,1)
        point[0] = LetterDictionary[squareName[0]]
        point[1] = int(squareName[1])
        return point
    
    def printPoint(self):
        print(self.point)
    
class King(ChessPiece):
    def __init__(self):
        ChessPiece.__init__(self, king)

class Knight(ChessPiece):
    def __init__(self):
        ChessPiece.__init__(self, knight)
        
class Bishop(ChessPiece):
    def __init__(self):
        ChessPiece.__init__(self, bishop)

#Main Program
#populate the dictionary for easy future mapping
i = 1
for c in ColumnLetters:
    LetterDictionary[c] = i
    i+=1

K = King()
N = Knight()
B = Bishop()
K.printPoint()
N.printPoint()
B.printPoint()


