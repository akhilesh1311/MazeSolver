import random
import math
import sys
import copy
import heapq
import maze


class DFSSolver(maze.Maze):
    """Class to solve a maze using DFS"""
    path = []
    def __init__(self, MazeObject):
        super().__init__(0, 0, MazeObject.maze)
        self.visited = set()
        self.parent = dict()
        self.is_solvable = False

    def find_path(self, cur_i, cur_j):
        """Performs a DFS search to find a path from (cur_i, cur_j) position to G in a maze"""
        dfs_stack = []
        self.visited.add((cur_i, cur_j))
        dfs_stack.append((cur_i, cur_j))
        self.max_fringe_size, self.nodes_expanded = 0, 0
        while dfs_stack:
            self.max_fringe_size = max(self.max_fringe_size, len(dfs_stack))
            self.nodes_expanded += 1
            cur_i, cur_j = dfs_stack.pop()
            for i in range(cur_i - 1, cur_i + 2):
                for j in range(cur_j - 1, cur_j + 2):
                    if 0 <= i < self.dim and 0 <= j < self.dim and abs(
                            i - cur_i) + abs(j - cur_j) == 1 and self.maze[i][j] != 'X' and (i, j) not in self.visited:
                        self.parent[(i, j)] = (cur_i, cur_j)
                        dfs_stack.append((i, j))
                        self.visited.add((i, j))
                        if self.maze[i][j] == 'G':
                            self.is_solvable = True
                            return

    def trace_path(self, goal_i, goal_j):
        """Traces the path from (goal_i, goal_j) position to S"""
        i, j = goal_i, goal_j
        self.maze_copy = copy.deepcopy(self.maze)
        while (i, j) != (0, 0):
            self.path.append((i, j))
            i, j = self.parent[(i, j)]
        self.path.pop(0)
        for i, j in self.path:
            self.maze_copy[i][j] = '#'
        self.solution_length = len(self.path) + 1

    def display_solution(self):
        """Displays the path from S to G"""
        self.find_path(0, 0)
        if self.is_solvable:
            print("Displaying solution with DFS -")
            self.trace_path(self.dim - 1, self.dim - 1)
            for i in range(self.dim):
                print(*self.maze_copy[i], sep=' ')
        else:
            print("Maze is not solvable.")
        print()


class BFSSolver(maze.Maze):
    """Class to solve a maze using BFS"""
    path = []

    def __init__(self, MazeObject):
        super().__init__(0, 0, MazeObject.maze)
        self.visited = set()
        self.parent = dict()
        self.is_solvable = False

    def find_path(self, cur_i, cur_j):
        """Performs a BFS search to find a path from (cur_i, cur_j) position to G in a maze"""
        queue = []
        queue.append((cur_i, cur_j))
        self.visited.add((cur_i, cur_j))
        self.max_fringe_size, self.nodes_expanded = 0, 0
        while queue:
            self.max_fringe_size = max(self.max_fringe_size, len(queue))
            self.nodes_expanded += 1
            cur_i, cur_j = queue.pop(0)
            for i in range(cur_i - 1, cur_i + 2):
                for j in range(cur_j - 1, cur_j + 2):
                    if 0 <= i < self.dim and 0 <= j < self.dim and abs(
                            i - cur_i) + abs(j - cur_j) == 1 and self.maze[i][j] != 'X' and (i, j) not in self.visited:
                        self.parent[(i, j)] = (cur_i, cur_j)
                        self.visited.add((i, j))
                        queue.append((i, j))
                        if self.maze[i][j] == 'G':
                            self.is_solvable = True
                            return

    def trace_path(self, goal_i, goal_j):
        """Traces the path from (goal_i, goal_j) position to S"""
        i, j = goal_i, goal_j
        self.maze_copy = copy.deepcopy(self.maze)
        while (i, j) != (0, 0):
            i, j = self.parent[(i, j)]
            self.path.append((i, j))
        self.path.pop()
        self.solution_length = len(self.path) + 1
        for i, j in self.path:
            self.maze_copy[i][j] = '#'

    def display_solution(self):
        """Displays the path from S to G"""
        self.find_path(0, 0)
        if self.is_solvable:
            print("Displaying solution with BFS -")
            self.trace_path(self.dim - 1, self.dim - 1)
            for i in range(self.dim):
                print(*self.maze_copy[i], sep=' ')
        else:
            print("Maze is not solvable.")
        print()