WHITE, BLACK = 1, 2


class Figure:  # Базовый класс для фигур
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Queen(Figure):  # Ферзь
    def char(self):
        return 'Q'

    def can_move(self, board, row, col, row1, col1):
        bishop = (row + col == row1 + col1) or (
                row - col == row1 - col1)  # ходит как слон
        rook = row == row1 or col == col1  # ходит как ладья

        if not (bishop or rook):
            return False

        if col == col1:  # движение по вертикали
            step = 1 if row1 > row else -1
            for r in range(row + step, row1, step):
                if not board[r][col] is None:
                    return False
            return True

        if row == row1:  # движение по горизонтали
            step = 1 if col1 > col else -1
            for c in range(col + step, col1, step):
                if not board[row][c] is None:
                    return False
            return True

        if row - col == row1 - col1:  # движение по диагонали параллельной главной
            step = 1 if row1 > row else -1
            for r in range(row + step, row1, step):
                c = r - row + col
                if not board[r][c] is None:
                    return False
            return True

        # движение по диагонали параллельной побочной
        step = 1 if row1 > row else -1
        for r in range(row + step, row1, step):
            c = row + col - r
            if not board[r][c] is None:
                return False
        return True


class Rook(Figure):  # Ладья
    def char(self):
        return 'R'

    def can_move(self, board, row, col, row1, col1):
        '''Невозможно сделать ход в клетку, которая не лежит в том же ряду
        или столбце клеток.'''
        if row != row1 and col != col1:
            return False
        return True


class Bishop(Figure):  # Слон
    def char(self):
        return 'B'

    def can_move(self, board, row, col, row1, col1):
        t1 = row - col == row1 - col1
        t2 = row + col == row1 + col1
        return t1 and t2


class Knight(Figure):  # Конь
    def can_move(self, board, row, col, row1, col1):
        res = (row != row1 and col != col1) and (
                abs(row - row1) + abs(col - col1) == 3)
        return res

    def char(self):
        return 'N'


class King(Figure):  # Король
    def char(self):
        return 'K'

    def can_move(self, board, row, col, row1, col1):
        delta_row = abs(row1 - row)
        delta_col = abs(col1 - col)
        return (delta_row <= 1 and delta_col <= 1)


class Pawn(Figure):  # Пешка
    def char(self):
        return 'P'

    def can_move(self, board, row, col, row1, col1):
        # Пешка может ходить только по вертикали
        # "взятие на проходе" не реализовано

        if not board[row1][col1] is None:
            return False

        if col != col1:
            return False

        # Пешка может сделать из начального положения ход на 2 клетки
        # вперёд, поэтому поместим индекс начального ряда в start_row.
        if self.color == WHITE:
            direction = 1
            start_row = 1
        else:
            direction = -1
            start_row = 6

        # ход на 1 клетку
        if row + direction == row1:
            return True

        # ход на 2 клетки из начального положения
        if (row == start_row
                and row + 2 * direction == row1
                and board[row + direction][col] is None):
            return True

        # Проверка, что пешка может съесть фигуру

    def can_attack(self, board, row, col, row1, col1):
        if board[row1][col1] is None:
            return False
        if board[row1][col1].get_color() == board[row][col].get_color():
            return False
        direction = 1 if (self.color == WHITE) else -1
        return (row + direction == row1
                and (col + 1 == col1 or col - 1 == col1))
