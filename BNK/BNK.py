#Justin Yu
#August 5, 2024
#BNK: a program to checkmate with bishop, knight, and king


min = 1
max = 8
columnMap = {"a":1,"b":2,"c":3,"d":4,"e":5,"f":6,"g":7,"h":8}
knight = "knight"
bishop = "bishop"
king = "king"

class ChessPiece:
    def __init__(self, name):
        self.square = self.validateInput(name)

    def validateInput(self,name):
        while (True):
            #flag to decide if the user's entry is valid when the while loop ends
            valid = True 
        
            #get user input
            entry = input("What square is your %s on (ie. a1)? \n"%(name)).rstrip().lstrip().lower() 

            if (len(entry)!=2): #condition 1: entry is two characters long
                 valid = False
            else:
                if (entry[0] not in columnMap): #condition 2: 1st character is letter a-h
                    valid = False 
                else:
                    try: #condition 3: 2nd character is integer
                        int(entry[1])
                    except:
                        valid=False
                    if (valid):
                        if (int(entry[1])>max and int(entry[1])<min):#condition 4: 2nd character is in range 1-8
                            valid=False

            if (valid): #all checkpoints passed, break while loop, return value
                break
            else:
                print("Sorry that is an invalid entry. Please try again.")
                continue 
        return entry    
            

#Main Program
K = ChessPiece(knight)