import heapq
from collections import deque
import heuristics


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


"""
This function performs a breadth-first search algorithm to find a solution path from an initial state to a goal state, given a set of operators that can be applied to the states.

Arguments:

initial_state: The initial state.
goal_state_func: Function returning True if a state is the goal state.
operators_func: Function returning a list of possible successor states.
Returns a list with three elements:

The TreeNode object that represents the solution path.
The total number of visited states and puzzles stored in memory.
The total number of iterations performed by the algorithm.
If no solution is found, the function returns None.
"""


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


"""
This function performs a depth-first search algorithm to find a solution path from an initial state to a goal state, given a set of operators that can be applied to the states.

Arguments:
initial_state: The initial state.
goal_state_func: Function returning True if a state is the goal state.
operators_func: Function returning a list of possible successor states.

Returns a list with three elements:
The TreeNode object that represents the solution path.
The total number of visited states and puzzles stored in memory.
The total number of iterations performed by the algorithm.
If no solution is found, the function returns None.

The function initializes a root node in the search tree with the initial state, and a queue to store the nodes. 
It also initializes a set to store the visited states. The function then iteratively pops a node from the queue, 
checks if it is the goal state, and explores its child nodes by applying the operators. 
The search algorithm proceeds by adding the new child nodes to the queue and marking them as visited. 
The function differs from breadth-first search in that it uses a stack instead of a queue, which means that it explores nodes depth-first instead of breadth-first.
"""


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


"""
This function performs a depth-limited search algorithm to find a solution path from an initial state to a goal state, given a set of operators that can be applied to the states, and a maximum depth limit.

Arguments:

initial_state: The initial state.
goal_state_func: Function returning True if a state is the goal state.
operators_func: Function returning a list of possible successor states.
depth_limit: Maximum depth limit for the search.

Returns a list with three elements:
The TreeNode object that represents the solution path.
The total number of visited states and puzzles stored in memory.
The total number of iterations performed by the algorithm.
If no solution is found within the depth limit, the function returns None.

The function initializes a root node in the search tree with the initial state, and a queue to store the nodes. 
It also initializes a set to store the visited states. The function then iteratively pops a node from the queue, checks if it is the goal state, and explores its child nodes by applying the operators, but only if the node depth is less than the depth limit. 
The search algorithm proceeds by adding the new child nodes to the queue and marking them as visited. The function differs from depth-first search in that it limits the depth of exploration to avoid infinite loops or excessively long search times.
"""


def depth_limited_search(initial_state, goal_state_func, operators_func, depth_limit):
    root = TreeNode(initial_state)  # create the root node in the search tree
    root.depth = 0
    queue = deque([root])  # initialize the queue to store the nodes
    visited = set()
    iterations = 0
    puzzles_in_memory = 0
    while queue:
        iterations += 1
        node = queue.popleft()  # get first element in the queue
        if goal_state_func(node.state):  # check goal state
            return [node, len(visited) + puzzles_in_memory, iterations]

        if node.depth <= depth_limit:
            for state in operators_func(node.state):  # go through next states
                if state not in visited:
                    child = TreeNode(state, node)
                    child.depth = node.depth + 1
                    node.add_child(child)
                    puzzles_in_memory += 1
                    queue.append(child)
                    visited.add(state)

    return None


"""
This function performs an iterative deepening search algorithm to find a solution path from an initial state to a goal state, given a set of operators that can be applied to the states.

Arguments:
initial_state: The initial state.
goal_state_func: Function returning True if a state is the goal state.
operators_func: Function returning a list of possible successor states.

Returns a list with three elements:
The TreeNode object that represents the solution path.
The total number of visited states and puzzles stored in memory.
The total number of iterations performed by the algorithm.
The function first sets the depth limit to zero and repeatedly calls the depth-limited search function with an increasing depth limit until a solution is found. If a solution is found, the function returns the result from the depth-limited search.
The depth-limited search is performed with the initial state, the goal state function, the operator function, and the current depth limit.

The iterative deepening search algorithm is a combination of the depth-first search and the breadth-first search algorithms. 
It performs a depth-first search up to a certain depth limit, and then starts over with an increased depth limit until the goal state is found. 
This approach combines the space efficiency of depth-first search with the completeness of breadth-first search. It also guarantees that the optimal solution will be found, as the depth limit is gradually increased."""


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


"""
This function implements the h-value calculation for the A* algorithm with a heuristic function.

Arguments:
node: A TreeNode object representing a state in the search tree.
heuristic: A heuristic function that takes a state and the move taken to reach that state, and returns an estimated cost from that state to the goal state.
moved: The index of the moved piece

Returns the sum of the heuristic value for the current state and the cost of moving from the parent state to the current state.
This function is called by the A* search algorithm to calculate the h-value for each node in the search tree.
The heuristic function is used to estimate the cost of reaching the goal state from the current state, and the moved parameter is used to represent the cost of moving from the parent state to the current state.
The h-value calculated by this function is used to calculate the f-value for the node, which is used to prioritize nodes for expansion in the A* search algorithm.
"""


def h_a_star(node, heuristic, moved):
    return heuristic(node.state, moved) + node.cost


"""
This function, named greedy_search, performs a greedy search algorithm to find a solution path from an initial state to 
a goal state, given a set of operators that can be applied to the states and a heuristic function that estimates the 
distance from the current state to the goal state.

Arguments:
initial_state: The initial state from which the search starts.
goal_state_func: A function that takes a state as input and returns True if it is the goal state, False otherwise.
operators_func: A function that takes a state as input and returns a list of possible successor states.
heuristic: A function that takes one state as input and returns an estimation of the distance from the current state to the goal state.

The function returns a list with three elements:
The first element is the TreeNode object that represents the solution path.
The second element is the total number of visited states and puzzles stored in memory during the search.
The third element is the total number of iterations performed by the algorithm.

If no solution is found, the function returns None.

The function works by maintaining a priority queue of nodes to be explored, where the priority of a node is determined by the value of the heuristic function for that node. 
At each iteration, the node with the lowest heuristic value is selected from the priority queue, and its children are generated and added to the queue. 
The function terminates when the goal state is found or the queue becomes empty, indicating that there is no solution path from the initial state to the goal state. 
The function also keeps track of the number of iterations and the number of visited states and puzzles stored in memory during the search.
"""


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


"""
This function, named a_star_search, performs the A* search algorithm to find a solution path from an initial state to a 
goal state, given a set of operators that can be applied to the states and a heuristic function 
that estimates the distance to the goal state.

Arguments:
initial_state: The initial state from which the search starts.
goal_state_func: A function that takes a state as input and returns True if it is the goal state, False otherwise.
operators_func: A function that takes a state as input and returns a list of possible successor states.
heuristic: A function that takes a state as input and returns an estimate of the distance to the goal state.

The function returns a list with three elements:
The first element is the TreeNode object that represents the solution path.
The second element is the total number of visited states and puzzles stored in memory during the search.
The third element is the total number of iterations performed by the algorithm.

If no solution is found, the function returns None.

"""


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


"""
This function, named weighted_a_star_search, performs a weighted A* search algorithm to find a solution path from an 
initial state to a goal state, given a set of operators that can be applied to the states.

Arguments:
initial_state: The initial state from which the search starts.
goal_state_func: A function that takes a state as input and returns True if it is the goal state, False otherwise.
operators_func: A function that takes a state as input and returns a list of possible successor states.
heuristic: A function that takes a state as input and returns an estimate of the distance from that state to the goal state.

The function first sets the weight w to be a specific heuristic function, and then calls the a_star_search function,
passing the appropriate arguments including a lambda function that averages the heuristic with the weight. 

The function returns the list returned by the a_star_search function.
"""


def weighted_a_star_search(initial_state, goal_state_func, operators_func, heuristic):
    w = heuristics.h1
    return a_star_search(initial_state, goal_state_func, operators_func,
                         lambda x, y: (heuristic(x, y) + w(x, None)) / 2)
