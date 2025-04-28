WHITE, BLACK = 1, 2


class Queen:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

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
                if not board.field[r][col] is None:
                    return False
            return True

        if row == row1:  # движение по горизонтали
            step = 1 if col1 > col else -1
            for c in range(col + step, col1, step):
                if not board.field[row][c] is None:
                    return False
            return True

        if row - col == row1 - col1:  # движение по диагонали параллельной главной
            step = 1 if row1 > row else -1
            for r in range(row + step, row1, step):
                c = r - row + col
                if not board.field[r][c] is None:
                    return False
            return True

        # движение по диагонали параллельной побочной
        step = 1 if row1 > row else -1
        for r in range(row + step, row1, step):
            c = row + col - r
            if not board.field[r][c] is None:
                return False
        return True


class Rook:  # Ладья
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'R'

    def can_move(self, board, row, col, row1, col1):
        '''Невозможно сделать ход в клетку, которая не лежит в том же ряду
        или столбце клеток.'''
        if row != row1 and col != col1:
            return False
        return True


class Bishop:  # Слон
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'B'

    def can_move(self, board, row, col, row1, col1):
        t1 = row - col == row1 - col1
        t2 = row + col == row1 + col1
        return t1 and t2


class Knight:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def can_move(self, board, row, col, row1, col1):
        res = (row != row1 and col != col1) and (
                abs(row - row1) + abs(col - col1) == 3)
        return res

    def char(self):
        return 'N'


class King:
    def __init__(self, color):
        self.color = color

    def char(self):
        return 'K'

    def get_color(self):
        return self.color

    def can_move(self, board, row, col, row1, col1):
        if abs(row1 - row) > 1 or abs(col1 - col):
            return False
        return True


class Pawn:

    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

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
                and board.field[row + direction][col] is None):
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


class Board:
    def __init__(self):
        self.color = WHITE
        self.field = []
        for row in range(8):
            self.field.append([None] * 8)
        self.field[0] = [
            Rook(WHITE), Knight(WHITE), Bishop(WHITE), Queen(WHITE),
            King(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)
        ]
        self.field[1] = [
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE),
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE)
        ]
        self.field[6] = [
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK),
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK)
        ]
        self.field[7] = [
            Rook(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK),
            King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)
        ]

    @staticmethod
    def correct_coords(row, col):
        """Функция проверяет, что координаты (row, col) лежат
        внутри доски"""
        return 0 <= row < 8 and 0 <= col < 8

    @staticmethod
    def opponent(color):
        return WHITE if color == BLACK else BLACK

    def current_player_color(self):
        return self.color

    def cell(self, row, col):
        """Возвращает строку из двух символов. Если в клетке (row, col)
        находится фигура, символы цвета и фигуры. Если клетка пуста,
        то два пробела."""
        piece = self.field[row][col]
        if piece is None:
            return '  '
        color = piece.get_color()
        c = 'w' if color == WHITE else 'b'
        return c + piece.char()

    def get_piece(self, row, col):
        if self.correct_coords(row, col):
            return self.field[row][col]
        else:
            return None

    def move_piece(self, row, col, row1, col1):
        """Переместить фигуру из точки (row, col) в точку (row1, col1).
        Если перемещение возможно, метод выполнит его и вернёт True.
        Если нет --- вернёт False"""

        if not self.correct_coords(row, col) or not self.correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False  # нельзя пойти в ту же клетку
        piece = self.field[row][col]
        if piece is None:
            return False
        if piece.get_color() != self.color:  # цвет хода должжен совпадать с цветом фигуры
            return False
        if self.field[row1][col1] is None:
            if not piece.can_move(self.field, row, col, row1, col1):
                return False
        elif self.field[row1][col1].get_color() == self.opponent(piece.get_color()):
            if not piece.can_attack(self.field, row, col, row1, col1):
                return False
        elif self.field[row1][col1].get_color() == piece.get_color():  # нельзя съесть свою фигуру
            return False
        else:
            return False
        self.field[row][col] = None  # Снять фигуру.
        self.field[row1][col1] = piece  # Поставить на новое место.
        self.color = self.opponent(self.color)
        return True

    def move_and_promote_pawn(self, row, col, row1, col1, char):

        pawn: Pawn = self.field[row][col]  # пешка
        if not isinstance(pawn, Pawn):
            return False
        if (pawn.can_move(self.field, row, col, row1, col1) or
                pawn.can_attack(self.field, row, col, row1, col1)):  # если пешка может пойти в клетку (row1, col1)
            color = pawn.get_color()  # цвет пешки
            self.move_piece(row, col, row1, col1)
            if char == 'R':
                self.field[row1][col1] = Rook(color)
            elif char == 'N':
                self.field[row1][col1] = Knight(color)
            elif char == 'Q':
                self.field[row1][col1] = Queen(color)
            elif char == 'K':
                self.field[row1][col1] = King(color)
            elif char == 'B':
                self.field[row1][col1] = Bishop(color)
            return True

        return False
