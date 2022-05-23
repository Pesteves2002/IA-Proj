
from random import random
from turtle import goto
from takuzu import *
from math import ceil

import os


MAX_PUZZLE_SIZE = 36

DIFFICULTIES = ["easy", "medium", "hard"]

INPUT_NAME = "ct"


DIRECTORY = os.getcwd() + "/tests/custom_tests/"


def get_number_gen(board, size, row: int, col: int) -> int:
    """Devolve o valor na respetiva posição do tabuleiro."""
    if (row >= size or col >= size or row < 0 or col < 0):
        return 2
    return board[row][col]


def check_3_inline_gen(board, actions):
    new_legal_actions = []
    size = len(board)
    for legal_action in actions:

        row_value = legal_action[0]
        col_value = legal_action[1]
        num_to_insert = legal_action[2]
        # left
        if (get_number_gen(board, size, row_value, col_value - 2) == num_to_insert == get_number_gen(board, size, row_value, col_value - 1)):
            continue
        # right
        if (get_number_gen(board, size, row_value, col_value + 2) == num_to_insert == get_number_gen(board, size, row_value, col_value + 1)):
            continue
        # middle horizontal
        if (get_number_gen(board, size, row_value, col_value + 1) == num_to_insert == get_number_gen(board, size, row_value, col_value - 1)):
            continue
        # above
        if (get_number_gen(board, size, row_value - 2, col_value) == num_to_insert == get_number_gen(board, size, row_value - 1, col_value)):
            continue
        # below
        if (get_number_gen(board, size, row_value + 2, col_value) == num_to_insert == get_number_gen(board, size, row_value + 1, col_value)):
            continue
        # middle vertical
        if (get_number_gen(board, size, row_value + 1, col_value) == num_to_insert == get_number_gen(board, size, row_value - 1, col_value)):
            continue

        new_legal_actions.append(legal_action)
    return new_legal_actions


def disparity_gen(row_num, col_num, board_row, board_col, action):
    size = len(board_row)
    if size % 2 == 0:
        if (board_col[col_num]["number_0"] > size/2 or board_col[col_num]["number_1"] > size/2):
            return []
        if (board_row[row_num]["number_0"] > size/2 or board_row[row_num]["number_1"] > size/2):
            return []
    else:
        if (board_col[col_num]["number_0"] > ceil(size/2) or board_col[col_num]["number_1"] > ceil(size/2)):
            return []
        if (board_row[row_num]["number_0"] > ceil(size/2) or board_row[row_num]["number_1"] > ceil(size/2)):
            return []
    return [1]


def generate(num_test, puzzle_size, difficulty):

    if (0 < num_test < 10):
        num_test = "00" + str(num_test)
    else:
        if (10 <= num_test < 99):
            num_test = "0" + str(num_test)
    file = open(DIRECTORY + INPUT_NAME + str(num_test), 'w')
    if (difficulty == "easy"):
        remaining_houses = puzzle_size**2 * 5/7
    if (difficulty == "medium"):
        remaining_houses = puzzle_size**2 * 3/5
    if (difficulty == "hard"):
        remaining_houses = puzzle_size**2 * 1/2
    remaining_houses = int(remaining_houses)
    save_remaining_houses = remaining_houses
    while (True):
        remaining_houses = save_remaining_houses

        board = []
        board_row = []
        board_col = []
        for n in range(puzzle_size):
            row = []
            for m in range(puzzle_size):
                row.append(2)
            board.append(row)
            board_row.append({"number_0": 0, "number_1": 0,
                             "blank_spots": puzzle_size})
            board_col.append({"number_0": 0, "number_1": 0,
                             "blank_spots": puzzle_size})

        while remaining_houses > 0:
            row_num = int(random() * puzzle_size)
            col_num = int(random() * puzzle_size)

            if board[row_num][col_num] == 2:
                action = round(random())
                if check_3_inline_gen(board, [(row_num, col_num, action)]) != []:
                    if disparity_gen(row_num, col_num, board_row, board_col, action) != []:
                        print(remaining_houses)
                        if (action == 0):
                            board_row[row_num]["number_0"] += 1
                            board_col[col_num]["number_0"] += 1
                        else:
                            board_row[row_num]["number_1"] += 1
                            board_col[col_num]["number_1"] += 1
                        board_row[row_num]["blank_spots"] -= 1
                        board_col[col_num]["blank_spots"] -= 1
                        board[row_num][col_num] = action
                        remaining_houses -= 1
                    else:
                        continue
        try:
            play(draw(board))
            break
        except:
            draw(board)
            print("")

    file.write(draw(board))
    file.close


def draw(array):
    board_string = ""
    board_string += str(len(array)) + "\n"
    for row in array:
        for cell in row:
            board_string += str(cell) + "\t"
        board_string = board_string[:-1]
        board_string += "\n"

    return board_string[:-1]


i = 1
for n in range(4, MAX_PUZZLE_SIZE):
    for dif in DIFFICULTIES:
        generate(i, n, dif)
        i += 1
