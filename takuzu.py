# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 02:
# 99202 Diogo Melita
# 99341 Tomás Esteves

import sys

import time

from numpy import transpose, floor
from pyparsing import originalTextFor

from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_graph_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
    depth_first_graph_search,
    iterative_deepening_search,
    depth_limited_search,
    compare_searchers,
)


def complementary_value(value):
    if value == 0:
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
        self.num_actions = 1

    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if row >= self.size or col >= self.size or row < 0 or col < 0:
            return 2
        return self.board[row][col]

    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
        if row <= 0:
            upper = None
            lower = self.board[row + 1][col]
        else:
            if row + 1 >= self.size:
                upper = self.board[row - 1][col]
                lower = None
            else:
                upper = self.board[row - 1][col]
                lower = self.board[row + 1][col]

        return (lower, upper)

    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""

        if col <= 0:
            left = None
            right = self.board[row][col + 1]
        else:
            if col + 1 >= self.size:
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
                if cell == 0:
                    row_disparity["number_0"] += 1
                if cell == 1:
                    row_disparity["number_1"] += 1
                if cell == 2:
                    this_board.spots_left += 1
                    row_disparity["blank_spots"] += 1
            this_board.disparity_row.append(row_disparity)
        this_board.blank_spots = this_board.get_blank_spots()

        board_transposed = transpose(this_board.board)

        for col in board_transposed:
            col_disparity = {"number_0": 0, "number_1": 0, "blank_spots": 0}
            for cell in col:
                if cell == 0:
                    col_disparity["number_0"] += 1
                if cell == 1:
                    col_disparity["number_1"] += 1
                if cell == 2:
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
                if self.get_number(row, col) == 2:
                    blank_spots.append((row, col))
        return blank_spots

    def update_disparity_values(self, row: int, col: int, value: int):
        """Atualiza os valores de disparidade na linha e coluna e reduz o número de espaços brancos na linha e coluna"""
        if value == 0:
            self.disparity_row[row]["number_0"] += 1
            self.disparity_col[col]["number_0"] += 1
        else:
            self.disparity_row[row]["number_1"] += 1
            self.disparity_col[col]["number_1"] += 1

        self.disparity_row[row]["blank_spots"] -= 1
        self.disparity_col[col]["blank_spots"] -= 1

    def check_completed_row_or_col(self, coord: int, row_or_col: str):
        """Verifica se a linha ou coluna se encontra duplicada no tabuleiro"""
        if row_or_col == "row":
            line = self.board[coord]
            binary_values = self.row_binary
            disparity_line = self.disparity_row[coord]
        else:
            transposed_board = transpose(self.board)
            line = transposed_board[coord]
            binary_values = self.col_binary
            disparity_line = self.disparity_col[coord]

        # Transforma-se o número binário em decimal, verificamos na lista se há igual
        sum = 0
        i = self.size - 1
        for value in line:
            sum += value * (2**i)
            i -= 1
        if sum not in binary_values:
            binary_values.append(sum)
        else:
            self.valid = False

        # Verifica-se se existe o mesmo número de 0's e de 1's
        if self.size % 2 == 0:
            if disparity_line["number_0"] != disparity_line["number_1"]:
                self.valid = False
        # Verifica-se se a diferença entre número de 0's e de 1's é igual a 1
        else:
            if abs(disparity_line["number_0"] - disparity_line["number_1"]) != 1:
                self.valid = False

    def decrease_spots_left(self, row: int, col: int, value: int):
        """Processa tudo sobre introduzir um número ao tabuleiro."""
        self.spots_left -= 1

        self.update_disparity_values(row, col, value)

        # Se linha já não tiver espaços vazios, verifica se já não há uma linha igual
        if self.disparity_row[row]["blank_spots"] == 0:
            self.check_completed_row_or_col(row, "row")

        # Se coluna já não tiver espaços vazios, verifica se já não há uma coluna igual
        if self.disparity_col[col]["blank_spots"] == 0:
            self.check_completed_row_or_col(col, "col")


class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = TakuzuState(board)

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""

        # Se o tabuleiro for inválido não se retorna ações
        if not state.board.valid:
            return []

        blank_spots = state.board.blank_spots

        # Procura alguma ação obrigatória
        legal_actions = self.find_mandatory_place(state.board, blank_spots)

        # Se não há ações obrigatória, envia-se o par de ações da próxima casa vazia
        if legal_actions == []:
            for i in range(2):
                legal_actions.append((blank_spots[0][0], blank_spots[0][1], i))
        state.board.num_actions = len(legal_actions)

        return legal_actions

    def find_mandatory_place(self, board, blank_spots):
        """Retorna uma ação no caso de saber que é obrigatória ela ser feita"""
        for blank_spot in blank_spots:
            row_value = blank_spot[0]
            col_value = blank_spot[1]

            # No caso de as casas de um número já estarem preenchidas
            # podemos devolver a ação mas temos de verificar se o tabuleiro continua válido
            if board.size % 2 == 0:
                size_divided = board.size / 2
            else:
                size_divided = int(floor(board.size / 2)) + 1

            if board.disparity_row[row_value]["number_0"] == size_divided:
                if self.check_3_inline(board, (row_value, col_value, 1)) == []:
                    board.valid = False
                return [(row_value, col_value, 1)]
            if board.disparity_row[row_value]["number_1"] == size_divided:
                if self.check_3_inline(board, (row_value, col_value, 0)) == []:
                    board.valid = False
                return [(row_value, col_value, 0)]
            if board.disparity_col[col_value]["number_0"] == size_divided:
                if self.check_3_inline(board, (row_value, col_value, 1)) == []:
                    board.valid = False
                return [(row_value, col_value, 1)]
            if board.disparity_col[col_value]["number_1"] == size_divided:
                if self.check_3_inline(board, (row_value, col_value, 0)) == []:
                    board.valid = False
                return [(row_value, col_value, 0)]

            possible_action = self.check_only_possible_action(
                board, (row_value, col_value)
            )
            if possible_action != []:
                return possible_action

        return []

    def check_3_inline(self, board: Board, action):
        """Se houver ao fazer a ação ficarem 3 números de seguida devolve-se a lista vazia"""

        COORDS_TO_CHECK = [
            [0, -2, 0, -1],
            [0, 2, 0, 1],
            [0, 1, 0, -1],
            [-2, 0, -1, 0],
            [2, 0, 1, 0],
            [1, 0, -1, 0],
        ]

        row_value = action[0]
        col_value = action[1]
        num_to_insert = action[2]

        for coords in COORDS_TO_CHECK:
            row_offset_1 = row_value + coords[0]
            col_offset_1 = col_value + coords[1]
            row_offset_2 = row_value + coords[2]
            col_offset_2 = col_value + coords[3]

            if (
                board.get_number(row_offset_1, col_offset_1)
                == num_to_insert
                == board.get_number(row_offset_2, col_offset_2)
            ):
                return []

        return [action]

    def check_only_possible_action(self, board: Board, action):
        """Se houver 2 casas de seguidas com a mesma posição, devolve-se a ação que coloca o número contrário a essas casas"""

        COORDS_TO_CHECK = [
            [0, -2, 0, -1],
            [0, 2, 0, 1],
            [0, 1, 0, -1],
            [-2, 0, -1, 0],
            [2, 0, 1, 0],
            [1, 0, -1, 0],
        ]

        row_value = action[0]
        col_value = action[1]

        for coords in COORDS_TO_CHECK:
            row_offset_1 = row_value + coords[0]
            col_offset_1 = col_value + coords[1]
            row_offset_2 = row_value + coords[2]
            col_offset_2 = col_value + coords[3]

            if (
                board.get_number(row_offset_1, col_offset_1)
                == board.get_number(row_offset_2, col_offset_2)
                != 2
            ):
                return [
                    (
                        row_value,
                        col_value,
                        complementary_value(
                            board.get_number(row_offset_1, col_offset_1)
                        ),
                    )
                ]

        return []

    def create_new_board(self, old_board: Board, action) -> Board:
        """Retorna um novo tabuleiro depois de efetuada a ação"""
        new_board = Board()
        new_board.size = old_board.size
        new_board.spots_left = old_board.spots_left
        new_board.valid = old_board.valid
        new_board.num_actions = old_board.num_actions

        # Copia o antigo tabuleiro
        for row in old_board.board:
            new_board.board.append(row[:])

        # Copia a disparidade das linhas
        for row in old_board.disparity_row:
            new_board.disparity_row.append(dict(row))

        # Copia a disparidade das colunas
        for col in old_board.disparity_col:
            new_board.disparity_col.append(dict(col))

        # Copia os binários
        new_board.row_binary = old_board.row_binary[:]
        new_board.col_binary = old_board.col_binary[:]

        # Copia as posições vazias
        new_board.blank_spots = old_board.blank_spots[:]

        # Faz a ação
        new_board.board[action[0]][action[1]] = action[2]

        # Remove o espaço vazio onde foi feita a ação
        new_board.blank_spots.remove((action[0], action[1]))

        # Processa o tabuleiro com a ação feita
        new_board.decrease_spots_left(action[0], action[1], action[2])

        return new_board

    def result(self, state: TakuzuState, action) -> TakuzuState:
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""

        new_board = self.create_new_board(state.board, action)
        new_state = TakuzuState(new_board)

        return new_state

    def goal_test(self, state: TakuzuState) -> bool:
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        return state.board.get_spots_left() == 0 and state.board.valid

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        action = node.action
        if action != None:
            # Retorna a casa mais longe, onde action está mais em baixo,
            # e com os spots left para dar prioridade a um jogo q ja esteja a acabar

            return (
                node.state.board.spots_left
                + (node.state.board.size - 1 - action[0])
                * 1
                / node.state.board.num_actions
            )
        return 0


if __name__ == "__main__":
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.

    board = Board.parse_instance_from_stdin()

    problem = Takuzu(board)

    compare_searchers(
        [problem],
        "----",
        searchers=[depth_first_graph_search, greedy_search, astar_search],
    )

    SEARCHES = ["BFS", "DFS", "GREEDY", "A*"]

    for search in SEARCHES:
        start = time.time()
        if search == SEARCHES[0]:
            # goal_node = breadth_first_tree_search(problem)
            print("NULL")

        if search == SEARCHES[1]:
            goal_node = depth_first_tree_search(problem)

        if search == SEARCHES[2]:
            goal_node = greedy_search(problem)

        if search == SEARCHES[3]:
            # goal_node = astar_search(problem)
            print("NULL")

        end = time.time()
        print(search, end - start)

    # print(goal_node.state.board)

pass
