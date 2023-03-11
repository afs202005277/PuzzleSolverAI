from collections import deque


class TreeNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
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

    while queue:
        node = queue.popleft()  # get first element in the queue
        if goal_state_func(node.state):  # check goal state
            return node

        for state in operators_func(node.state):  # go through next states
            child = TreeNode(state, node)

            node.add_child(child)

            queue.append(child)

    return None


def print_solution(node):
    if node is not None:
        print_solution(node.parent)
        print(node.state)


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
    return heuristic(node) + node.cost


def a_star_search(initial_state, goal_state_func, operators_func, heuristic):
    root = TreeNode(initial_state)  # create the root node in the search tree
    queue = [root]  # initialize the queue to store the nodes
    visited = []
    while queue:
        node = queue.pop()  # get first element in the queue
        if goal_state_func(node.state):  # check goal state
            return node

        for state in operators_func(node.state):  # go through next states
            if state not in visited:
                child = TreeNode(state, node)
                child.cost += node.cost

                node.add_child(child)

                queue.append(child)

                sorted(queue, key=lambda x: h_a_star(x, heuristic), reverse=True)
                visited.append(state)

    return None
