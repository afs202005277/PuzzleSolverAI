# Block Escape

## Overview
Block Escape is an AI-based puzzle-solving project where the objective is to navigate a red block to the exit on a limited grid, while maneuvering around various obstacles. This project aims to implement and analyze various search algorithms to determine the most efficient approach for solving the puzzle.

## Project Objectives
1. Implement search algorithms to efficiently find a path to the exit.
2. Test and compare various algorithms and heuristics to identify the optimal approach for solving the puzzle.
3. Analyze performance metrics for different algorithms.

## Formulation of the Problem
- **Objective Test:** The red block reaches the exit position.
- **State Representation:** A Puzzle object with defined dimensions and a list of blocks.
- **Initial State:** A grid with the red block blocked by obstacles.
- **Operators:**
  - `move`: Move a block to an adjacent empty space if it is within the valid coordinates of the board.
  - **Preconditions:** Space adjacent to the current position must be valid and empty.
  - **Cost:** 1 move.
  - **Effect:** Updates the position of the block.

## Heuristics
1. Distance from the red block to the exit.
2. Weighted sum of obstacles between the red block and the exit.
3. Maximizing contiguous empty space near the red block.
4. Keeping the red block close to the edges of the board.
5. Ensuring the red block always has a valid move.
6. Prioritizing fitting blocks along the board edges from largest to smallest.
7. Moving the largest blocks first.
8. Moving the smallest blocks first.

## Implemented Algorithms
- Breadth-First Search (BFS)
- Depth-First Search (DFS)
- Depth-Limited Search
- Iterative Deepening Search (IDS)
- Greedy Search
- A* Search
- Weighted A* Search

## Experimental Results
The experimental results, as detailed in the report, highlight the following:
- BFS is the slowest algorithm.
- Greedy search performs inconsistently due to the lack of a cost function.
- Heuristic prioritizing proximity to board edges yielded the best results.
- All heuristics produced optimal solutions with the A* algorithm.
- IDS proved slower than DFS but was more memory-efficient.

## Conclusions
The performance of search-based games like Block Escape is significantly influenced by the choice of algorithm and heuristic. While BFS is not well-suited for this game, Greedy Search offered interesting but suboptimal performance. Ultimately, A* with suitable heuristics proved to be the most effective approach.
