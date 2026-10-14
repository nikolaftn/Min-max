import sys
import random
from colorama import Fore, Back, init
from copy import deepcopy
import time
state_scores = {}  # hash map for memoization


class Board:
    def __init__(self, size=8):
        self._size = size
        self._grid = [["." for _ in range(size)] for _ in range(size)]


    def display(self):
        # Horizontal line above the board
        print("   " + " ".join(str(c) for c in range(self._size)))
        print("   " + "-"*(self._size*2-1))


        for i, row in enumerate(self._grid):
            print(f"{i} |" + " ".join(row) + "|")


        print("   " + "-"*(self._size*2-1))


    def place_piece(self, row, col, player):
        if row < 0 or row >= self._size or col < 0 or col >= self._size:
            raise ValueError("Position is outside the board!")
        if self._grid[row][col] != '.':
            raise ValueError("The square is occupied!")
        self._grid[row][col] = player


class Game:
    def __init__(self, size=8):
        self._board = Board(size) #board object created
        self._board1 = Board(size)
        self._current_player = "A"
        self._setup_board()


    def _setup_board(self):
        size = self._board._size
        for col in range(size):
            # A moves downward (last two rows)
            if (size-2 + col) % 2 == 0:  # A on white squares
                self._board.place_piece(size-2, col, 'A')
            if (size-1 + col) % 2 == 0:
                self._board.place_piece(size-1, col, 'A')


            # B moves upward (first two rows)
            if (0 + col) % 2 == 1:  # B on black squares
                self._board.place_piece(0, col, 'B')
            if (1 + col) % 2 == 1:
                self._board.place_piece(1, col, 'B')




    def switch_player(self):
        if self._current_player == 'A':
            self._current_player = 'B'
        else:
            self._current_player = 'A'


    def move_piece(self, start_row, start_col, end_row, end_col):
        size = self._board._size


        if not (0 <= end_row < size and 0 <= end_col < size):
            raise ValueError("Target position is outside the board!")


        if self._board._grid[start_row][start_col] != self._current_player:
            raise ValueError("Your piece is not at the starting position!")


        dr = end_row - start_row
        dc = end_col - start_col


        if self._current_player == 'A':
            if dr != -1 and dr != 1:  # must move forward
                raise ValueError("Piece A can only move forward!")
            if dc == 0:
                # Forward: target must be empty
                if self._board._grid[end_row][end_col] != '.':
                    raise ValueError("Target square is occupied!")
            elif abs(dc) == 1:
                # Diagonally forward: target must contain an opponent
                if self._board._grid[end_row][end_col] == self._current_player:
                    raise ValueError("You cannot move onto your own piece!")
            else:
                raise ValueError("Invalid move!")


        elif self._current_player == 'B':
            if dr != 1 and dr != -1:  # B moves upward
                raise ValueError("Piece B can only move forward!")
            if dc == 0:
                if self._board._grid[end_row][end_col] != '.':
                    raise ValueError("Target square is occupied!")
            elif abs(dc) == 1:
                if self._board._grid[end_row][end_col] == self._current_player:
                    raise ValueError("You cannot move onto your own piece!")
            else:
                raise ValueError("Invalid move!")


        # Move the piece
        self._board._grid[start_row][start_col] = '.'
        self._board._grid[end_row][end_col] = self._current_player


        self._board1._grid[start_row][start_col] = '.'
        self._board1._grid[end_row][end_col] = self._current_player


        # Switch player
        self.switch_player()


    def get_valid_moves(self, player):
        size = self._board._size
        moves = []


        if player == 'A':
            direction = [-1, 1]
        else:
            direction = [1, -1]


        for row in range(size):
            for col in range(size):
                if self._board._grid[row][col] == player:


                    #forward
                    new_row = row + direction[0]
                    new_col = col
                    if 0 <= new_row < size and 0 <= new_col < size:
                        if self._board._grid[new_row][new_col] == ".":
                            moves.append(((row, col), (new_row, new_col)))


                    #forward-levo
                    new_row = row + direction[0]
                    new_col = col + direction[0]
                    if 0 <= new_row < size and 0 <= new_col < size:
                        if self._board._grid[new_row][new_col] != player:
                            moves.append(((row, col), (new_row, new_col)))


                    #forward-desno
                    new_row = row + direction[0]
                    new_col = col - direction[0]
                    if 0 <= new_row < size and 0 <= new_col < size:
                        if self._board._grid[new_row][new_col] != player:
                            moves.append(((row, col), (new_row, new_col)))


                    #backward-left
                    new_row = row + direction[1]
                    new_col = col + direction[0]
                    if 0 <= new_row < size and 0 <= new_col < size:
                        if self._board._grid[new_row][new_col] != player:
                            moves.append(((row, col), (new_row, new_col)))


                    #backward-right
                    new_row = row + direction[1]
                    new_col = col - direction[0]
                    if 0 <= new_row < size and 0 <= new_col < size:
                        if self._board._grid[new_row][new_col] != player:
                            moves.append(((row, col), (new_row, new_col)))
        return moves


    def check_winner(self):
        size = self._board._size


        for col in range(size):
            if self._board._grid[0][col] == "A":
                return "A"


        for col in range(size):
            if self._board._grid[size-1][col] == 'B':
                return 'B'


        has_A = any('A' in row for row in self._board._grid)
        has_B = any('B' in row for row in self._board._grid)
        if not has_A:
            return 'B'
        if not has_B:
            return 'A'


        return None


def board_to_key(board: Board):
    return tuple(tuple(row) for row in board._grid)  # tuple of tuples, hashable


def generate_next_steps(game: Game, player):
    moves = game.get_valid_moves(player)
    states = []
    for (start, end) in moves:
        new_game = deepcopy(game)
        new_game._current_player = player
        new_game.move_piece(start[0], start[1], end[0], end[1])
        states.append((new_game, (start, end)))
    return states


def evaluate_board(board: Board):
    player = "B"
    opponent = "A"
    size = board._size
    score = 0
    for r in range(size):
        for c in range(size):
            if board._grid[r][c] == player:
                score += r
            elif board._grid[r][c] == opponent:
                score -= (size - 1 - r)
    return score


def make_move(game: Game, start, end):
    """Move the piece i vrati šta je bilo na cilju (za undo)."""
    sr, sc = start
    er, ec = end
    captured = game._board._grid[er][ec]
    game._board._grid[er][ec] = game._board._grid[sr][sc]
    game._board._grid[sr][sc] = '.'
    return captured


def undo_move(game: Game, start, end, captured):
    """Move the piece back to the start and restore the captured piece."""
    sr, sc = start
    er, ec = end
    game._board._grid[sr][sc] = game._board._grid[er][ec]
    game._board._grid[er][ec] = captured


def minimax(game: Game, depth: int, alpha: int, beta: int, maximizing_player: bool, player: str):
    key = board_to_key(game._board)
    if key in state_scores:
        return state_scores[key]


    winner = game.check_winner()
    if winner == player:
        return 1000
    elif winner is not None:
        return -1000


    if depth == 0:
        score = evaluate_board(game._board)
        state_scores[key] = score
        return score


    if maximizing_player:
        max_value = -float('inf')
        for start, end in game.get_valid_moves("B"):
            captured = make_move(game, start, end)
            value = minimax(game, depth-1, alpha, beta, False, "B")
            undo_move(game, start, end, captured)
            max_value = max(max_value, value)
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        state_scores[key] = max_value
        return max_value
    else:
        min_value = float('inf')
        for start, end in game.get_valid_moves("A"):
            captured = make_move(game, start, end)
            value = minimax(game, depth-1, alpha, beta, True, "A")
            undo_move(game, start, end, captured)
            min_value = min(min_value, value)
            beta = min(value, beta)
            if alpha >= beta:
                break
        state_scores[key] = min_value
        return min_value


def ai_move(game: Game, player="B", max_depth=3):
    best_score = -float("inf")
    best_moves = []


    for next_state, move in generate_next_steps(game, player):
        score = minimax(next_state, max_depth-1, -float('inf'), float('inf'), False, player)


        if score > best_score:
            best_score = score
            best_moves = [move]
        elif score == best_score:
            best_moves.append(move)


    # Filter moves that capture an opponent
    capture_moves = []
    for start, end in best_moves:
        end_row, end_col = end
        if game._board._grid[end_row][end_col] != '.':
            capture_moves.append((start, end))


    if capture_moves:
        chosen_move = random.choice(capture_moves)
    else:
        chosen_move = random.choice(best_moves)


    start, end = chosen_move
    game._current_player = player
    game.move_piece(start[0], start[1], end[0], end[1])
    return end[0], end[1]


def main():
    game = Game()
    size = game._board._size
    game._board1 = deepcopy(game._board)
    backup = deepcopy(game._board)
    while True:
        game._board.display()
        game._board = backup
        if game._current_player == "A":
            valid_moves = game.get_valid_moves('A')
            if not valid_moves:
                print("No more valid moves! Player B wins.")
                return
            print("Your turn.")
            while True:
                start = input("Enter the position of the piece you want to move (row,col): ")
                try:
                    start_split = start.split(",")
                    start_row = int(start_split[0])
                    start_col = int(start_split[1])
                    if not (0 <= start_row < size and 0 <= start_col < size):
                        print("You entered a position that does not exist.")
                        continue
                    if game._board._grid[start_row][start_col] != 'A':
                        print("Your piece is not at the entered position!")
                        continue


                except (ValueError, IndexError):
                    print("Invalid input! Use the format row,col, e.g. 2,3.")


                napred = False
                napred_levo = False
                napred_desno = False
                nazad_levo = False
                nazad_desno = False


                if ((start_row, start_col), (start_row - 1, start_col)) in valid_moves:
                    napred = True
                if ((start_row, start_col), (start_row - 1, start_col - 1)) in valid_moves:
                    napred_levo = True
                if ((start_row, start_col), (start_row - 1, start_col + 1)) in valid_moves:
                    napred_desno = True
                if ((start_row, start_col), (start_row + 1, start_col - 1)) in valid_moves:
                    nazad_levo = True
                if ((start_row, start_col), (start_row + 1, start_col + 1)) in valid_moves:
                    nazad_desno = True


                if not napred and not napred_levo and not napred_desno and not nazad_desno and not nazad_levo:
                    print("There are no valid moves for the selected piece.")
                    continue
                else:
                    if napred:
                        current_value = game._board1._grid[start_row - 1][start_col]
                        game._board1._grid[start_row - 1][start_col] = Back.GREEN + current_value + Back.RESET
                    if napred_levo:
                        current_value = game._board1._grid[start_row - 1][start_col - 1]
                        game._board1._grid[start_row - 1][start_col - 1] = Back.GREEN + current_value + Back.RESET
                    if napred_desno:
                        current_value = game._board1._grid[start_row - 1][start_col + 1]
                        game._board1._grid[start_row - 1][start_col + 1] = Back.GREEN + current_value + Back.RESET
                    if nazad_levo:
                        current_value = game._board1._grid[start_row + 1][start_col - 1]
                        game._board1._grid[start_row + 1][start_col - 1] = Back.GREEN + current_value + Back.RESET
                    if nazad_desno:
                        current_value = game._board1._grid[start_row + 1][start_col + 1]
                        game._board1._grid[start_row + 1][start_col + 1] = Back.GREEN + current_value + Back.RESET
                    game._board1.display()
                    break


            while True:
                move = input("Choose a direction (forward (1), forward-left (2), forward-right (3), backward-left (4), backward-right (5)): ")
                if move.lower() == 'n':
                    break
                elif move == "1" and napred:
                    end_row = start_row - 1
                    end_col = start_col
                elif move == "2" and napred_levo:
                    end_row = start_row - 1
                    end_col = start_col - 1
                elif move == "3" and napred_desno:
                    end_row = start_row - 1
                    end_col = start_col + 1
                elif move == "4" and nazad_levo:
                    end_row = start_row + 1
                    end_col = start_col - 1
                elif move == "5" and nazad_desno:
                    end_row = start_row + 1
                    end_col = start_col + 1
                else:
                    print("Invalid direction!")
                    continue


                try:
                    game.move_piece(start_row, start_col, end_row, end_col)
                    winner = game.check_winner()
                    if winner:
                        game._board.display()
                        print(f"Player {winner} wins!")
                        return
                    game._board1 = deepcopy(game._board)
                    backup = deepcopy(game._board)
                    current_value = game._board._grid[end_row][end_col]
                    game._board._grid[end_row][end_col] = Fore.RED + current_value + Fore.RESET
                    break  # move completed successfully
                except ValueError as e:
                    print(f"Error: {e}")


        else:
            valid_moves = game.get_valid_moves('B')
            if not valid_moves:   # <-- OVO
                print("No more valid moves! Player A wins.")
                return
            print("Computer's turn")
            start_time = time.time()
            end_row, end_col = ai_move(game)
            end_time = time.time()
            print(end_time - start_time)
            winner = game.check_winner()
            if winner:
                game._board.display()
                print(f"Player {winner} wins!")
                return
            backup = deepcopy(game._board)
            current_value = game._board._grid[end_row][end_col]
            game._board._grid[end_row][end_col] = Fore.RED + current_value + Fore.RESET


def main_menu():
    while True:
        print("====Breakthrough====")
        print("1. Start a new game")
        print("2. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            main()  # call the game function here
        elif choice == "2":
            print("Goodbye!")
            sys.exit()
        else:
            print("Invalid menu option.")


if __name__ == "__main__":
    main_menu()
