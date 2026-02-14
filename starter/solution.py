#   You may only add standard python imports
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files
from typing import Callable, Union

import os                       # For time functions
import math                     # For infinity

from src import (
    # For search engine implementations
    SearchEngine, SearchNode, SearchStatistics,
    # For Sokoban-specific implementations
    SokobanState,
    sokoban_goal_state,
    UP, DOWN, LEFT, RIGHT,
    # You may further import any constants you may need.
    # See `search_constants.py`
)

# SOKOBAN HEURISTICS
def heur_alternate(state: 'SokobanState') -> float:


    boxes = list(state.boxes)
    storage = list(state.storage)
    walls = state.obstacles

    # -------------------------
    # 1️⃣ Corner Deadlock Check
    # -------------------------
    for (x, y) in boxes:

        # If box already on storage, skip
        if (x, y) in state.storage:
            continue

        # Check 4 corner configurations
        if ((x-1, y) in walls and (x, y-1) in walls) or \
           ((x-1, y) in walls and (x, y+1) in walls) or \
           ((x+1, y) in walls and (x, y-1) in walls) or \
           ((x+1, y) in walls and (x, y+1) in walls):

            return float('inf')  # Dead state

    # -----------------------------------
    # 2️⃣ Optimal Matching via Backtracking
    # -----------------------------------

    n = len(boxes)
    used = [False] * len(storage)

    def backtrack(i):
        if i == n:
            return 0

        min_cost = float('inf')

        for j in range(len(storage)):
            if not used[j]:
                used[j] = True

                cost = abs(boxes[i][0] - storage[j][0]) + \
                       abs(boxes[i][1] - storage[j][1])

                total = cost + backtrack(i + 1)

                if total < min_cost:
                    min_cost = total

                used[j] = False

        return min_cost

    return backtrack(0)


def heur_zero(state: 'SokobanState') -> float:
    """
    This function is used in A* to perform a uniform cost search
    by returning zero.

    :param state: A SokobanState object representing the current
                  state in a game of Sokoban.
    :return: The zero value.
    """
    return 0

def heur_manhattan_distance(state: 'SokobanState') -> float:
    # IMPLEMENT
    """
    Returns an admissible - i.e. optimistic - heuristic by never
    overestimating the cost to transition from the current state to the goal state.
    The sum of the Manhattan distances between each box that has yet to be stored
    and the storage point nearest to it qualifies as such a heuristic.

    You may assume there are no obstacles on the grid when calculating distances.
    You must implement this function exactly as specified.

    :param state: A SokobanState object representing the current
                  state in a game of Sokoban.
    :return: An admissible estimate of the distance from the
             current SokobanState to the goal state.
    """
    dist = 0
    for box in state.boxes:
        min_dist = float('inf')
        for stor in state.storage:
            new_dist = abs(box[0] - stor[0]) + abs(box[1] - stor[1])
            if new_dist < min_dist:
                min_dist = new_dist
        dist += min_dist

    return dist

def fval_function(node: 'SearchNode', weight: float) -> float:
    """
    Returns the f-value of the state contained in node
    based on weight, to be used in Anytime Weighted A* search.

    :param node: A SearchNode object containing a SokobanState object
    :param weight: The weight used in Anytime Weighted A* search.
    :return: The f-value of the state contained in node.
    """
    return node.gval + weight*node.hval

# SEARCH ALGORITHMS
def weighted_astar(
        initial_state: 'SokobanState',
        heur_fn: Callable,
        weight: float,
        timebound: int) -> tuple[Union['SokobanState', bool], 'SearchStatistics']:
    """
    Returns a tuple of the goal SokobanState and a SearchStatistics object
    by implementing weighted A* search as defined in the handout.

    If no goal state is found, returns a tuple of False and a SearchStatistics
    object.

    :param initial_state: The initial SokobanState of the game of Sokoban.
    :param heur_fn: The heuristic function used in weighted A* search.
    :param weight: The weight used in calculating the heuristic.
    :param timebound: The time bound used in weighted A* search, in seconds.
    :return: A tuple consisting of the goal SokobanState or False if such a state
             is not found, and a SearchStatistics object.
    """
    wrap_fn = lambda sN: fval_function(sN, weight)

    search_eng = SearchEngine(strategy='custom')
    search_eng.init_search(initial_state, sokoban_goal_state, heur_alternate, wrap_fn)

    return search_eng.search(timebound)

def iterative_astar( # uses f(n)
        initial_state: 'SokobanState',
        heur_fn: Callable,
        weight: float = 1,
        timebound: int = 5) -> tuple[Union['SokobanState', bool], 'SearchStatistics']:
    """
    Returns a tuple of the goal SokobanState and a SearchStatistics object
    by implementing realtime iterative A* search as defined in the handout.

    If no goal state is found, returns a tuple of False and a SearchStatistics
    object.

    Refer to test_alternate_fun in autograder.py to see how to initialize a search.

    :param initial_state: The initial SokobanState of the game of Sokoban.
    :param heur_fn: The heuristic function used in realtime iterative A* search.
    :param weight: The weight used in calculating the heuristic.
    :param timebound: The time bound used in realtime iterative A* search, in seconds.
    :return: A tuple consisting of the goal SokobanState or False if such a state
             is not found, and a SearchStatistics object.
    """
    
    start = os.times()[0]
    max_cost = float('inf')
    best_soln = None
    first_call = True


    while True:
        #Create search engine
        wrap_fn = lambda sN: fval_function(sN, weight)

        search_eng = SearchEngine(strategy='custom')
        search_eng.init_search(initial_state, sokoban_goal_state, heur_alternate, wrap_fn)

        #Update Time
        time_left = timebound - (os.times()[0] - start)

        #Check to see if Under time
        if not first_call:
            if time_left <= 0:
                if best_soln is not None:
                    return best_soln
                else:
                    return result

        #Search
        result = search_eng.search(time_left, (float('inf'), float('inf'), max_cost))
        if first_call and result[0] == False:
            return result
        first_call = False

        if result[0] == False:
            if best_soln is not None:
                return best_soln
            else:
                return result

        #Update cost
        cost = result[0].gval
        if cost < max_cost:
            max_cost = cost
            best_soln = result

        #Update Weight
        if weight <= 1:
            return best_soln
        else:
            weight /= 2


def iterative_gbfs( # uses h(n)
        initial_state: 'SokobanState',
        heur_fn: Callable,
        timebound: int = 5) -> tuple[Union['SokobanState', bool], 'SearchStatistics']:
    """
    Returns a tuple of the goal SokobanState and a SearchStatistics object
    by implementing iterative greedy best-first search as defined in the handout.

    :param initial_state: The initial SokobanState of the game of Sokoban.
    :param heur_fn: The heuristic function used in iterative greedy best-first search.
    :param timebound: The time bound used in iterative greedy best-first search, in seconds.
    :return: A tuple consisting of the goal SokobanState or False if such a state
             is not found, and a SearchStatistics object.
    """
    start = os.times()[0]
    max_g = float('inf')
    best_soln = None
    first_call = True


    while True:
        #Create search engine
        wrap_fn = lambda sN: sN.hval
        search_eng = SearchEngine(strategy='custom')
        search_eng.init_search(initial_state, sokoban_goal_state, heur_alternate, wrap_fn)

        #Update Time
        time_left = timebound - (os.times()[0] - start)

        #Check to see if Under time
        if not first_call:
            if time_left <= 0:
                if best_soln is not None:
                    return best_soln
                else:
                    return result

        #Search
        result = search_eng.search(time_left, (max_g, float('inf'), float('inf')))
        if first_call and result[0] == False:
            return result
        first_call = False

        if result[0] == False:
            if best_soln is not None:
                return best_soln
            else:
                return result

        #Update cost
        g_v = result[0].gval
        if g_v < max_g:
            max_g = g_v
            best_soln = result