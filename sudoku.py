# Author: David Powdrill
# Date: 11/21/2020
# Description: Given a filled out Sudoku board, the program will verify that the Sudoku is solved correctly.
# Also, given an unsolved Sudoku board the program will solve it and show the solved Sudoku board to the user. If there
# is no way to solve the puzzle, the user is told it is unsolvable and leaves the board in it's beginning state.
# Hosted at: https://repl.it/@powdrild/Sudoku#main.py

import pygame
from pygame.locals import *
import sys
import requests


class Sudoku:
    def __init__(self, grid):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("Sudoku Solver/Verifier 1.0")
        self.grid = grid
        self.locked = [[False for row in range(9)] for col in range(9)]
        self.dif = 500 / 9
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (39, 232, 51)
        self.RED = (255, 0, 0)
        self.font = pygame.font.SysFont('Comic Sans', 60)
        self.small_font = pygame.font.SysFont('Comicsansms', 19)
        self.small_font2 = pygame.font.SysFont('Comicsansms', 30)
        self.small_font3 = pygame.font.SysFont('Comicsansms', 25)
        self.screen = pygame.display.set_mode((500, 650))
        self.screen.fill(self.WHITE)
        self.solved = False
        self.x = 0
        self.y = 0
        self.count = 0

    def instructions(self):
        """Renders the instructions/controls to the user"""
        text = self.small_font.render("Press enter to solve/verify the Sudoku!", 1, self.BLACK)
        self.screen.blit(text, (70, 550))
        text1 = self.small_font.render("Press the space bar to generate a new Sudoku board!", 1, self.BLACK)
        self.screen.blit(text1, (15, 520))

    def new_game(self):
        """Sets Sudoku board up for a new game"""
        self.solved = False
        self.make_locked()
        self.clear_board()
        self.drawGrid()
        rect = pygame.Rect(70, 590, 350, 50)
        pygame.draw.rect(self.screen, self.WHITE, rect)  # erases Sudoku ending text (ex. "Sudoku Solved!" erased)

    def random_board(self):
        """Generates a random Sudoku board. Only works if can connect to internet.
        Reference: https://github.com/berto/sugoku"""
        r = requests.get('https://sugoku.herokuapp.com/board?difficulty=random')
        json_board = r.json()
        board = json_board["board"]
        self.grid = board

    def drawGrid(self):
        """Draws the Sudoku board for pygame
        Reference: https://www.geeksforgeeks.org/building-and-visualizing-sudoku-game-using-pygame/"""
        blockSize = 56  # Set the size of the grid block
        for x in range(9):  # draws each square
            for y in range(9):
                rect = pygame.Rect(x * blockSize, y * blockSize, 1, 1)
                pygame.draw.rect(self.screen, self.BLACK, rect, 1)
                self.draw(x, y)
        for i in range(10):  # draws each line, thick and non-think for pygame
            if i % 3 == 0:
                thick = 7
            else:
                thick = 1
            pygame.draw.line(self.screen, self.BLACK, (0, i * self.dif), (500, i * self.dif), thick)
            pygame.draw.line(self.screen, self.BLACK, (i * self.dif, 0), (i * self.dif, 500), thick)

    def draw(self, x, y):
        """Draws all numbers to their correct spot for pygame"""
        if self.check_locked(x,y) is True:  # Black numbers for starter numbers
            text1 = self.font.render(str(self.grid[x][y]), 1, self.BLACK)
            self.screen.blit(text1, (y * self.dif + 15, x * self.dif + 15))
        else:  # green numbers for solved numbers
            text1 = self.font.render(str(self.grid[x][y]), 1, self.GREEN)
            self.screen.blit(text1, (y * self.dif + 15, x * self.dif + 15))

    def clear(self, x, y):
        """Clears a number from their spot for pygame"""
        blockSize = 56
        rect = pygame.Rect(y * blockSize, x * blockSize, blockSize, blockSize)
        pygame.draw.rect(self.screen, self.WHITE, rect)

    def clear_board(self):
        """Clears each spot on the board for pyagme"""
        for x in range(9):
            for y in range(9):
                self.clear(x, y)

    def make_locked(self):
        """Locks starter numbers and makes zero's into blank spaces"""
        self.locked = [[False for row in range(9)] for col in range(9)]
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] != 0:
                    self.locked[i][j] = True
                    self.count += 1
                else:
                    self.grid[i][j] = ' '

    def check_locked(self, x, y):
        """Checks if a spot is locked"""
        if self.locked[x][y] is True:
            return True
        return False

    def solve(self):
        """Returns True if Sudoku is solvable. Otherwise, returns False.
        Reference: https://www.geeksforgeeks.org/sudoku-backtracking-7/"""
        if self.solved is True:
            return True
        spot = self.playable_spot()
        if spot is False:  # All spots on board are filled
            if self.count == 81:  # user submitted board for verification
                if self.check_sudoku() is True:
                    self.solved = True
                    return True
                else:
                    return False
            return True
        if spot is not False:
            row = spot[0]
            col = spot[1]
            for i in range(1, 10):  # Attempts numbers 1-9 in spot
                if self.check_row(i, row) is True and self.check_col(i, col) is True \
                        and self.check_box(i, row, col) is True:  # legal number placement
                    self.grid[row][col] = i  # places number
                    self.clear(row, col)  # clears spot for pygame
                    self.draw(row, col)  # places number for pygame
                    if col == 8 and row == 8:  # All spots have been filled legally
                        self.solved = True
                    if self.solve() is True:  # recursive call with number (i) on grid
                        self.solved = True  # sudoku is solved
                        self.end_puzzle()
                        return True
                    else:  # if recursive call doesn't end up solving sudoku, resets number to blank space and tries
                        # next number in the spot where recursive call occurred
                        self.grid[row][col] = ' '
            return False  # not solvable

    def check_row(self, num, row):
        """Checks if num is compatible with row"""
        count = 0
        for numbers in self.grid[row]:
            if self.count == 81:  # user submitted board for verification
                if numbers == num:
                    count += 1
            else:
                if numbers == num:
                    return False
        if count == 2:
            return False
        return True

    def check_col(self, num, col):
        """Checks if num is compatible with column"""
        count = 0
        for i in range(9):
            if self.count == 81:  # user submitted board for verification
                if self.grid[i][col] == num:
                    count += 1
            else:
                if self.grid[i][col] == num:
                    return False
        if count == 2:
            return False
        return True

    def check_box(self, num, row, col):
        """Checks if num is compatible within box"""
        box_row = row // 3  # row number of big boxes that number is in
        box_col = col // 3  # column number of big boxes that number is in
        count = 0
        if box_row == 0 and box_col == 0:
            for row in range(3):
                for col in range(3):
                    if self.count == 81:  # user submitted board for verification
                        if self.grid[row][col] == num:
                            count += 1
                    else:
                        if self.grid[row][col] == num:
                            return False
        if box_row == 0 and box_col == 1:
            for row in range(3):
                for col in range(3, 6):
                    if self.count == 81:
                        if self.grid[row][col] == num:
                            count += 1
                    else:
                        if self.grid[row][col] == num:
                            return False
        if box_row == 0 and box_col == 2:
            for row in range(3):
                for col in range(6, 9):
                    if self.count == 81:
                        if self.grid[row][col] == num:
                            count += 1
                    else:
                        if self.grid[row][col] == num:
                            return False
        if box_row == 1 and box_col == 0:
            for row in range(3, 6):
                for col in range(3):
                    if self.count == 81:
                        if self.grid[row][col] == num:
                            count += 1
                    else:
                        if self.grid[row][col] == num:
                            return False
        if box_row == 1 and box_col == 1:
            for row in range(3, 6):
                for col in range(3, 6):
                    if self.count == 81:
                        if self.grid[row][col] == num:
                            count += 1
                    else:
                        if self.grid[row][col] == num:
                            return False
        if box_row == 1 and box_col == 2:
            for row in range(3, 6):
                for col in range(6, 9):
                    if self.count == 81:
                        if self.grid[row][col] == num:
                            count += 1
                    else:
                        if self.grid[row][col] == num:
                            return False
        if box_row == 2 and box_col == 0:
            for row in range(6, 9):
                for col in range(3):
                    if self.count == 81:
                        if self.grid[row][col] == num:
                            count += 1
                    else:
                        if self.grid[row][col] == num:
                            return False
        if box_row == 2 and box_col == 1:
            for row in range(6, 9):
                for col in range(3, 6):
                    if self.count == 81:
                        if self.grid[row][col] == num:
                            count += 1
                    else:
                        if self.grid[row][col] == num:
                            return False
        if box_row == 2 and box_col == 2:
            for row in range(6, 9):
                for col in range(6, 9):
                    if self.count == 81:
                        if self.grid[row][col] == num:
                            count += 1
                    else:
                        if self.grid[row][col] == num:
                            return False
        if self.count == 2:
            return False
        return True

    def playable_spot(self):
        """Returns a spot on the board that is playable (' ')"""
        i = 0
        for row in self.grid:
            j = 0
            for col in row:
                if self.grid[i][j] == ' ':
                    return [i, j]
                j += 1
            i += 1
        return False

    def check_sudoku(self):
        """Returns True if user's solution is correct. Otherwise, returns False."""
        for i in range(9):
            for j in range(9):
                num = self.grid[i][j]
                if self.check_row(num, i) is False:
                    return False
                if self.check_col(num, j) is False:
                    return False
                if self.check_box(num, i, j) is False:
                    return False
        return True

    def solve_status(self):
        """Returns the solved status of the board"""
        return self.solved

    def end_puzzle(self):
        """Renders 'SUDOKU SOLVED!' if solved. Otherwise renders 'SUDOKU UNSOLVABLE!'"""
        if self.solved is True:
            text = self.small_font2.render("SUDOKU SOLVED!", 1, self.GREEN)
            self.screen.blit(text, (120, 590))
        else:
            text = self.small_font3.render("SUDOKU INCORRECT/UNSOLVABLE!", 1, self.RED)
            self.screen.blit(text, (25, 590))


grid = [[6,4,2,1,3,8,5,7,9],
         [1,3,5,2,7,9,4,6,8],
         [7,8,9,4,5,6,1,2,3],
         [2,1,3,5,4,7,8,9,6],
         [4,5,6,8,9,2,3,1,7],
         [8,9,7,3,6,1,2,4,5],
         [3,6,1,7,2,5,9,8,4],
         [5,7,8,9,1,4,6,3,2],
         [9,2,4,6,8,3,7,5,1]]

# grid = [[0,0,0,1,0,0,5,0,0],
#          [0,0,5,0,7,0,0,6,0],
#          [0,0,0,4,0,0,0,0,0],
#          [2,0,3,0,0,7,8,0,0],
#          [4,5,0,8,9,2,3,1,0],
#          [0,0,7,0,6,0,0,4,5],
#          [0,6,1,7,2,0,9,0,0],
#          [5,0,8,9,1,4,6,0,0],
#          [9,0,4,0,0,3,0,5,1]]

game = Sudoku(grid)
game.instructions()
game.new_game()
while True:
    game.drawGrid()
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
          if event.key == K_SPACE:
            game.random_board()
            game.new_game()
          if event.key == K_RETURN:
            game.clear_board()
            if game.solve() is False:
              game.clear_board()
            game.end_puzzle()
          if event.key == K_ESCAPE:
            pygame.quit()
            sys.exit(0)
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit(0)
      pygame.display.flip()