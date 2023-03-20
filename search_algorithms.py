import heapq
from collections import deque


class TreeNode:
    def __init__(self, state, parent=None, cost=0):
        self.state = state
        self.parent = parent
        self.children = []
        self.cost = cost
        if self.parent is None:
            self.depth = 0
        else:
            self.depth = self.parent.depth + 1

    def add_child(self, child_node):
        self.children.append(child_node)
        child_node.parent = self


def breadth_first_search(initial_state, goal_state_func, operators_func):
    root = TreeNode(initial_state)  # create the root node in the search tree
    queue = deque([root])  # initialize the queue to store the nodes
    visited = set()

    while queue:
        node = queue.popleft()  # get first element in the queue
        visited.add(node.state)
        # print(node.state.show_tui())

        if goal_state_func(node.state):  # check goal state
            return node

        for state in operators_func(node.state):  # go through next states
            if state not in visited:
                child = TreeNode(state, node)
                node.add_child(child)
                queue.append(child)

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
    visited = list()

    while queue:
        node = queue.pop()  # get first element in the queue
        if goal_state_func(node.state):  # check goal state
            return node

        for state in operators_func(node.state):  # go through next states
            if state not in visited:
                child = TreeNode(state, node)

                node.add_child(child)

                queue.append(child)
                visited.append(state)

    return None


def depth_limited_search(initial_state, goal_state_func, operators_func, depth_limit):
    root = TreeNode(initial_state)  # create the root node in the search tree
    queue = [root]  # initialize the queue to store the nodes
    visited = list()
    depth = 0
    while queue:
        node = queue.pop()  # get first element in the queue
        if goal_state_func(node.state):  # check goal state
            return node

        if depth < depth_limit:
            for state in operators_func(node.state):  # go through next states
                if state not in visited:
                    child = TreeNode(state, node)

                    node.add_child(child)

                    queue.append(child)
                    visited.append(state)
        depth += 1

    return None


def iterative_deepening_search(initial_state, goal_state_func, operators_func, depth_limit):
    for i in range(depth_limit):
        answer = depth_limited_search(initial_state,
                                      goal_state_func,
                                      operators_func,
                                      i)
        if answer:
            print(i)
            return answer


def h_a_star(node, heuristic):
    return heuristic(node.state) + node.cost


def a_star_search(initial_state, goal_state_func, operators_func, heuristic):
    setattr(TreeNode, "__lt__", lambda self, other: heuristic(self.state) < heuristic(other.state))
    root = TreeNode(initial_state)  # create the root node in the search tree
    queue = [root]  # initialize the queue to store the nodes
    visited = set()
    iterations = 0
    while queue:
        iterations += 1
        node = heapq.heappop(queue)
        if goal_state_func(node.state):  # check goal state
            print(iterations)
            return node

        for state in operators_func(node.state):  # go through next states
            if state not in visited:
                child = TreeNode(state, node, node.cost + 1)

                node.add_child(child)

                heapq.heappush(queue, child)

                queue = sorted(queue, key=lambda x: h_a_star(x, heuristic))
                visited.add(state)
    return None
