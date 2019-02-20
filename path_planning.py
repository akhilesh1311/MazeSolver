import random
import sys


class Maze(object):
    def __init__(self, dim=0, p=0, maze_arr=[]):
        self.arr = []
        if dim != 0:
            self.dim = dim
            self.p = p
            for i in range(dim):
                tmp = []
                for j in range(dim):
                    cell = 'X' if random.random() < p else 'O'
                    tmp.append(cell)
                self.arr.append(tmp)
            self.arr[0][0] = 'S'
            self.arr[dim - 1][dim - 1] = 'G'
        else:
            for i in range(len(maze_arr)):
                tmp = []
                for j in range(len(maze_arr[i])):
                    if maze_arr[i][j] == '#':
                        tmp.append('O')
                    else:
                        tmp.append(maze_arr[i][j])
                self.arr.append(tmp)
            self.dim = len(maze_arr)

    def display(self):
        for i in range(self.dim):
            print(*self.arr[i], sep=' ')


class DFSSolver(Maze):
    path = []
    dfs_stack = []
    def __init__(self, MazeObject):
        super().__init__(0, 0, MazeObject.arr)
        self.visited = set()
        self.parent = dict()
        self.is_solvable = False

    def find_path(self, cur_i, cur_j):
        self.visited.add((cur_i, cur_j))
        self.dfs_stack.append((cur_i, cur_j))
        while self.dfs_stack:
            cur_i, cur_j = self.dfs_stack.pop()
            for i in range(cur_i - 1, cur_i + 2):
                for j in range(cur_j - 1, cur_j + 2):
                    if 0 <= i < self.dim and 0 <= j < self.dim and abs(
                            i - cur_i) + abs(j - cur_j) == 1 and self.arr[i][j] != 'X' and (i, j) not in self.visited:
                        self.parent[(i, j)] = (cur_i, cur_j)
                        self.dfs_stack.append((i, j))
                        self.visited.add((i, j))
                        if self.arr[i][j] == 'G':
                            self.is_solvable = True
                            return

    def trace_path(self, goal_i, goal_j):
        i, j = goal_i, goal_j
        while (i, j) != (0, 0):
            self.path.append((i, j))
            i, j = self.parent[(i, j)]
        self.path.pop(0)
        for i, j in self.path:
            self.arr[i][j] = '#'

    def display_solution(self):
        # self.display()
        self.find_path(0, 0)
        if self.is_solvable:
            print("Displaying solution with DFS -")
            self.trace_path(self.dim - 1, self.dim - 1)
            for i in range(self.dim):
                print(*self.arr[i], sep=' ')
        else:
            print("Maze is not solvable.")


class BFSSolver(Maze):
    path = []

    def __init__(self, MazeObject):
        super().__init__(0, 0, MazeObject.arr)
        self.visited = set()
        self.parent = dict()
        self.queue = []
        self.is_solvable = False

    def find_path(self, cur_i, cur_j):
        self.queue.append((cur_i, cur_j))
        self.visited.add((cur_i, cur_j))
        while self.queue:
            cur_i, cur_j = self.queue.pop(0)
            for i in range(cur_i - 1, cur_i + 2):
                for j in range(cur_j - 1, cur_j + 2):
                    if 0 <= i < self.dim and 0 <= j < self.dim and abs(
                            i - cur_i) + abs(j - cur_j) == 1 and self.arr[i][j] != 'X' and (i, j) not in self.visited:
                        self.parent[(i, j)] = (cur_i, cur_j)
                        self.visited.add((i, j))
                        self.queue.append((i, j))
                        if self.arr[i][j] == 'G':
                            self.is_solvable = True
                            return

    def trace_path(self, goal_i, goal_j):
        i, j = goal_i, goal_j
        while (i, j) != (0, 0):
            i, j = self.parent[(i, j)]
            self.path.append((i, j))
        self.path.pop()
        for i, j in self.path:
            self.arr[i][j] = '#'

    def display_solution(self):
        self.find_path(0, 0)
        if self.is_solvable:
            print("Displaying solution with BFS -")
            self.trace_path(self.dim - 1, self.dim - 1)
            for i in range(self.dim):
                print(*self.arr[i], sep=' ')
        else:
            print("Maze is not solvable.")


if __name__ == '__main__':
    M = Maze(4000, 0.1)
    # print("Displaying the maze: ")
    # M.display()
    # D = DFSSolver(M)
    B = BFSSolver(M)
    # D.display_solution()
    # B.display_solution()
    print("Successful")
