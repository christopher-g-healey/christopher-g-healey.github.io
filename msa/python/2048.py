# - 2048.PY ---------------------------------------------------------- #
#   Python implementation of 2048 tile game                            #
#                                                                      #
# - When: ----- Who: ------------------ Comments: -------------------- #
#                                                                      #
# 08-18-23     Christopher G. Healey   Initial implementation          #
# -------------------------------------------------------------------- #

import copy
import keyboard
import random

EMPTY = 0  # Empty board constant
done = False  # Game finished flag

# Playing board, value is value of entry in square, 0 means empty;
# board is top-to-bottom row-major, so first sublist is top row,
# second is second row, etc.

board_sz = 4
board = [
    [EMPTY] * board_sz,
    [EMPTY] * board_sz,
    [EMPTY] * board_sz,
    [EMPTY] * board_sz,
]


def board_down():
    """Update board for push down"""

    global board
    global done

    if done:  # Ignore command if program is done
        return

    # Perform a downward push

    for c in range(0, board_sz):  # For all columns
        merge = False

        for r in range(board_sz - 2, -1, -1):  # For top n-1 rows
            if board[r][c] == EMPTY:  # Nothing to push?
                continue

            merge_loop = False
            while r <= board_sz - 2:  # Space to try pushing down?
                if board[r + 1][c] == EMPTY:  # Move value down
                    board[r + 1][c] = board[r][c]
                    board[r][c] = EMPTY

                elif not merge and (  # No merge and matching squares, merge
                    board[r + 1][c] == board[r][c]
                ):  # Combine values
                    board[r + 1][c] *= 2
                    board[r][c] = EMPTY
                    merge = True

                elif (
                    merge
                    and (  # Already merged and matching squares, blocked,
                        board[r + 1][c] == board[r][c]
                    )
                ):
                    break

                elif board[r + 1][c] != board[r][c]:  # Blocked
                    break

                r += 1


# End function board_down


def board_left():
    """Update board for push left"""

    global board
    global done

    if done:  # Ignore command if program is done
        return

    # Perform a leftward push

    for r in range(0, board_sz):  # For all rows
        merge = False

        for c in range(1, board_sz):  # For right n-1 columns
            if board[r][c] == EMPTY:  # Nothing to push?
                continue

            while c >= 1:  # Space to try pushing left?
                if board[r][c - 1] == EMPTY:  # Move value left
                    board[r][c - 1] = board[r][c]
                    board[r][c] = EMPTY

                elif not merge and (  # No merge and matching squares, merge
                    board[r][c - 1] == board[r][c]
                ):  # Combine values
                    board[r][c - 1] *= 2
                    board[r][c] = EMPTY
                    merge = True

                elif merge and (  # Already merged and matching squares, blocked
                    board[r][c - 1] == board[r][c]
                ):
                    break

                elif board[r][c - 1] != board[r][c]:  # Blocked
                    break

                c -= 1


# End function board_left


def board_right():
    """Update board for push right"""

    global board
    global done

    if done:  # Ignore command if program is done
        return

    # Perform a rightward push

    for r in range(0, board_sz):  # For all rows
        merge = False

        for c in range(board_sz - 2, -1, -1):  # For left n-1 columns
            if board[r][c] == EMPTY:  # Nothing to push?
                continue

            while c <= board_sz - 2:  # Space to try pushing right?
                if board[r][c + 1] == EMPTY:  # Move value right
                    board[r][c + 1] = board[r][c]
                    board[r][c] = EMPTY

                elif not merge and (  # No merge and matching squares, merge
                    board[r][c + 1] == board[r][c]
                ):  # Combine values
                    board[r][c + 1] *= 2
                    board[r][c] = EMPTY
                    merge = True

                elif merge and (  # Already merged and matching squares, blocked
                    board[r][c + 1] == board[r][c]
                ):
                    break

                elif board[r][c + 1] != board[r][c]:  # Blocked
                    break

                c += 1


# End function board_right


def board_up():
    """Update board for push up"""

    global board
    global done

    if done:  # Ignore command if program is done
        return

    # Perform an upward push

    for c in range(0, board_sz):  # For all columns
        merge = False

        for r in range(1, board_sz):  # For bottom n-1 rows
            if board[r][c] == EMPTY:  # Nothing to push?
                continue

            while r >= 1:  # Space to try pushing up?
                if board[r - 1][c] == EMPTY:  # Move value up
                    board[r - 1][c] = board[r][c]
                    board[r][c] = EMPTY

                elif not merge and (  # No merge and matching squares, merge
                    board[r - 1][c] == board[r][c]
                ):  # Combine values
                    board[r - 1][c] *= 2
                    board[r][c] = EMPTY
                    merge = True

                elif merge and (  # Already merged and matching squares, blocked
                    board[r - 1][c] == board[r][c]
                ):
                    break

                elif board[r - 1][c] != board[r][c]:  # Blocked?
                    break

                r -= 1


# End function board_up


def empty_count():
    """Return count of empty squares

    Returns:
        int: Number of empty squares
    """
    global board

    n = 0
    for r in range(0, board_sz):
        for c in range(0, board_sz):
            if board[r][c] == EMPTY:
                n += 1

    return n


# End function empty_count


def lose():
    """Check for board full and no valid moves, player lost"""

    global board
    global done

    # Simulate left/right/up/down to see if any valid moves exist

    board_cp = copy.deepcopy(board)  # Save copy of current board

    board_down()
    n = empty_count()
    board = copy.deepcopy(board_cp)
    if n > 0:
        return

    board_left()
    n = empty_count()
    board = copy.deepcopy(board_cp)
    if n > 0:
        return

    board_right()
    n = empty_count()
    board = copy.deepcopy(board_cp)
    if n > 0:
        return

    board_up()
    n = empty_count()
    board = copy.deepcopy(board_cp)
    if n > 0:
        return

    sum = 0
    for r in range(0, board_sz):
        for c in range(0, board_sz):
            sum += board[r][c]

    print("\nSorry, no valid moves are left. You lost.")
    print(f"Your score was {sum}.")
    print("Press ESCAPE to end the game.")
    done = True


# End function lose


def print_board():
    """Print current board state"""

    global board

    for r in range(0, board_sz):  # For all rows
        for c in range(0, board_sz):  # For all columns
            if board[r][c] == EMPTY:  # Show empty square as hyphen
                print("  -  ", end="")
            else:
                print(f"{board[r][c]:4d} ", end="")
        print()

    for i in range(0, board_sz):
        print("-----", end="")
    print()


# End function print_board


def push_down(k):
    """Push board down

    Args:
        k (event): Keyboard event
    """
    global board

    print("\u2193")
    board_down()

    update_board(1)  # Add 2 to random position
    print_board()

    win()
    lose()


# End function push_down


def push_left(k):
    """Push board left

    Args:
        k (event): Keyboard event
    """

    global board

    # Elements in first column can't move, so stop at second column

    print("\u2190")
    board_left()

    update_board(1)  # Add 2 to random position
    print_board()

    win()
    lose()


# End function push_left


def push_right(k):
    """Push board right

    Args:
        k (event): Keyboard event
    """

    global board

    print("\u2192")
    board_right()

    update_board(1)  # Add 2 to random position
    print_board()

    win()
    lose()


# End function push_right


def push_up(k):
    """Push board up

    Args:
        k (event): Keyboard event
    """

    global board

    print("\u2191")
    board_up()

    update_board(1)  # Add 2 to random position
    print_board()

    win()
    lose()


# End function push_up


def update_board(n):
    """Update board by placing random 2's in empty squares

    Args:
        n (int): Number of 2's to palce
    """

    global board

    # If less than n positions exist, fill as many positions as possible

    if n > empty_count():
        print(f"update_board(), {n} positions requested, {empty_count()} exist")
        n = empty_count()

    # Choose n random positions to place value 2

    r = random.randrange(0, board_sz)
    c = random.randrange(0, board_sz)
    count = 0

    while count != n:
        if board[r][c] == 0:
            board[r][c] = 2
            count += 1

        r = random.randrange(0, board_sz)
        c = random.randrange(0, board_sz)


# End function init_board


def win():
    """Check for square with 2048, player won"""

    global board
    global done

    for r in range(0, board_sz):
        for c in range(0, board_sz):
            if board[r][c] == 2048:
                print("\nCongratulations! You won.")
                print("Press ESCAPE to end the game.")
                done = True


# End function win


# Mainline

print("\nWelcome to 2048.")
print("Press ESCAPE at any time to terminate the game.\n")

update_board(2)
print_board()

# Use keyboard module to catch arrow key presses

keyboard.on_press_key("down arrow", push_down)
keyboard.on_press_key("left arrow", push_left)
keyboard.on_press_key("right arrow", push_right)
keyboard.on_press_key("up arrow", push_up)

keyboard.wait("escape")

print("\nAll done")
