WHITE, BLACK = 1, 2


class Pawn:  # Пешка
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'P'


class Rook:  # Ладья
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'R'


class Bishop:  # Слон
    def __init__(self, color):
        self.color = color

    def char(self):
        return 'B'

    def get_color(self):
        return self.color


class Knight:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'N'


class King:
    def __init__(self, color):
        self.color = color

    def char(self):
        return 'K'

    def get_color(self):
        return self.color


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
        return 0 <= row < 8 and 0 <= col < 8

    @staticmethod
    def opponent(color):
        return WHITE if color == BLACK else BLACK

    def current_player_color(self):
        return self.color

    def cell(self, row, col):
        '''Возвращает строку из двух символов. Если в клетке (row, col)
        находится фигура, символы цвета и фигуры. Если клетка пуста,
        то два пробела.'''
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
        '''Переместить фигуру из точки (row, col) в точку (row1, col1).
        Если перемещение возможно, метод выполнит его и вернёт True.
        Если нет --- вернёт False'''

        if not self.correct_coords(row, col) or not self.correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False  # нельзя пойти в ту же клетку
        piece = self.field[row][col]
        if piece is None:
            return False
        if piece.get_color() != self.color:
            return False
        if self.field[row1][col1] is None:
            if not piece.can_move(self, row, col, row1, col1):
                return False
        elif self.field[row1][col1].get_color() == opponent(piece.get_color()):
            if not piece.can_attack(self, row, col, row1, col1):
                return False
        else:
            return False
        self.field[row][col] = None  # Снять фигуру.
        self.field[row1][col1] = piece  # Поставить на новое место.
        self.color = self.opponent(self.color)
        return True


class Queen:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'Q'

    def can_move(self, board, row, col, row1, col1):
        if board.field[row][col] is None:
            return False
        bishop = (row + col == row1 + col1) or (
                row - col == row1 - col1)  # ходит как слон
        in_board = (0 <= row1 < 8) and (0 <= col1 < 8)  # находится в поле
        rook = row == row1 or col == col1  # ходит как ладья

        if not (in_board and (rook or bishop)):
            return False

        if row == row1 and col == col1:  # нельзя пойти в ту же клетку
            return False

        if not board.field[row1][col1] is None and board.field[row1][col1].get_color() == \
                board.field[row][col].get_color():  # нельзя съесть свою фигуру
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

    # def set_position(self, row, col, row1, col1):

