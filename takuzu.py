# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 02:
# 99202 Diogo Melita
# 99341 Tomás Esteves

import sys

from numpy import transpose, floor

from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_graph_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


def complementary_value(value):
    if (value == 0):
        return 1
    return 0


class TakuzuState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = TakuzuState.state_id
        TakuzuState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Takuzu."""

    def __init__(self) -> None:
        self.board = []
        self.size = 0
        self.spots_left = 0
        self.blank_spots = []
        self.disparity_row = []
        self.disparity_col = []
        self.row_binary = []
        self.col_binary = []
        self.valid = True

    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if (row >= self.size or col >= self.size or row < 0 or col < 0):
            return 2
        return self.board[row][col]

    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
        if (row <= 0):
            upper = None
            lower = self.board[row+1][col]
        else:
            if(row + 1 >= self.size):
                upper = self.board[row - 1][col]
                lower = None
            else:
                upper = self.board[row - 1][col]
                lower = self.board[row+1][col]

        return (lower, upper)

    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""

        if (col <= 0):
            left = None
            right = self.board[row][col+1]
        else:
            if(col + 1 >= self.size):
                left = self.board[row][col - 1]
                right = None
            else:
                left = self.board[row][col - 1]
                right = self.board[row][col + 1]

        return (left, right)

    @staticmethod
    def parse_instance_from_stdin():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 takuzu.py < input_T01

            > from sys import stdin
            > stdin.readline()
        """

        this_board = Board()

        for line in sys.stdin:
            if this_board.size == 0:
                this_board.size = int(line.strip())
            else:
                new_row = line.strip().split("\t")
                this_board.board.append(list(map(int, new_row)))

        for row in this_board.board:
            row_disparity = {"number_0": 0, "number_1": 0, "blank_spots": 0}
            for cell in row:
                if (cell == 0):
                    row_disparity["number_0"] += 1
                if (cell == 1):
                    row_disparity["number_1"] += 1
                if (cell == 2):
                    this_board.spots_left += 1
                    row_disparity["blank_spots"] += 1
            this_board.disparity_row.append(row_disparity)
        this_board.blank_spots = this_board.get_blank_spots()

        board_transposed = transpose(this_board.board)

        for col in board_transposed:
            col_disparity = {"number_0": 0, "number_1": 0, "blank_spots": 0}
            for cell in col:
                if (cell == 0):
                    col_disparity["number_0"] += 1
                if (cell == 1):
                    col_disparity["number_1"] += 1
                if (cell == 2):
                    col_disparity["blank_spots"] += 1
            this_board.disparity_col.append(col_disparity)

        return this_board

    # TODO: outros metodos da classe

    def __str__(self):
        """Devolve string com a representação de output do tabuleiro."""
        board_string = ""
        for row in self.board:
            for cell in row:
                board_string += str(cell) + "\t"
            board_string = board_string[:-1]
            board_string += "\n"

        return board_string[:-1]

    def get_spots_left(self) -> int:
        """Devolve o número de lugares vazios do tabuleiro."""
        return self.spots_left

    def get_blank_spots(self):
        """Devolve as coordenadas das posições livres do tabuleiro."""
        blank_spots = []
        for row in range(self.size):
            for col in range(self.size):
                if (self.get_number(row, col) == 2):
                    blank_spots.append((row, col))
        return blank_spots

    def decrease_spots_left(self, row: int, col: int, value: int):
        """Processa tudo sobre introduzir um número ao tabuleiro."""
        self.spots_left -= 1
        # update disparity values
        if (value == 0):
            self.disparity_row[row]["number_0"] += 1
            self.disparity_col[col]["number_0"] += 1
        else:
            self.disparity_row[row]["number_1"] += 1
            self.disparity_col[col]["number_1"] += 1

        self.disparity_row[row]["blank_spots"] -= 1
        self.disparity_col[col]["blank_spots"] -= 1

        if (self.disparity_row[row]["blank_spots"] == 0):
            sum = 0
            i = self.size - 1
            for value in self.board[row]:
                sum += value * (2 ** i)
                i -= 1
            if sum not in self.row_binary:
                self.row_binary.append(sum)
            else:
                self.valid = False

            if self.size % 2 == 0:
                if (self.disparity_row[row]["number_0"] != self.disparity_row[row]["number_1"]):
                    self.valid = False
            else:
                if (abs(self.disparity_row[row]["number_0"] - self.disparity_row[row]["number_1"]) != 1):
                    self.valid = False

        if (self.disparity_col[col]["blank_spots"] == 0):
            sum = 0
            i = self.size - 1
            board_transpose = transpose(self.board)
            for value in board_transpose[col]:
                sum += value * (2 ** i)
                i -= 1
            if sum not in self.col_binary:
                self.col_binary.append(sum)
            else:
                self.valid = False
            if self.size % 2 == 0:
                if (self.disparity_col[col]["number_0"] != self.disparity_col[col]["number_1"]):
                    self.valid = False
            else:
                if (abs(self.disparity_col[col]["number_0"] - self.disparity_col[col]["number_1"]) != 1):
                    self.valid = False


class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = TakuzuState(board)
        pass

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""

        if not state.board.valid:
            return []
        blank_spots = state.board.blank_spots

        legal_actions = self.find_mandatory_place(state.board, blank_spots)

        if legal_actions == []:
            for i in range(2):
                legal_actions.append(
                    (blank_spots[0][0], blank_spots[0][1], i))
        return legal_actions
        pass

    def find_mandatory_place(self, board, blank_spots):
        for blank_spot in blank_spots:
            row_value = blank_spot[0]
            col_value = blank_spot[1]

            # In case all values of the other number are already filled we can just put the complementary
            if (board.size % 2 == 0):
                if (board.disparity_row[row_value]["number_0"] == board.size/2):
                    if (self.check_3_inline(board, [(row_value, col_value, 1)]) == []):
                        board.valid = False
                    return[(row_value, col_value, 1)]
                if (board.disparity_row[row_value]["number_1"] == board.size/2):
                    if (self.check_3_inline(board, [(row_value, col_value, 0)]) == []):
                        board.valid = False
                    return[(row_value, col_value, 0)]
                if (board.disparity_col[col_value]["number_0"] == board.size/2):
                    if (self.check_3_inline(board, [(row_value, col_value, 1)]) == []):
                        board.valid = False
                    return[(row_value, col_value, 1)]
                if (board.disparity_col[col_value]["number_1"] == board.size/2):
                    if (self.check_3_inline(board, [(row_value, col_value, 0)]) == []):
                        board.valid = False
                    return[(row_value, col_value, 0)]
            else:
                if (board.disparity_row[row_value]["number_0"] == (int(floor(board.size/2)) + 1)):
                    if (self.check_3_inline(board, [(row_value, col_value, 1)]) == []):
                        board.valid = False
                    return[(row_value, col_value, 1)]
                if (board.disparity_row[row_value]["number_1"] == (int(floor(board.size/2)) + 1)):
                    if (self.check_3_inline(board, [(row_value, col_value, 0)]) == []):
                        board.valid = False
                    return[(row_value, col_value, 0)]
                if (board.disparity_col[col_value]["number_0"] == (int(floor(board.size/2)) + 1)):
                    if (self.check_3_inline(board, [(row_value, col_value, 1)]) == []):
                        board.valid = False
                    return[(row_value, col_value, 1)]
                if (board.disparity_col[col_value]["number_1"] == (int(floor(board.size/2)) + 1)):
                    if (self.check_3_inline(board, [(row_value, col_value, 0)]) == []):
                        board.valid = False
                    return[(row_value, col_value, 0)]
            # left
            if (board.get_number(row_value, col_value - 2) == board.get_number(row_value, col_value - 1) != 2):
                return [(row_value, col_value, complementary_value(board.get_number(row_value, col_value - 1)))]
            # right
            if (board.get_number(row_value, col_value + 2) == board.get_number(row_value, col_value + 1) != 2):
                return [(row_value, col_value, complementary_value(board.get_number(row_value, col_value + 1)))]

            # middle horizontal
            if (board.get_number(row_value, col_value + 1) == board.get_number(row_value, col_value - 1) != 2):
                return [(row_value, col_value, complementary_value(board.get_number(row_value, col_value - 1)))]

            # above
            if (board.get_number(row_value - 2, col_value) == board.get_number(row_value - 1, col_value) != 2):
                return [(row_value, col_value, complementary_value(board.get_number(row_value - 1, col_value)))]

            # below
            if (board.get_number(row_value + 2, col_value) == board.get_number(row_value + 1, col_value) != 2):

                return [(row_value, col_value, complementary_value(board.get_number(row_value + 1, col_value)))]

            # middle vertical
            if (board.get_number(row_value + 1, col_value) == board.get_number(row_value - 1, col_value) != 2):
                return [(row_value, col_value, complementary_value(board.get_number(row_value - 1, col_value)))]

        return []

    def disparity(self, board, actions):
        new_legal_actions = []

        for action in actions:
            row_value = action[0]
            col_value = action[1]
            num_to_insert = action[2]
            if num_to_insert == 0:
                num_to_insert = -1

            if board.size % 2 == 0:
                limit = 0
            else:
                limit = 1

            value_row = abs(
                board.disparity_row[row_value]["number_0"] - board.disparity_row[row_value]["number_1"])
            value_col = abs(
                board.disparity_col[col_value]["number_0"] - board.disparity_col[col_value]["number_1"])

            if(value_row - board.disparity_row[row_value]["blank_spots"] > limit):
                continue

            if(value_col - board.disparity_col[col_value]["blank_spots"] > limit):
                continue

            new_legal_actions.append(action)

        return new_legal_actions

    def check_3_inline(self, board, actions):
        new_legal_actions = []
        for legal_action in actions:
            row_value = legal_action[0]
            col_value = legal_action[1]
            num_to_insert = legal_action[2]
            # left
            if (board.get_number(row_value, col_value - 2) == num_to_insert == board.get_number(row_value, col_value - 1)):
                continue
            # right
            if (board.get_number(row_value, col_value + 2) == num_to_insert == board.get_number(row_value, col_value + 1)):
                continue
            # middle horizontal
            if (board.get_number(row_value, col_value + 1) == num_to_insert == board.get_number(row_value, col_value - 1)):
                continue
            # above
            if (board.get_number(row_value - 2, col_value) == num_to_insert == board.get_number(row_value - 1, col_value)):
                continue
            # below
            if (board.get_number(row_value + 2, col_value) == num_to_insert == board.get_number(row_value + 1, col_value)):
                continue
            # middle vertical
            if (board.get_number(row_value + 1, col_value) == num_to_insert == board.get_number(row_value - 1, col_value)):
                continue

            new_legal_actions.append(legal_action)
        return new_legal_actions

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO

        new_board = Board()
        new_board.size = state.board.size
        new_board.spots_left = state.board.spots_left
        for row in state.board.board:
            new_board.board.append(row[:])

        for row in state.board.disparity_row:
            new_board.disparity_row.append(dict(row))

        for col in state.board.disparity_col:
            new_board.disparity_col.append(dict(col))

        new_board.board[action[0]][action[1]] = action[2]

        new_board.row_binary = state.board.row_binary[:]
        new_board.col_binary = state.board.col_binary[:]

        new_board.blank_spots = state.board.blank_spots[:]
        new_board.blank_spots.remove((action[0], action[1]))
        new_board.valid = state.board.valid
        new_board.decrease_spots_left(action[0], action[1], action[2])
        new_state = TakuzuState(new_board)
        return new_state
        pass

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        # TODO
        return state.board.get_spots_left() == 0 and state.board.valid
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.

    board = Board.parse_instance_from_stdin()

    problem = Takuzu(board)

    goal_node = depth_first_tree_search(problem)

    print(goal_node.state.board)
    # print(goal_node.state.board.disparity_row)
    # print(goal_node.state.board.disparity_col)
    # print(goal_node.state.board.valid)
    # print(goal_node.state.board.row_binary)
    # print(goal_node.state.board.col_binary)


pass
