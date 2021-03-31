"""
    File name: __init__.py
    Author: Patrick D
    Date created: 2021-03-31
    Date last modified:
    Purpose: Generate and solve Sodoku puzzles
"""
# imports
import tkinter
from tkinter import messagebox


# Create a class to represent a group of Sodoku puzzles, Puzzles()
class Puzzles:
    def __init__(self):
        self.pack = []
        self.sodoku = []
        self.size = 0
        self.create_puzzles()
        for p in range(self.size):
            self.sodoku.append(Sodoku(self.pack[p]))

    # Request user for file path to puzzle(s) in .txt format
    # import .txt file and create a matrix
    def open_file(cls):
        """Returns 2D array from user inputted local filepath, and number of puzzles located within the filepath
        :return p:
        :return num:
        """
        try:
            file_path = input("Please enter root filepath of your puzzles in .txt format")
            with open(file_path, "r") as file:
                # read the file and assign to fs
                fs = file.read().rsplit()
        except Exception as error:
            # set main tkinter window
            root = tkinter.Tk()
            # remove main window
            root.withdraw()
            # create alert box using tkinter messagebox
            messagebox.showinfo("ERROR!", error)
        # Determines the how many puzzles there are within the file
        num = int((len(fs) / 9))
        # create an empty 9x9 matrix
        p = [[None for _ in range(9)] for _ in range(num)]
        counter = 0
        for x in range(num):
            for y in range(9):
                p[x][y] = fs[counter]
                counter += 1
        return p, num

    # Creates a list of the rows from a individual puzzle, converts .txt type of each square into int
    def create_user_puzzle(cls, puzzle):
        """Takes the raw puzzle from a file as a parameter, returns a formatted puzzle by each row
        :param puzzle:
        :return rows_array:
        """
        rows_array = [[None for _ in range(9)] for _ in range(9)]
        row_counter = 0
        column_counter = 0
        for line in puzzle:
            for num in line:
                num = int(num)
                rows_array[row_counter][column_counter] = num
                if column_counter < 8:
                    column_counter += 1
                else:
                    column_counter = 0
            row_counter += 1
        return rows_array

    def create_puzzles(cls):
        """Calls open_file(), using the create_row_list(),
        returns a Pack object containing a Sodoku object for each puzzle,
        from the opened file"""
        # Creates puzzles from file
        puzzles, num_of_puzzles = cls.open_file()
        # Assigns number of puzzles to Pack() attribute, size
        cls.size = num_of_puzzles
        # Iterates over the range of the number of puzzles
        for p in range(num_of_puzzles):
            # Creates a matrix of integers from the puzzle, puzzle
            cls.pack.append(cls.create_user_puzzle(puzzles[p]))


# Create a Sodoku class
class Sodoku:
    # parameterized class constructor
    # @Parameter: puzzle_array
    # 2D array in a 9 rows and 9 columns format representing a Sodoku puzzle
    # Must have at least 17 clues
    def __init__(self, puzzle_array=None):
        self.puzzle_array = None
        if puzzle_array:
            try:
                # set main tkinter window
                root = tkinter.Tk()
                # remove main window
                root.withdraw()
                num_of_clues = 0
                # iterate through array and count how many squares do not equal zero
                for row in range(9):
                    # ensure argument consists of 9 rows and 9 columns
                    if len(puzzle_array[row]) != 9:
                        # create alert box, array not in a 9 row and 9 column format
                        messagebox.showinfo("ERROR!", "Please provide array in a 9 row and 9 column format")
                        break
                    for column in range(9):
                        # ensure argument consists of integers
                        if type(puzzle_array[row][column]) is int:
                            if puzzle_array[row][column] != 0:
                                num_of_clues += 1
                        else:
                            # create alert box, display square not an int message
                            messagebox.showinfo("ERROR!", "Please provide only integers")
                            break
                # Sodoku requires at least 17 clues in order to be solved
                if num_of_clues < 17:
                    # create alert box using tkinter messagebox
                    messagebox.showinfo("ERROR!", "Please provide at least 17 clues.")
                else:
                    # assign argument to object attribute self.puzzle_array
                    self.puzzle_array = puzzle_array
                    self.solve(self.puzzle_array)

            # exception handling
            # generic exception
            except Exception as error:
                # create alert box using tkinter messagebox
                messagebox.showinfo("ERROR!", error)

    # check puzzle_array for value of 0
    def empty(self, puzzle_array):
        """ Returns the coordinates of the next value of puzzle that is zero
        :param puzzle_array:
        :return row, column:
        """
        for row in range(9):
            for column in range(9):
                # If the square is 0, return the row and column of that square
                if puzzle_array[row][column] == 0:
                    return row, column
        return False

    def check_square(self, puzzle_array, row, column, num):
        """ Determine if num is within the row, column or grid. Returns True is num not in row, column, or region
        :param puzzle_array:
        :param row:
        :param column:
        :param num:
        :return bool:
        """
        # Check if num is in the puzzles row, if True return false
        if num in puzzle_array[row]:
            return False
        # Check if the num is in the puzzles column, if True return false
        for x in range(9):
            if puzzle_array[x][column] == num:
                return False
        # Check if the num is the puzzles region, if True return false
        region_row = (row // 3) * 3
        region_column = (column // 3) * 3
        for x in range(region_row, (region_row + 3)):
            for y in range(region_column, (region_column + 3)):
                if puzzle_array[x][y] == num:
                    return False
        return True

    def solve(cls, puzzle_array):
        """ recursively solves each Sodoku object within the Pack object
        :param puzzle_array:
        :return bool:
        """
        # Assign return of next_square() to empty variable
        empty = cls.empty(puzzle_array)
        # if there is no square with value of zero return True
        if not empty:
            return True
        else:
            # If there is a square with the value of zero, assign to row and column variable
            row, column = empty
        # iterate through all the possible number candidates
        for possible_num in range(1, 10):
            # check if the number can be placed within the row, column or region with check_square()
            if cls.check_square(puzzle_array, row, column, possible_num):
                # if check_square returns True, assign that number to the current square
                puzzle_array[row][column] = possible_num
                if cls.solve(puzzle_array):  # Recursively call recursive_solve until False
                    return True
        # if any return is not True, assign current square to zero to backtrack
        puzzle_array[row][column] = 0
        # Return False to break the recursion and backtracking
        return False


# test puzzle array
test_puzzle = [[0, 0, 3, 0, 2, 0, 6, 0, 0], [9, 0, 0, 3, 0, 5, 0, 0, 1], [0, 0, 1, 8, 0, 6, 4, 0, 0],
               [0, 0, 8, 1, 0, 2, 9, 0, 0], [7, 0, 0, 0, 0, 0, 0, 0, 8], [0, 0, 6, 7, 0, 8, 2, 0, 0],
               [0, 0, 2, 6, 0, 9, 5, 0, 0], [8, 0, 0, 2, 0, 3, 0, 0, 9], [0, 0, 5, 0, 1, 0, 3, 0, 0]]

# D:\Documents\PythonProjects\Sodoku\blank puzzles.txt
pack = Puzzles()
for num in range(pack.size):
    print(pack.sodoku[num].puzzle_array)