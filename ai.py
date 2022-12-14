import math
from numpy import float64, ndarray
from board import Board


class AI:
    def __init__(self, board: Board, depth: int) -> None:
        self.board = board
        self.depth = depth

    def generateDecision(self) -> list[int, int]:
        return self.maximumPlayer(self.board.copy(), self.depth, -99999, 99999)

    def maximumPlayer(self, board: Board, depth: int, alpha: int, beta: int) -> list[int, int]:
        score = self.score(board.data)
        if depth == 0:
            return [None, score]

        _, cols = board.data.shape
        # Column, score
        maxValue = [None, -99999]

        for col in range(cols):
            new_board = board.copy()
            if not new_board.is_valid_location(col):
                continue
            new_board.drop_piece(col, 2)
            next_move = self.minimizePlayer(new_board, depth - 1, alpha, beta)
            if next_move[1] > maxValue[1]:
                maxValue[0] = col
                maxValue[1] = next_move[1]
            if maxValue[1] >= beta:
                break
            alpha = max(alpha, maxValue[1])
        return maxValue

    def minimizePlayer(self, board: Board, depth: int, alpha: int, beta: int) -> list[int, int]:
        score = self.score(board.data)
        if depth == 0:
            return [None, score]

        _, cols = board.data.shape
        # Column, score
        minValue = [None, 99999]

        for col in range(cols):
            new_board = board.copy()
            if not new_board.is_valid_location(col):
                continue
            new_board.drop_piece(col, 1)
            next_move = self.maximumPlayer(new_board, depth - 1, alpha, beta)
            if next_move[1] < minValue[1]:
                minValue[0] = col
                minValue[1] = next_move[1]
            if minValue[1] <= alpha:
                break
            beta = min(beta, minValue[1])
        return minValue

    def score(self, data: ndarray[float64]) -> int:
        rows, cols = data.shape
        vertical_points = 0
        horizontal_points = 0
        diagonal1_points = 0
        diagonal2_points = 0

        for row in range(rows - 3):
            for col in range(cols):
                score = self.score_position(data, row, col, 1,  0)
                vertical_points += score
        for row in range(rows):
            for col in range(cols - 3):
                score = self.score_position(data, row, col, 0, 1)
                horizontal_points += score
        for row in range(rows - 3):
            for col in range(cols - 3):
                score = self.score_position(data, row, col, 1, 1)
                diagonal1_points += score
        for row in range(3, rows):
            for col in range(cols - 3):
                score = self.score_position(data, row, col, -1, 1)
                diagonal2_points += score

        return vertical_points + horizontal_points + diagonal1_points + diagonal2_points

    def score_position(self, data: ndarray[float64], row: int, col: int, delta_y: int, delta_x: int):
        human_point = 0
        ai_point = 0

        for _ in range(4):
            if data[row][col] == 1:
                human_point += 1
            elif data[row][col] == 2:
                ai_point += 1
            row += delta_y
            col += delta_x

        if human_point == 4:
            return -10000
        if ai_point == 4:
            return 10000
        if human_point == ai_point == 0:
            return 0
        if human_point == 0:
            return math.pow(3, ai_point - 1)
        if ai_point == 0:
            return -math.pow(3, human_point - 1)
        return 0
