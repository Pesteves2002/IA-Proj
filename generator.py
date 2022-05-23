
from random import random
from turtle import goto
from takuzu import *
from math import ceil

import os


NUMBER_TESTS = 36

NUMBER_PERMS = 3

DIFFICULTIES = ["easy", "medium", "hard"]

INPUT_NAME = "in_ct"

OUTPUT_NAME = "out_ct"


DIRECTORY = os.getcwd() + "/tests/custom_tests/"


def create(board, num_test):

    file = open(DIRECTORY + INPUT_NAME + str(num_test), 'w')
    size = len(board)

    original_board = []
    for row in board:
        original_board.append(row[:])

    while (True):
        board = []
        for row in original_board:
            board.append(row[:])

        for perm in range(NUMBER_PERMS):
            new_board = []
            row1 = int(random()*size)
            row2 = int(random()*size)
            for i in range(size):
                if (i == row1):
                    new_board.append(board[row2])
                else:
                    if (i == row2):
                        new_board.append(board[row1])
                    else:
                        new_board.append(board[i])
            board = []
            for row in new_board:
                board.append(row[:])
        try:
            play(draw(board))
            break
        except:
            pass
    file.write(draw(board))
    file.close

    file = open(DIRECTORY + OUTPUT_NAME + str(num_test), 'w')
    file.write(draw(play(draw(board))))
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


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.

    board = Board.parse_instance_from_stdin()

    for i in range(NUMBER_TESTS):
        new_board = []
        for row in board.board:
            new_board.append(row[:])
        if (i % 2 == 0):
            new_board = transpose(new_board)
        create(new_board, i)

    # print(goal_node.state.board.disparity_row)
    # print(goal_node.state.board.disparity_col)
    # print(goal_node.state.board.valid)
    # print(goal_node.state.board.row_binary)
    # print(goal_node.state.board.col_binary)


pass
