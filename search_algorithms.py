import heapq
from collections import deque
import main


class TreeNode:
    def __init__(self, state, parent=None, cost=0):
        self.state = state
        self.parent = parent
        self.children = []
        self.cost = cost
        self.moved_piece = None
        if self.parent is None:
            self.depth = 0
        else:
            self.depth = self.parent.depth + 1

    def add_child(self, child_node):
        self.children.append(child_node)
        child_node.parent = self


def breadth_first_search(initial_state, goal_state_func, operators_func):
    root = TreeNode(initial_state)
    queue = deque([root])
    visited = set()

    puzzles_in_memory = 0
    iterations = 0
    while queue:
        iterations += 1
        node = queue.popleft()
        visited.add(node.state)

        if goal_state_func(node.state):
            return [node, len(visited) + puzzles_in_memory, iterations]

        for state in operators_func(node.state):
            if state not in visited:
                child = TreeNode(state, node)
                node.add_child(child)
                queue.append(child)
                puzzles_in_memory += 1

    return None


def print_solution(node):
    if node is not None:
        print_solution(node.parent)
        print(node.state.show_tui())


def get_solution_path(node):
    res = []
    if node is not None:
        res += get_solution_path(node.parent)
        res.append(node.state)
    return res


def depth_first_search(initial_state, goal_state_func, operators_func):
    root = TreeNode(initial_state)  # create the root node in the search tree
    queue = [root]  # initialize the queue to store the nodes
    visited = set()

    puzzles_in_memory = 0
    iterations = 0
    while queue:
        iterations += 1
        node = queue.pop()  # get first element in the queue
        if goal_state_func(node.state):  # check goal state
            return [node, len(visited) + puzzles_in_memory, iterations]

        for state in operators_func(node.state):  # go through next states
            if state not in visited:
                child = TreeNode(state, node)

                node.add_child(child)

                queue.append(child)
                puzzles_in_memory += 1
                visited.add(state)

    return None


def depth_limited_search(initial_state, goal_state_func, operators_func, depth_limit):
    root = TreeNode(initial_state)  # create the root node in the search tree
    queue = [root]  # initialize the queue to store the nodes
    visited = set()
    iterations = 0
    puzzles_in_memory = 0
    while queue:
        iterations += 1
        node = queue.pop()  # get first element in the queue
        if goal_state_func(node.state):  # check goal state
            return [node, len(visited) + puzzles_in_memory, iterations]

        if node.depth < depth_limit:
            for state in operators_func(node.state):  # go through next states
                if state not in visited:
                    child = TreeNode(state, node)

                    node.add_child(child)
                    puzzles_in_memory += 1
                    queue.append(child)
                    visited.add(state)

    return None


def iterative_deepening_search(initial_state, goal_state_func, operators_func):
    depth_limit = 0
    while True:
        depth_limit += 1
        answer = depth_limited_search(initial_state,
                                      goal_state_func,
                                      operators_func,
                                      depth_limit)
        if answer:
            return answer


def h_a_star(node, heuristic, moved):
    return heuristic(node.state, moved) + node.cost


def greedy_search(initial_state, goal_state_func, operators_func, heuristic):
    setattr(TreeNode, "__lt__",
            lambda self, other: h_a_star(self, heuristic, self.moved_piece) < h_a_star(other, heuristic,
                                                                                       other.moved_piece))
    root = TreeNode(initial_state)  # create the root node in the search tree
    queue = [root]
    heapq.heapify(queue)  # initialize the queue to store the nodes
    visited = set()
    iterations = 0
    puzzles_in_memory = 0
    while queue:
        iterations += 1
        node = heapq.heappop(queue)
        if goal_state_func(node.state):  # check goal state
            return [node, len(visited) + puzzles_in_memory, iterations]

        for state in operators_func(node.state):  # go through next states
            if state not in visited:
                for i, piece in enumerate(node.state.pieces):
                    if piece != state.pieces[i]:
                        state.moved_piece = i
                        break
                child = TreeNode(state, node)

                node.add_child(child)

                heapq.heappush(queue, child)

                puzzles_in_memory += 1
                visited.add(state)
    return None


def a_star_search(initial_state, goal_state_func, operators_func, heuristic):
    setattr(TreeNode, "__lt__",
            lambda self, other: h_a_star(self, heuristic, self.moved_piece) < h_a_star(other, heuristic,
                                                                                       other.moved_piece))
    root = TreeNode(initial_state)  # create the root node in the search tree
    queue = [root]
    heapq.heapify(queue)  # initialize the queue to store the nodes
    visited = set()
    iterations = 0
    puzzles_in_memory = 0
    while queue:
        iterations += 1
        node = heapq.heappop(queue)
        if goal_state_func(node.state):  # check goal state
            return [node, len(visited) + puzzles_in_memory, iterations]

        for state in operators_func(node.state):  # go through next states
            if state not in visited:
                for i, piece in enumerate(node.state.pieces):
                    if piece != state.pieces[i]:
                        state.moved_piece = i
                        break
                child = TreeNode(state, node, node.cost + 1)

                node.add_child(child)

                heapq.heappush(queue, child)

                puzzles_in_memory += 1
                visited.add(state)
    return None


def weighted_a_star_search(initial_state, goal_state_func, operators_func, heuristic):
    w = main.h1
    return a_star_search(initial_state, goal_state_func, operators_func,
                         lambda x, y: (heuristic(x, y) + w(x, None)) / 2)
