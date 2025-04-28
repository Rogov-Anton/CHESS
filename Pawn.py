WHITE, BLACK = 1, 2


# Функция для вычисления цвета противника
def opponent(color):
    return WHITE if color == BLACK else BLACK


def print_board(board):  # Распечатать доску в текстовом виде
    print('     +----+----+----+----+----+----+----+----+')
    for row in range(7, -1, -1):
        print(' ', row, end='  ')
        for col in range(8):
            print('|', board.cell(row, col), end=' ')
        print('|')
        print('     +----+----+----+----+----+----+----+----+')
    print(end='        ')
    for col in range(8):
        print(col, end='    ')
    print()


def coords_in_field(row, col):
    """Функция проверяет, что координаты (row, col) лежат
    внутри доски"""
    return 0 <= row < 8 and 0 <= col < 8


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

    def can_attack(self, board, row, col, row1, col1):
        direction = 1 if (self.color == WHITE) else -1
        return (row + direction == row1
                and (col + 1 == col1 or col - 1 == col1))


class Board:
    def __init__(self):
        self.color = WHITE
        self.field = []
        for row in range(8):
            self.field.append([None] * 8)
        self.field[1][4] = Pawn(WHITE)
        self.field[2][3] = Pawn(BLACK)

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
        if piece.get_color() != self.color:
            return False
        if self.field[row1][col1] is None:
            if not piece.can_move(self, row, col, row1, col1):
                return False
        elif self.field[row1][col1].get_color() == self.opponent(piece.get_color()):
            if not piece.can_attack(self, row, col, row1, col1):
                return False
        else:
            return False
        self.field[row][col] = None  # Снять фигуру.
        self.field[row1][col1] = piece  # Поставить на новое место.
        self.color = self.opponent(self.color)
        return True

    def move_and_promote_pawn(self, row, col, row1, col1, char):
        pawn: Pawn = self.field[row][col]  # пешка
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


board = Board()
board.field = [([None] * 8) for i in range(8)]
board.field[6][3] = Pawn(WHITE)
board.field[7][4] = Rook(BLACK)

print('before:')
for row in range(7, -1, -1):
    for col in range(8):
        char = board.cell(row, col)[1]
        print(char.replace(' ', '-'), end='')
    print()
print()

board.move_and_promote_pawn(6, 3, 7, 4, 'N')

print('after:')
for row in range(7, -1, -1):
    for col in range(8):
        char = board.cell(row, col)[1]
        print(char.replace(' ', '-'), end='')
    print()

color = board.get_piece(7, 4).get_color()
color_str = 'white' if color == WHITE else 'black'
print(color_str)
