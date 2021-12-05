from pathlib import Path

SIDE_LENGTH = 5

class Board:
    def __init__(self, raw: str):
        board = []
        lines = raw.split("\n")
        for line in lines:
            row = [int(cell) for cell in line.split()]
            board.append(row)
        self.board = board
        self.marked = set()

    def __str__(self):
        result = ""
        for row_num, row in enumerate(self.board):
            for col_num, cell in enumerate(row):
                if (row_num, col_num) in self.marked:
                    result += f"({cell})\t"
                else:
                    result += f"{cell}\t"
            result += "\n"
        return result

    def mark(self, called_num: int):
        for row_num, row in enumerate(self.board):
            for col_num, cell in enumerate(row):
                if cell == called_num:
                    self.marked.add((row_num, col_num))

    def has_won(self):
        for i in range(SIDE_LENGTH):
            # check rows
            if len([1 for (row, _) in self.marked if row == i]) == SIDE_LENGTH:
                return True
            # check cols
            if len([1 for (_, col) in self.marked if col == i]) == SIDE_LENGTH:
                return True
        return False

    def sum_unmarked(self):
        total = 0
        unmarked = []
        for row_num, row in enumerate(self.board):
            for col_num, cell in enumerate(row):
                if (row_num, col_num) in self.marked:
                    continue
                total += cell
                unmarked.append(cell)
        return total

def get_sections():
    text = Path("problem_04.txt").read_text()
    return text.split("\n\n")

def get_nums_and_boards():
    sections = get_sections()
    called_str = sections.pop(0)
    nums_called = [int(num) for num in called_str.split(",")]
    boards = [Board(raw) for raw in sections]
    return (nums_called, boards)

def part_a():
    nums_called, boards = get_nums_and_boards()

    for called_num in nums_called:
        for board in boards:
            board.mark(called_num)
            if board.has_won():
                return called_num * board.sum_unmarked()


def part_b():
    nums_called, boards = get_nums_and_boards()

    for called_num in nums_called:
        for board in boards:
            board.mark(called_num)
        last_board = boards[0]
        boards = [board for board in boards if not board.has_won()]
        if not boards:
            return called_num * last_board.sum_unmarked()

print(part_a())
print(part_b())
