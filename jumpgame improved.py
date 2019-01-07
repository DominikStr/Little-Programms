import numpy as np
import time
import pandas as pd

sudoku_data = pd.read_csv( "C:/Users/domin/Documents/Programmieren/Sudoku/sudoku_csv.csv") 


def create_gameboard(alt = False):
    """ Creates an empty Gameboard"""
    game_board_blank = np.empty([7,7], dtype = str)
    for i in range(len(game_board_blank)):
        for j in range(len(game_board_blank[i])):
            if i < 2 and 1 < j < 5:
                game_board_blank[i][j] = "I"
            elif 1 < i < 5:
                game_board_blank[i][j] = "I"
            elif 4 < i and 1 < j < 5:
                game_board_blank[i][j] = "I"
            else: 
                game_board_blank[i][j] = "#"
            if i == 3 and j == 3:
                game_board_blank[i][j] = " "
    
    if alt == True:
        game_board_blank[1][1] = "I"
        game_board_blank[1][5] = "I"
        game_board_blank[5][1] = "I"
        game_board_blank[5][5] = "I"
    
    
    return gameboard_as_dict(game_board_blank)

def string_gameboard(board):
    """ Returns the gamboard as a string which can be printed"""
    String = "     "
    for i in range(7):
        String += str(i+1) + "   "
        
    String += "\n"*2   
        
    for y in range(7):
        String += str(y+1) + "   "
        for x in range(7):
            String += str(board["["+str(x)+", "+str(y)+"]"]) + "   "
        String += "\n"
        
    return String

def gameboard_as_dict(board):
    gameboard = {}
    for i in range(len(board)):
        for j in range(len(board[i])):
            loccoordiante = str([j,i])
            gameboard[loccoordiante] = board[i][j]
    
    return gameboard



def valid_move(board,before, after):
     
    xB = before[0]
    xA = after[0]
    yB = before[1]
    yA = after[1]
    
    if (str(before) or str(after))  not in board:
        print("\n Not a valid coordinate. Please try again")
        return False
    
    elif (board[str(before)] or board[str(after)])  == "#":
        print("\n Not a valid coordinate (#). Please try again")
        return False
       
    elif board[str(before)] != "I":
        print("\n No Pin in this position. Please try again")
        return False
        
    elif board[str(after)] != " ":
        print("\n You can not move on to another pin. Please try again")    
        return False
            
    elif (abs(xB - xA) != 2 or abs(xB - xA) == 0) and (abs(yB - yA) != 2 or abs(yB - yA) == 0):
        print("\n Not a valid move (too far, too close). Please try again")
        return False
    
    elif (xA != xB) and (yA != yB):
        print("\n Not a valid move (diagonal). Please try again")
        return False
    
    else:
        return True


def move_and_delete(board, before, after):
    """ Moves a pin and deletes the on jumped over"""
    
    xB = before[0]
    xA = after[0]
    yB = before[1]
    yA = after[1]
    
    xR = int(xB + 0.5*(xA - xB))
    yR = int(yB + 0.5*(yA - yB))
    
    board["["+str(xB)+", "+str(yB)+"]"] = " "
    board["["+str(xA)+", "+str(yA)+"]"] = "I"
    board["["+str(xR)+", "+str(yR)+"]"] = " "
    
    return board
    


def give_valid_moves(board):
    """Returns all valid moves possible"""
    
    valid_moves = []

    for cor in board:
        loccoordinate = str(cor)
        
        i = int(cor[4])
        j = int(cor[1])
        
        if board[loccoordinate] == "I":
            if board.get(str([j+2,i])) == " " and board.get(str([j+1,i])) == "I":
                if valid_move(board, [j,i], [j+2, i]):
                    valid_moves += [[[j,i],[j+2,i]]]
                
            if board.get(str([j-2,i])) == " " and board.get(str([j-1,i])) == "I":
                if valid_move(board, [j,i], [j-2, i]):
                    valid_moves += [[[j,i],[j-2,i]]]
                
            if board.get(str([j,i+2])) == " " and board.get(str([j,i+1])) == "I":
                if valid_move(board, [j,i], [j, i+2]):
                    valid_moves += [[[j,i],[j,i+2]]]
                
            if board.get(str([j,i-2])) == " " and board.get(str([j,i-1])) == "I":
                if valid_move(board, [j,i], [j, i-2]):
                    valid_moves += [[[j,i],[j,i-2]]]
       
    return valid_moves          
            
def pins_left(board):
    """ Returns the amount of pins left"""
    
    counter = 0
    
    for cor in board:
        if board[cor] == "I":
            counter += 1
    
    return counter
    


def review_solution(Board, Solution):
    
    for move in Solution:
        
        #print(move)
        
        Board = move_and_delete(Board, move[0], move[1])
        
        #time.sleep(2)
        
        
        print(string_gameboard(Board))
        

            
def find_solution(previousboard, Solution):
    
    global Found
    
    if Found == False:    
        if pins_left(previousboard) <= 1:
            
            Found = True
        
        else: 
            validmoves = give_valid_moves(previousboard)
            
            
            for move in validmoves: 
                
                board = previousboard.copy()
                
                newboard = move_and_delete(board, move[0], move[1])
                
                
                if Found == False:
                    Solution.append(move)
                
                if Found == False:
                    find_solution(newboard, Solution)
                
                if Found == False:
                    Solution.pop()
                
                
    
    return Solution


print("Start Calculation")

starttime = time.time()

Board = create_gameboard(alt = True)

#Board["["+str(3)+", "+str(3)+"]"] = "I"
#Board["["+str(3)+", "+str(2)+"]"] = " "

#print(Board)

global Found
Found = False

global Solution
Solution = []

sol = find_solution(Board, Solution)

endtime = time.time()
time = endtime - starttime

print("Calculation finished")
print("Time needed: " + str(time))

# Beginn:	             Time0 = 4.160743474960327 
# After all as dict:   Time1 = 1.2216978073120117

review_solution(Board, sol)
