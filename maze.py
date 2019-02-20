import random
import copy


def shortest_path(maze):
	"""Returns the length of the shortest path from S to G in a maze. Returns -1 if maze is unsolvable."""
	path = []
	queue = []
	visited = set()
	queue.append((0, 0))
	visited.add((0, 0))
	parent_node = {}
	while queue:
		cur_i, cur_j = queue.pop(0)
		if maze[cur_i][cur_j] == 'G':
			while cur_i + cur_j:
				path.append((cur_i, cur_j))
				cur_i, cur_j = parent_node[(cur_i, cur_j)]
			return len(path)
		for i, j in [(cur_i - 1, cur_j), (cur_i + 1, cur_j), (cur_i, cur_j - 1), (cur_i, cur_j + 1)]:
			if 0 <= i < len(maze) and 0 <= j < len(maze) and maze[i][j] != 'X' and (i, j) not in visited:
				queue.append((i, j))
				parent_node[(i, j)] = (cur_i, cur_j)
				visited.add((i, j))
	return -1


def find_hardest_maze(maze_ls):	#maze_ls is a list of mazes
	"""Returns the index of the maze that has longest shortest path from S to G in maze_ls."""
	ans_arr = []
	for index, cur_maze in enumerate(maze_ls):
		shortest_path_length = shortest_path(cur_maze)
		ans_arr.append((shortest_path_length, random.random(), index))
	ans_arr.sort(reverse = True)
	return ans_arr[0][-1]


class Maze(object):
	"""Class to generate a simple maze"""
	def __init__(self, dim=0, p=0, maze_arr=[]):
		self.maze = []
		if dim != 0:
			self.dim = dim
			self.p = p
			for i in range(dim):
				tmp = []
				for j in range(dim):
					cell = 'X' if random.random() < p else 'O'
					tmp.append(cell)
				self.maze.append(tmp)
			self.maze[0][0] = 'S'
			self.maze[dim - 1][dim - 1] = 'G'
		else:
			for i in range(len(maze_arr)):
				tmp = []
				for j in range(len(maze_arr[i])):
					if maze_arr[i][j] == '#':
						tmp.append('O')
					else:
						tmp.append(maze_arr[i][j])
				self.maze.append(tmp)
			self.dim = len(maze_arr)

	def display(self):
		for i in range(self.dim):
			print(*self.maze[i], sep=' ')


class HardMaze(Maze):
	"""Class to generate hard mazes"""
	__maze_fringe = []

	def __init__(self, dim, p):
		super().__init__(dim, p)

	def iterate(self, iters):
		"""Does iters number of iterations of hill climbing to make the maze more difficult to solve."""
		x, y = random.randint(0, self.dim - 1), random.randint(0, self.dim - 1)
		for _ in range(iters):
			self.__maze_fringe = [self.maze]
			for i, j in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
				if 0 <= i < self.dim and 0 <= j < self.dim and self.maze[i][j] in ['O', 'X']:
					arr = copy.deepcopy(self.maze)
					arr[i][j] = 'O' if arr[i][j] == 'X' else 'X'
					self.__maze_fringe.append(arr)
			index = find_hardest_maze(self.__maze_fringe)
			self.maze = self.__maze_fringe[index]
			if index:
				x, y = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)][index - 1]
			else:
				x, y = random.randint(0, self.dim - 1), random.randint(0, self.dim - 1)

	def terminate(self, step, diff_threshold, max_iters=1000):
		"""This function is used to make the simple maze harder to solve. 
		Instead of doing a fixed number of iterations, the process terminates whenever the increase in length of shortest path in maze falls below diff_threshold (in percentage) after steps number of iterations."""
		path_length_ls = []
		x, y = random.randint(0, self.dim - 1), random.randint(0, self.dim - 1)
		for _ in range(max_iters):
			self.__maze_fringe = [self.maze]
			path_length_ls.append(shortest_path(self.maze))
			for i, j in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
				if 0 <= i < self.dim and 0 <= j < self.dim and self.maze[i][j] in ['O', 'X']:
					arr = copy.deepcopy(self.maze)
					arr[i][j] = 'O' if arr[i][j] == 'X' else 'X'
					self.__maze_fringe.append(arr)
			index = find_hardest_maze(self.__maze_fringe)
			self.maze = self.__maze_fringe[index]
			if index:
				x, y = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)][index - 1]
			else:
				x, y = random.randint(0, self.dim - 1), random.randint(0, self.dim - 1)
			if len(path_length_ls) > step and (path_length_ls[-1] - path_length_ls[-step - 1]) * 100 / path_length_ls[-step - 1] < diff_threshold:
				break