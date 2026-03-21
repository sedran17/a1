from typing import Callable, Optional

# These functions are imported for you to use
# in your implementation.
from src import (
    find_lines,
    get_possible_moves,
    get_score,
    play_move,
    eprint      # for debugging
)

# Use this global variable for state caching.
# You may find that it's useful to use the following
# information to form a key into the
#
#       (board, player_to_move, limit, node_type)
#
state_cache = {}


###############################################################################
############################# VALUE FUNCTIONS #################################
###############################################################################
def compute_utility(board: tuple[tuple[int, ...], ...], color: int) -> int:
    """
    Return the utility value of the given board for the given player color.

    :param board: a board representing the current state of an Othello game
    :param color: the color of the player. 1 for dark, 2 for light.

    :return: the utility of the given board for the given player color.
    """
    dark, light = get_score(board)
    if color == 1:
        return dark - light
    elif color == 2:
        return light - dark
    else:
        return None

def compute_heuristic(board: tuple[tuple[int, ...], ...], color: int) -> int:
    """
    Return the heuristic value of the given board for the given player color.

    :param board: a board representing the current state of an Othello game
    :param color: the color of the player. 1 for dark, 2 for light.

    :return: the heuristic value of the given board for the given player color.
    """
    dark, light = get_score(board)
    if color == 1:
        return light - dark
    elif color == 2:
        return dark - light
    else:
        return None


###############################################################################
####################### ALPHA-BETA PRUNING FUNCTIONS ##########################
###############################################################################
def alphabeta_min_node(
        value_fn: Callable,
        board: tuple[tuple[int, ...], ...],
        color: int,
        alpha: int,
        beta: int,
        limit: int,
        caching: int = 0,
        ordering: int = 0) -> tuple[Optional[tuple[int, int]], int]:
    """
    Return a tuple of the move that yields the *lowest* possible utility
    and the *lowest* possible utility itself for the given board, color,
    limit, value_fn to determine utility and alpha, beta to prune.
    Optionally use state caching and node ordering.

    :param value_fn: function used to determine utility values
    :param board: the current state of the Othello game
    :param color: the color of the current player (1 for dark, 2 for light)
    :param alpha: the alpha parameter, used in pruning
    :param beta: the beta parameter, used in pruning
    :param limit: the depth limit of the alpha-beta search
    :param caching: whether to use state caching
                    if 1, use state caching
                    if 0, do not use state caching
    :param ordering: whether to order moves during move selection

    :return: a tuple (None|(i,j), utility) of the next move to be
             taken, and the utility value associated with it
    """
    # TODO: Implement
    raise RuntimeError("Method not implemented")  # Replace this line!

def alphabeta_max_node(
        value_fn: Callable,
        board: tuple[tuple[int, ...], ...],
        color: int,
        alpha: int,
        beta: int,
        limit: int,
        caching: int = 0,
        ordering: int = 0) -> tuple[Optional[tuple[int, int]], int]:
    """
    Return a tuple of the move that yields the *highest* possible utility
    and the *highest* possible utility itself for the given board, color,
    limit, value_fn to determine utility and alpha, beta to prune.
    Optionally use state caching and node ordering.

    :param value_fn: function used to determine utility values
    :param board: the current state of the Othello game
    :param color: the color of the current player (1 for dark, 2 for light)
    :param alpha: the alpha parameter, used in pruning
    :param beta: the beta parameter, used in pruning
    :param limit: the depth limit of the alpha-beta search
    :param caching: whether to use state caching
                    if 1, use state caching
                    if 0, do not use state caching
    :param ordering: whether to order moves during move selection

    :return: a tuple (None|(i,j), utility) of the next move to be
             taken, and the utility value associated with it
    """
    # TODO: Implement
    raise RuntimeError("Method not implemented")  # Replace this line!

def select_move_alphabeta(
        value_fn: Callable,
        board: tuple[tuple[int, ...], ...],
        color: int,
        limit: int = -1,
        caching: int = 0,
        ordering: int = 0) -> Optional[tuple[int, int]]:
    """
    Return the next move determined by alpha-beta pruning in a game of Othello
    defined by the given board, player color, depth limit, and use of caching
    and node ordering. Use value_fn to determine utility values in subroutines.

    :param value_fn: function used to determine utility values
    :param board: the current state of the Othello game
    :param color: the color of the current player (1 for dark, 2 for light)
    :param limit: the depth limit of the alpha-beta search
    :param caching: whether to use state caching
                    if 1, use state caching
                    if 0, do not use state caching
    :param ordering: whether to order moves during move selection

    :return: a tuple (i, j) of the next move to be taken, or None
    """
    # TODO: Implement
    raise RuntimeError("Method not implemented")  # Replace this line!


###############################################################################
############################# MINIMAX FUNCTIONS ###############################
###############################################################################
def minimax_min_node(
        value_fn: Callable,
        board: tuple[tuple[int, ...], ...],
        color: int,
        limit: int,
        caching: int = 0) -> tuple[Optional[tuple[int, int]], int]:
    """
    Return a tuple of the move that yields the lowest possible utility
    and the lowest possible utility itself for the given board, color,
    limit, using value_fn to determine utility. Optionally use state caching
    and node ordering.

    The algorithm is outlined as follows:
        1. Get all allowed moves
        2. Check if we are at a terminal state
        3. If not, minimize over the set of max utility values for each possible move

    :param value_fn: function used to determine utility values
    :param board: the current state of the Othello game
    :param color: the color of the current player (1 for dark, 2 for light)
    :param limit: the depth limit of the Minimax search
    :param caching: whether to use state caching in Minimax
                    if 1, use state caching
                    if 0, do not use state caching

    :return: a tuple (None|(i,j), utility) of the next move to be
             taken, and the utility value associated with it
    """
    moves = get_possible_moves(board, color)
    best_move = (None, float("inf"))
    opp_color = 2
    if color == 2:
        opp_color = 1
    if len(moves) == 0:
        return None, compute_utility(board, opp_color)
    else:
        opp_color = 2
        if color == 2:
            opp_color = 1
        for move in moves:
            new_board = play_move(board, color, move[0], move[1])
            new_move = minimax_max_node(value_fn, new_board, opp_color, limit)

            if new_move[1] < best_move[1]:
                best_move = (move, new_move[1])
        return best_move

def minimax_max_node(
        value_fn: Callable,
        board: tuple[tuple[int, ...], ...],
        color: int,
        limit: int,
        caching: int = 0) -> tuple[Optional[tuple[int, int]], int]:
    """
    Return a tuple of the move that yields the highest possible utility
    and the highest possible utility itself for the given board, color,
    limit, using value_fn to determine utility. Optionally use state caching
    and node ordering.

    The algorithm is outlined as follows:
        1. Get all allowed moves
        2. Check if we are at a terminal state
        3. If not, maximize over the set of min utility values for each possible move

    :param value_fn: function used to determine utility values
    :param board: the current state of the Othello game
    :param color: the color of the current player (1 for dark, 2 for light)
    :param limit: the depth limit of the Minimax search
    :param caching: whether to use state caching in Minimax
                    if 1, use state caching
                    if 0, do not use state caching

    :return: a tuple (None|(i,j), utility) of the next move to be
             taken, and the utility value associated with it
    """
    moves = get_possible_moves(board, color)
    best_move = (None, float("-inf"))
    opp_color = 2
    if color == 2:
        opp_color = 1
    if len(moves) == 0:
        return None, compute_utility(board, color)
    else:
        for move in moves:
            new_board = play_move(board, color, move[0], move[1])
            new_move = minimax_min_node(value_fn, new_board, opp_color, limit)

            if new_move[1] > best_move[1]:
                best_move = (move, new_move[1])
        return best_move



def select_move_minimax(
        value_fn: Callable,
        board: tuple[tuple[int, ...], ...],
        color: int,
        limit: int,
        caching: int = 0) -> Optional[tuple[int, int]]:
    """
    Return the next move determined by Minimax in a game of Othello
    defined by the given board, player color, depth limit, and use of caching.
    Uses value_fn to determine utility values in subroutines.

    :param value_fn: function used to determine utility values
    :param board: the current state of the Othello game
    :param color: the color of the current player (1 for dark, 2 for light)
    :param limit: the depth limit of the Minimax search
    :param caching: whether to use state caching
                    if 1, use state caching
                    if 0, do not use state caching

    :return: a tuple (i, j) of the next move to be taken, or None
    """
    move, _ = minimax_max_node(value_fn, board, color, limit)
    return move


###############################################################################
############################### ENTRY-POINT ###################################
###############################################################################
def run_ai():
    """
    Communicate with the game manager to simulate a player in a game
    of Othello. Accepts input from stdin to determine:
        * color    - 1 for dark, 2 for light
        * limit    - the depth limit
        * minimax  - 1 to run minimax, otherwise run alpha-beta
        * caching  - 1 to run with caching, otherwise run without it
        * ordering - 1 to run alpha-beta with node ordering,
                     otherwise run without it.

    Use `compute_utility` as the value function by default.
    """
    print("Othello AI")  # First line is the name of this AI
    color, limit, minimax, caching, ordering = map(int, input().split(","))

    eprint("Running MINIMAX") if minimax else eprint("Running ALPHA-BETA")
    eprint("State Caching is ON") if caching else eprint("State Caching is OFF")
    eprint("Node Ordering is ON") if ordering else eprint("Node Ordering is OFF")
    eprint("Depth Limit is ", limit) if limit >= 0 else eprint("Depth Limit is OFF")

    while True:
        # Read the current state of the game as yielded by the game manager.
        # Consists of a string of the form:
        #
        #       (SCORE|FINAL) \d+ \d+    , e.g. SCORE 9 7
        #
        # The first string is the state of the game:
        #   * SCORE indicates that the game is still active.
        #   * FINAL indicates that the game is over.
        #
        # The first digit is the score for player 1 (the dark player.)
        #
        # The second digit is the score for player 2 (the light player.)
        status, _, _ = input().strip().split()

        if status == "FINAL":
            break
        else:
            # Read the current board represented as a tuple of tuples, where
            # nested tuples represent rows of the board. For example:
            #
            #   ((0, 0, 0, 0),
            #    (0, 2, 1, 0),
            #    (0, 1, 2, 0),
            #    (0, 0, 0, 0))
            #
            # where
            #
            #   * 0 - an empty square on the board
            #   * 1 - a piece played by player 1, or the dark player.
            #   * 2 - a piece played by player 2, or the light player.
            board = eval(input())

            if (minimax == 1):
                i, j = select_move_minimax(
                    compute_utility,
                    board,
                    color,
                    limit,
                    caching
                )
            else:
                i, j = select_move_alphabeta(
                    compute_utility,
                    board,
                    color,
                    limit,
                    caching,
                    ordering
                )

            print("{} {}".format(i, j))


if __name__ == "__main__":
    run_ai()
