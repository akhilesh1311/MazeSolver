import random
import copy
import sys


# class Maze(object):
#     def __init__(self, dim=0, p=0, maze_arr=[]):
#         self.arr = []
#         if dim != 0:
#             self.dim = dim
#             self.p = p
#             for i in range(dim):
#                 tmp = []
#                 for j in range(dim):
#                     cell = 'X' if random.random() < p else 'O'
#                     tmp.append(cell)
#                 self.arr.append(tmp)
#             self.arr[0][0] = 'S'
#             self.arr[dim - 1][dim - 1] = 'G'
#         else:
#         	self.arr = copy.deepcopy(maze_arr)
#         	self.dim = len(maze_arr)
#             # for i in range(len(maze_arr)):
#             #     tmp = []
#             #     for j in range(len(maze_arr[i])):
#             #         if maze_arr[i][j] == '#':
#             #             tmp.append('O')
#             #         else:
#             #             tmp.append(maze_arr[i][j])
#             #     self.arr.append(tmp)

#     def display(self):
#         for i in range(self.dim):
#             print(*self.arr[i], sep=' ')


# class DFSSolver(Maze):
#     path = []
#     dfs_stack = []
#     max_fringe = 0
#     path_length = 0

#     def __init__(self, maze_arr):
#         super().__init__(0, 0, maze_arr)
#         self.visited = set()
#         self.parent = dict()
#         self.is_solvable = False

#     def find_path(self, cur_i, cur_j):
#         self.visited.add((cur_i, cur_j))
#         self.dfs_stack.append((cur_i, cur_j))
#         while self.dfs_stack:
#             cur_i, cur_j = self.dfs_stack.pop()
#             if self.arr[cur_i][cur_j] == 'G':
#             	self.is_solvable = True
#             	return
#             self.max_fringe = max(self.max_fringe, len(self.dfs_stack))
#             for i in range(cur_i - 1, cur_i + 2):
#                 for j in range(cur_j - 1, cur_j + 2):
#                     if 0 <= i < self.dim and 0 <= j < self.dim and abs(
#                             i - cur_i) + abs(j - cur_j) == 1 and self.arr[i][j] != 'X' and (i, j) not in self.visited:
#                         self.parent[(i, j)] = (cur_i, cur_j)
#                         self.dfs_stack.append((i, j))
#                         self.visited.add((i, j))
#                         # if self.arr[i][j] == 'G':
#                         #     self.is_solvable = True
#                         #     return

#     def trace_path(self, goal_i, goal_j):
#         i, j = goal_i, goal_j
#         while (i, j) != (0, 0):
#             self.path.append((i, j))
#             i, j = self.parent[(i, j)]
#         self.path.pop(0)
#         for i, j in self.path:
#             self.arr[i][j] = '#'
#         self.path_length = len(self.path)

#     def display_solution(self):
#         # self.display()
#         self.find_path(0, 0)
#         if self.is_solvable:
#             print("Displaying solution with DFS -")
#             self.trace_path(self.dim - 1, self.dim - 1)
#             for i in range(self.dim):
#                 print(*self.arr[i], sep=' ')
#         else:
#             print("Maze is not solvable.")


# class BFSSolver(Maze):
#     path = []
#     max_fringe = 0
#     nodes_expanded = 0
#     path_length = 0

#     def __init__(self, maze_arr):
#         super().__init__(0, 0, maze_arr)
#         self.visited = set()
#         self.parent = dict()
#         self.queue = []
#         self.is_solvable = False

#     def find_path(self, cur_i, cur_j):
#         self.queue.append((cur_i, cur_j))
#         self.visited.add((cur_i, cur_j))
#         while self.queue:
#         	# max_fringe = max(max_fringe, len(queue))
#             cur_i, cur_j = self.queue.pop(0)
#             self.max_fringe = max(self.max_fringe, len(self.queue))
#             self.nodes_expanded += 1
#             for i in range(cur_i - 1, cur_i + 2):
#                 for j in range(cur_j - 1, cur_j + 2):
#                     if 0 <= i < self.dim and 0 <= j < self.dim and abs(
#                             i - cur_i) + abs(j - cur_j) == 1 and self.arr[i][j] != 'X' and (i, j) not in self.visited:
#                         self.parent[(i, j)] = (cur_i, cur_j)
#                         self.visited.add((i, j))
#                         self.queue.append((i, j))
#                         if self.arr[i][j] == 'G':
#                             self.is_solvable = True
#                             return

#     def trace_path(self, goal_i, goal_j):
#         i, j = goal_i, goal_j
#         while (i, j) != (0, 0):
#             i, j = self.parent[(i, j)]
#             self.path.append((i, j))
#         self.path.pop()
#         for i, j in self.path:
#             self.arr[i][j] = '#'
#         self.path_length = len(self.path)

#     def display_solution(self):
#         self.find_path(0, 0)
#         if self.is_solvable:
#             print("Displaying solution with BFS -")
#             self.trace_path(self.dim - 1, self.dim - 1)
#             for i in range(self.dim):
#                 print(*self.arr[i], sep=' ')
#         else:
#             print("Maze is not solvable.")


# def find_hard_maze(mazes):
# 	ans_arr = []
# 	for index, maze in enumerate(mazes):
# 		B = DFSSolver(maze)
# 		B.find_path(0, 0)
# 		if B.is_solvable:
# 			ans_arr.append((B.path_length, index))
# 		else:
# 			ans_arr.append((-1, index))
# 	ans_arr.sort(reverse = True)
# 	if ans_arr[0][0] == -1:
# 		return -1
# 	print(ans_arr[0][0])
# 	return ans_arr[0][1]


# if __name__ == '__main__':
# 	ls = []
# 	arr = []
# 	dim, p = 10, 0.3
# 	for i in range(dim):
# 		tmp = []
# 		for j in range(dim):
# 			x = 'X' if random.random() < p else 'O'
# 			tmp.append(x)
# 		arr.append(tmp)
# 	arr[0][0] = 'S'
# 	arr[dim - 1][dim - 1] = 'G'
# 	abc = copy.deepcopy(arr)
# 	for tmp in arr:
# 		print(*tmp, sep = ' ')
# 	print('\n\n\n')
# 	bfs1 = BFSSolver(arr)
# 	bfs1.display_solution()
# 	print('\n\n\n')
# 	iters = 1000
# 	x, y = random.randint(0, dim - 1), random.randint(0, dim - 1)
# 	for i in range(iters):
# 		mazes = [arr]
# 		temp = [(x -1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
# 		random.shuffle(temp)
# 		for p, q in temp:
# 			if 0 <= p < dim and 0 <= q < dim and (p, q) != (0, 0) and (p, q) != (dim - 1, dim - 1):
# 				new_arr = copy.deepcopy(arr)
# 				new_arr[p][q] = ('O' if new_arr[p][q] == 'X' else 'X')
# 				mazes.append(new_arr)
# 		ans = find_hard_maze(mazes)
# 		ls.append(ans)
# 		# print(ans)
# 		if ans <= 0 or random.random() <= 0.2:
# 			x, y = random.randint(0, dim - 1), random.randint(0, dim - 1)
# 		else:
# 			arr = mazes[ans]
# 			x, y = temp[ans - 1]
# 	# for tmp in abc:
# 	# 	print(*tmp, sep = ' ')
# 		# print('\n\n\n')
# 	c = 0
# 	for i in range(dim):
# 		for j in range(dim):
# 			if abc[i][j] != arr[i][j]:
# 				c += 1
# 	print('\n\n\n')
# 	# arr = [[x if x != '#' else 'O' for x in tmp] for tmp in arr]
# 	# B = BFSSolver(arr)
# 	# B.display_solution()
# 	for tmp in arr:
# 		print(*tmp, sep=' ')
# 	print(c)
# 	abc = copy.deepcopy(arr)
# 	bfs2 = DFSSolver(abc)
# 	bfs2.display_solution()
# 	# print(*ls, sep = ' ')


def bfs(arr, is_path = False):
	path = []
	queue = []
	visited = set()
	queue.append((0, 0))
	visited.add((0, 0))
	parent_node = {}
	while queue:
		# nodes_expanded += 1
		cur_i, cur_j = queue.pop(0)
		if arr[cur_i][cur_j] == 'G':
			ans = 0
			while cur_i + cur_j:
				path.append((cur_i, cur_j))
				cur_i, cur_j = parent_node[(cur_i, cur_j)]
				ans += 1
			if is_path:
				for p, q in path:
					if arr[p][q] in ['O', 'X']:
						arr[p][q] = '#'
				display_maze(arr)
				return
			else:
				return ans
			# return ans
		for i, j in [(cur_i - 1, cur_j), (cur_i + 1, cur_j), (cur_i, cur_j - 1), (cur_i, cur_j + 1)]:
			if 0 <= i < len(arr) and 0 <= j < len(arr) and arr[i][j] != 'X' and (i, j) not in visited:
				queue.append((i, j))
				parent_node[(i, j)] = (cur_i, cur_j)
				visited.add((i, j))
	return -1


def find_best_maze(maze_list):
	ans_arr = []
	for index, maze in enumerate(maze_list):
		nodes_expanded = bfs(maze)
		ans_arr.append((nodes_expanded, random.random(), index))
	ans_arr.sort(reverse = True)
	return ans_arr[0][-1]


def display_maze(maze):
	for row in maze:
		print(*row, sep = ' ')
	print('\n\n')

if __name__ == '__main__':
	# Creating a random maze
	dim, p, iters = 15, 0.3, 100
	maze = []
	for i in range(dim):
		tmp = []
		for j in range(dim):
			tmp.append('X' if random.random() < p else 'O')
		maze.append(tmp)
	maze[0][0] = 'S'
	maze[dim - 1][dim - 1] = 'G'
	print("Displaying maze from part-1: ")
	display_maze(maze)
	print("Displaying maze from part-1 with the shortest path: ")
	bfs(maze, True)
	for i in range(dim):
		for j in range(dim):
			if maze[i][j] == '#':
				maze[i][j] = 'O'
	x, y = random.randint(0, dim - 1), random.randint(0, dim - 1)
	for _ in range(iters):
		maze_list = [maze]
		for i, j in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
			if 0 <= i < dim and 0 <= j < dim and maze[i][j] in ['O', 'X']:
				arr = copy.deepcopy(maze)
				arr[i][j] = 'O' if arr[i][j] == 'X' else 'X'
				maze_list.append(arr)
		index = find_best_maze(maze_list)
		maze = maze_list[index]
		# print(index)
		if index:
			x, y = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)][index - 1]
		else:
			x, y = random.randint(0, dim - 1), random.randint(0, dim - 1)
	print("Displaying maze after hill climbing: ")
	display_maze(maze)
	print("Displaying maze with the shortest path after hill climbing: ")
	bfs(maze, True)