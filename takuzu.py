# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

import sys


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

    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.board[row][col]
        pass

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
        pass

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

        pass

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
            for cell in row:
                if (cell == 2):
                    this_board.spots_left += 1

        this_board.blank_spots = this_board.get_blank_spots()

        return this_board

    # TODO: outros metodos da classe

    def __str__(self):
        board_string = ""
        for row in self.board:
            for cell in row:
                board_string += str(cell) + "\t"
            board_string += "\n"
        return board_string

    def get_spots_left(self):
        return self.spots_left

    def get_blank_spots(self):
        blank_spots = []
        for row in range(self.size):
            for col in range(self.size):
                if (self.get_number(row, col) == 2):
                    blank_spots.append((row, col))
        return blank_spots

    def decrease_spots_left(self):
        self.spots_left -= 1


class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        # TODO
        self.initial = TakuzuState(board)
        pass

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        legal_actions = []
        blank_spots = state.board.blank_spots
        for blank_spot in blank_spots:
            vertical_adjancies = state.board.adjacent_vertical_numbers(
                blank_spot[0], blank_spot[1])
            horizontal_adjancies = state.board.adjacent_horizontal_numbers(
                blank_spot[0], blank_spot[1])
            if (vertical_adjancies != (0, 0) and horizontal_adjancies != (0, 0)):
                legal_actions.append((blank_spot[0], blank_spot[1], 0))
            if (vertical_adjancies != (1, 1) and horizontal_adjancies != (1, 1)):
                legal_actions.append((blank_spot[0], blank_spot[1], 1))
        return legal_actions
        pass

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

        new_board.board[action[0]][action[1]] = action[2]

        new_board.blank_spots = state.board.blank_spots[:]
        new_board.blank_spots.remove((action[0], action[1]))
        new_board.decrease_spots_left()
        new_state = TakuzuState(new_board)
        return new_state
        pass

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        # TODO
        return state.board.get_spots_left() == 0
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
    print(board)

    problem = Takuzu(board)

    goal_node = depth_first_tree_search(problem)

    print("Is goal?", problem.goal_test(goal_node.state))
    print("Solution:\n", goal_node.state.board, sep="")


pass
