import time
from collections import deque

# Define goal state
GOAL_STATE = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 0]

# Define initial state
INITIAL_STATE = [1, 0, 2, 4, 5, 7, 3, 8, 9, 6, 11, 12, 13, 10, 14, 15]

# Define actions
ACTIONS = {'U': -4, 'D': 4, 'L': -1, 'R': 1}


def get_manhattan_distance(state):
    """
    Calculate the sum of Manhattan distances of all tiles from their goal positions.
    """
    distance = 0
    for i, value in enumerate(state):
        if value != 0:
            goal_x, goal_y = divmod(GOAL_STATE.index(value), 4)
            current_x, current_y = divmod(i, 4)
            distance += abs(goal_x - current_x) + abs(goal_y - current_y)
    return distance


def get_misplaced_tiles(state):
    """
    Calculate number of misplaced tiles.
    """
    count = 0
    for i, value in enumerate(state):
        if value != 0 and value != GOAL_STATE[i]:
            count += 1
    return count


def get_successors(state):
    """
    Generate all possible successor states.
    """
    successors = []
    blank_index = state.index(0)
    for action, offset in ACTIONS.items():
        new_index = blank_index + offset
        if 0 <= new_index < 16 and (new_index // 4 == blank_index // 4 or new_index % 4 == blank_index % 4):
            new_state = state[:]
            new_state[blank_index], new_state[new_index] = new_state[new_index], new_state[blank_index]
            successors.append((new_state, action))
    return successors


def breadth_first_search():
    """
    Perform BFS to solve the 15-puzzle problem.
    """
    start_time = time.time()

    queue = deque([(INITIAL_STATE, [])])
    visited = set()
    while queue:
        state, moves = queue.popleft()
        if tuple(state) in visited:
            continue
        visited.add(tuple(state))

        if state == GOAL_STATE:
            end_time = time.time()
            print("BFS")
            print("Moves:", "".join(moves))
            print(f"Time taken: {(end_time - start_time) * 1000:.2f} ms")
            print("Solution exists")
            return

        for successor, action in get_successors(state):
            queue.append((successor, moves + [action]))

    print("BFS")
    print("No solution found")


def depth_first_search():
    """
    Perform DFS to solve the 15-puzzle problem.
    """
    start_time = time.time()

    stack = [(INITIAL_STATE, [])]
    visited = set()
    while stack:
        state, moves = stack.pop()
        if tuple(state) in visited:
            continue
        visited.add(tuple(state))

        if state == GOAL_STATE:
            end_time = time.time()
            print("DFS")
            print("Moves:", "".join(moves))
            print(f"Time taken: {(end_time - start_time) * 1000:.2f} ms")
            print("Solution exists")
            return

        for successor, action in get_successors(state):
            stack.append((successor, moves + [action]))

    print("DFS")
    print("No solution found")


def informed_search(heuristic):
    """
    Perform Informed Search with a given heuristic to solve the 15-puzzle problem.
    """
    start_time = time.time()

    queue = [(heuristic(INITIAL_STATE), 0, INITIAL_STATE, [])]
    visited = set()
    while queue:
        _, cost, state, moves = queue.pop(0)
        if tuple(state) in visited:
            continue
        visited.add(tuple(state))

        if state == GOAL_STATE:
            end_time = time.time()
            print(f"Informed Search ({heuristic.__name__})")
            print("Moves:", "".join(moves))
            print(f"Time taken: {(end_time - start_time) * 1000:.2f} ms")
            print("Solution exists")
            return

        for successor, action in get_successors(state):
            queue.append((heuristic(successor) + cost + 1, cost + 1, successor, moves + [action]))
        queue.sort()

    print(f"Informed Search ({heuristic.__name__})")
    print("No solution found")


# Run search algorithms
breadth_first_search()
print()
depth_first_search()
print()
informed_search(get_misplaced_tiles)
print()
informed_search(get_manhattan_distance)
