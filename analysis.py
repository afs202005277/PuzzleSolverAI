import show_data_web
from models import *
from search_algorithms import *
from heuristics import *
import time

"""
This code block contains the code which compares the performance of different search strategies and heuristics on different levels of a game. Here's what it does:

Defines three dictionaries: 
- uninformed_search contains the different uninformed search algorithms to be tested
- informed_search contains the different informed search algorithms to be tested
- heuristics contains the different heuristics to be used

Defines a dictionary levels containing different levels of the game.
Defines two dictionaries: 
- optimal_solutions will store the optimal solutions for each level
- statistics will store the statistics of the search algorithms for each level
Loops over each level and each uninformed search strategy: for each combination, it measures the time it takes to find a solution, the number of nodes expanded, the number of iterations performed, and the relative error (difference between the found solution and the optimal solution, divided by the optimal solution).
Loops over each level and each informed search strategy and heuristic: for each combination, it measures the time it takes to find a solution, the number of nodes expanded, the number of iterations performed, and the relative error.
Displays the statistics in a web page using the show_data module.
Overall, the program compares the performance of different search algorithms and heuristics on different levels of a game. 
It measures the time it takes to find a solution, the number of nodes expanded, the number of iterations performed, and the relative error. 
Finally, it displays the results in a web application.
"""
if __name__ == '__main__':
    uninformed_search = {"BFS": breadth_first_search, "DFS": depth_first_search, "IDS": iterative_deepening_search}
    informed_search = {"Greedy": greedy_search, "A* search": a_star_search,
                       "Weighted A* search": weighted_a_star_search}
    heuristics = {"h1": h1, "h2": h2, "h3": h3, "h4": h4, "h5": h5, "h6": h6, "h7": h7, "h8": h8}
    levels = {'easy': easy_map(), 'medium': medium_map()}
    optimal_solutions = dict()
    statistics = dict()

    for level in levels:
        statistics[level] = {'time': {}, 'nodes': {}, 'iterations': {}, 'relative error': {}}

    for strategy in uninformed_search:
        for level in levels:
            start = time.time()
            details = uninformed_search[strategy](levels[level], gameOver, get_child_states)
            end = time.time()

            path = get_solution_path(details[0])

            if strategy == "BFS":
                optimal_solutions[level] = len(path)
            statistics[level]['time'][strategy] = end - start
            statistics[level]['nodes'][strategy] = details[1]
            statistics[level]['iterations'][strategy] = details[2]
            statistics[level]['relative error'][strategy] = (abs(len(path) - optimal_solutions[level]) /
                                                             optimal_solutions[
                                                                 level]) * 100

    statistics_informed = dict()
    for level in levels:
        statistics_informed[level] = {'time': {algo_name: {} for algo_name in informed_search.keys()},
                                      'nodes': {algo_name: {} for algo_name in informed_search.keys()},
                                      'iterations': {algo_name: {} for algo_name in informed_search.keys()},
                                      'relative error': {algo_name: {} for algo_name in informed_search.keys()}}
    for strategy in informed_search:
        for level in levels:
            for heuristic in heuristics:
                start = time.time()
                # [node, len(visited) + puzzles_in_memory, iterations]
                details = informed_search[strategy](levels[level], gameOver, get_child_states, heuristics[heuristic])
                end = time.time()

                path = get_solution_path(details[0])
                if not statistics_informed[level]['time'][strategy]:
                    statistics_informed[level]['time'][strategy] = {}
                    statistics_informed[level]['nodes'][strategy] = {}
                    statistics_informed[level]['iterations'][strategy] = {}
                    statistics_informed[level]['relative error'][strategy] = {}

                statistics_informed[level]['time'][strategy][heuristic] = end - start
                statistics_informed[level]['nodes'][strategy][heuristic] = details[1]
                statistics_informed[level]['iterations'][strategy][heuristic] = details[2]
                statistics_informed[level]['relative error'][strategy][heuristic] = ((len(path) - optimal_solutions[
                    level]) /
                                                                                     optimal_solutions[level]) * 100
    app = show_data_web.show_data(statistics, statistics_informed)
    app.run()
