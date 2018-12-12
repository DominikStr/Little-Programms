import numpy as np
import time
import timeit
import pandas as pd
import sys

    

class Sudoku:
    def __init__(self, number = 0):
        self.solved = False
        self.board = np.zeros([9,9], dtype = int)
        
        
        if type(number) == int :
            sudoku_data = pd.read_csv( "C:/Users/domin/Documents/Programmieren/Sudoku/sudoku_csv.csv", nrows= number + 5)
        
            sudoku = sudoku_data.iloc[number]
    
            for y in range(len(self.board)):
                for x in range(len(self.board[y])):
            
                    index = x + y*9
                    self.board[y][x] = sudoku["quizzes"][index]
        
        elif number == "escargot":
            self.board = [[1, 0, 0, 0, 0, 7, 0, 9, 0],
                          [0, 3, 0, 0, 2, 0, 0, 0, 8],
                          [0, 0, 9, 6, 0, 0, 5, 0, 0],
                          [0, 0, 5, 3, 0, 0, 9, 0, 0],
                          [0, 1, 0, 0, 8, 0, 0, 0, 2],
                          [6, 0, 0, 0, 0, 4, 0, 0, 0],
                          [3, 0, 0, 0, 0, 0, 0, 1, 0],
                          [0, 4, 0, 0, 0, 0, 0, 0, 7],
                          [0, 0, 7, 0, 0, 0, 3, 0, 0]]
        
        elif number == "17clues":
             self.board = [[0, 0, 0, 7, 0, 0, 0, 0, 0],
                           [1, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 4, 3, 0, 2, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 6],
                           [0, 0, 0, 5, 0, 9, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 4, 1, 8],
                           [0, 0, 0, 0, 8, 1, 0, 0, 0],
                           [0, 0, 2, 0, 0, 0, 0, 5, 0],
                           [0, 4, 0, 0, 0, 0, 3, 0, 0]]
        
    def printit(self):
        String = "   "
        tempString = ""
        
        for i in range(len(self.board)):
            String += "  " + str(i+1) + " "
            
            if (i+1) % 3 == 0 and i:
               String += "   " 
            
        String += "\n" + " "*2 + "_"*46 + "\n"*2
            
        for y in range(len(self.board)):
            
            String += str(y+1) + " | "
            tempString += "  | "
            
            for x in range(len(self.board[y])):
                
                if self.board[y][x] != 0:
                    String += " " + str(self.board[y][x]) + "  "
                    
                else: 
                    String += "    "
                
                tempString += "    "
                
                if (x+1) % 3 == 0:
                    String += " | "
                    tempString += " | "
            
            if (y+1) % 3 == 0:
               String += "\n" + " "*2 + "_"*46 + "\n"
            
            
            if y < 8:
                String += "\n" + tempString + "\n"
                tempString = ""
            
        print(String)
        
    def get_possibilities(self, x, y):
        
        still_possible = list(range(10))
        
        if self.board[y][x] != 0:
            still_possible = []
            #print(" Already filled ")
        else:
            """//////////////// Check Rows /////////////////////"""
            for dx in range(len(self.board[y])):
                if self.board[y][dx] in still_possible:
                    still_possible.remove(self.board[y][dx])
                     
            """//////////////// Check Columns /////////////////////"""
            for dy in range(len(self.board)):
                if self.board[dy][x] in still_possible:
                    still_possible.remove(self.board[dy][x])
                     
            """//////////////// Check Square /////////////////////"""
            
            square = self.get_square(x,y)
            
            for dy in range(len(self.board)):
                for dx in range(len(self.board[y])):
                    if self.get_square(dx,dy) == square:
                        if self.board[dy][dx] in still_possible:
                            still_possible.remove(self.board[dy][dx])
             
        return still_possible
      
    def get_square(self, x, y):
        """ Square 1; Square 2; Square 3
            Square 4; Square 5; Square 6
            Square 7; Square 8; Square 9"""
            
        if y < 3: 
            if x < 3: square = 1  
            elif x > 5: square = 3
            else: square = 2
                
        elif y > 5: 
            if x < 3: square = 7  
            elif x > 5: square = 9
            else: square = 8
        
        else: 
            if x < 3: square = 4  
            elif x > 5: square = 6
            else: square = 5
            
        return square
    
        
    def verify(self):
        
        solved = True
    
        for dy in range(len(self.board)):
            SumRow = 0 
            for dx in range(len(self.board[dy])):
                SumRow += self.board[dy][dx] 
            if SumRow != 45:
                solved = False
        
        for dx in range(len(self.board[1])):
            SumCol = 0 
            for dy in range(len(self.board)):
                SumCol += self.board[dy][dx] 
            if SumCol != 45:
                solved = False
        
        for dy in range(len(self.board)):
            for dx in range(len(self.board[dy])):
                SumSqr = 0
                
                for j in range(len(self.board)):
                    for i in range(len(self.board[dy])):
                        if self.get_square(i,j) == self.get_square(dx,dy):
                            SumSqr += self.board[j][i] 
                
                if SumSqr != 45:    
                    solved = False
        
        
        return solved
    
    
    def solvable(self):
        
        solvable = True
    
        for dy in range(len(self.board)):
            for dx in range(len(self.board[dy])):
                if self.board[dy][dx] == 0: 
                    if self.get_possibilities(dx,dy) == []:
                        solvable = False
        
        return solvable
    

    def solve(self):
    
        move_possible = True
        moves_made = []
        
        
        while self.solved == False and move_possible == True:
            
            move_possible = False
            
            for dy in range(len(self.board)):
                for dx in range(len(self.board[dy])):
                    
                    possibilities = self.get_possibilities(dx,dy)
                    
                    col_candidates = []
                    row_candidates = []
                    sqr_candidates = []
                    
                    
                    if len(possibilities) == 1:
                        self.board[dy][dx] = possibilities[0]
                        
                        move = [dx,dy]
                        
                        if move not in moves_made:
                            moves_made.append(move)
                        
                        move_possible = True
                    
                    elif len(possibilities) > 1:
                        
                        #### look in column   
                        for i in range(len(self.board)):
                            if i != dy and self.board[i][dx] == 0 :
                                col_possibilities = self.get_possibilities(dx,i)
                                col_candidates.append(col_possibilities)
                                
                        possibilities_copy = []
                        
                        for pos in range(len(possibilities)):
                            not_in = True
                            
                            for can in range(len(col_candidates)):
                                if possibilities[pos] in col_candidates[can]:
                                    not_in = False
                            
                            if not_in == True:
                                possibilities_copy.append(possibilities[pos])
                        
                        
                        if len(possibilities_copy) == 1:
                            self.board[dy][dx] = possibilities_copy[0]
                            
                            move = [dx,dy]
                            
                            if move not in moves_made:
                                moves_made.append(move)
                            
                            move_possible = True
                        
                        if move_possible != True:
                            #### look in column   
                            
                                for j in range(len(self.board[dy])):
                                    if j != dx and self.board[dy][j] == 0 :
                                        row_possibilities = self.get_possibilities(j,dy)
                                        row_candidates.append(row_possibilities)
                                
                                possibilities_copy = []
                                
                                for pos in range(len(possibilities)):
                                    not_in = True
                                    
                                    for can in range(len(row_candidates)):
                                        if possibilities[pos] in row_candidates[can]:
                                            not_in = False
                                    
                                    if not_in == True:
                                        possibilities_copy.append(possibilities[pos])
                                
                                
                                if len(possibilities_copy) == 1:
                                    self.board[dy][dx] = possibilities_copy[0]
                                    
                                    move = [dx,dy]
                                    
                                    if move not in moves_made:
                                        moves_made.append(move)
                                    
                                    move_possible = True
                        
                        
                        if move_possible != True:

                            #### look in square
                            for j in range(len(self.board)):
                                for i in range(len(self.board[dy])):
                                    if self.get_square(i,j) == self.get_square(dx,dy):
                                    
                                        if not (i == dx and j == dy) and self.board[j][i] == 0 :
                                            sqr_possibilities = self.get_possibilities(i,j)
                                            sqr_candidates.append(sqr_possibilities)
                                
                            possibilities_copy = []
                            
                            
                            for pos in range(len(possibilities)):
                                not_in = True
                                
                                for can in range(len(sqr_candidates)):
                                    if possibilities[pos] in sqr_candidates[can]:
                                        not_in = False
                                 
                                if not_in == True:
                                    possibilities_copy.append(possibilities[pos])
    
                            
                            if len(possibilities_copy) == 1:
                                self.board[dy][dx] = possibilities_copy[0]
                                
                                move = [dx,dy]
                                
                                if move not in moves_made:
                                    moves_made.append(move)
                                
                                move_possible = True
            
            self.solved = self.verify()
               
        
        if self.solvable() == True:
            for dy in range(len(self.board)):
                for dx in range(len(self.board[dy])):
                    if self.board[dy][dx] == 0:
                        possibilities = self.get_possibilities(dx,dy)
                        
                        for i in range(len(possibilities)):
                            
                            self.board[dy][dx] = possibilities[i]
                                    
                            move = [dx,dy]
                            moves_made.append(move)
                            
                            
                                    
                            if self.solvable() == True: 
                                self.solve()
                                
                            if self.solved == False:
                                for j in range(len(moves_made)):
                                    self.board[moves_made[j][1]][moves_made[j][0]] = 0
                            else:
                                break

                        break
                if self.board[dy][dx] == 0:
                    break
                        
        else:
            for j in range(len(moves_made)):
                self.board[moves_made[j][1]][moves_made[j][0]] = 0
            
            
            
        self.solved = self.verify()
        
        
        return self.solved
    
def test_all(a,b):
    start = timeit.default_timer()

    for i in range(10000):
        x = Sudoku(i)
        
        x.solve()
        
        if x.solved != True:
            print("You failed")
            break
        
        if i % 100 == 0:

            print("Status: " + str(i/100) + " %")
    
    stop = timeit.default_timer()
    
    print( "Solved: " + str(x.verify()))
    print('Elapsed time: ', stop - start) 
            
    x.printit() 

def test_one(Name):     
        
    x = Sudoku(Name)
    x.printit()
    
    start = timeit.default_timer()
    
    x.solve()
    
    stop = timeit.default_timer()
    
    print( "Solved: " + str(x.verify()))
    print('Elapsed time: ', stop - start) 
            
    x.printit() 


#test_one("escargot")

test_all()

        
        
        