from board import Board


def main():
    board: Board = Board()
    row = board.row(board[3][4])
    column = board.column(board[3][4])

    print(f"board[3][4]:\t{board[3][4]}")
    print(f"row[0]:\t\t\t{row[0]}")
    print(f"column[0]:\t\t{column[0]}")
    print(f"board.value:\t{board.value}")
    pass


if __name__ == '__main__':
    main()
