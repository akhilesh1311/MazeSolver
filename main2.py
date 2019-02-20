import heapq
import random
import math
from datetime import datetime
import numpy as np
import sys
import pickle
import time

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
	def get_dim(self):
		return self.dim
	def get_p(self):
		return self.p
	def get_arr(self):
		return self.arr
	def display(self):
		for i in range(self.dim):
			print(*self.arr[i], sep=' ')


class Astar(object):
	fringe = []
	heuristic_type = ""
	heuristic = {}
	solvable = False
	max_fringe_size = 0
	total_fringe_size = 0
	avg_fringe_size = 0
	path_length = 0
	total_nodes_expanded = 0
	final_path = []
	actual_cost = dict()


	def __init__(self, maze, heuristic_type="E", timeout=None):
		#heuristic_type is either "M" for manhattan or "E" for euclidean
		self.heuristic_type = heuristic_type
		self.maze = maze
		self.dim = maze.get_dim()
		self.heuristic_cal()
		self.visited = np.zeros((self.dim, self.dim), dtype=bool)
		self.parent = dict()
		self.actual_cost[(0,0)] = 0
		self.timeout = timeout
		self.solve_time = None

	def heuristic_cal(self):
		if self.heuristic_type == "M":
			for i in range(self.maze.get_dim()):
				for j in range(self.maze.get_dim()):
					if self.maze.get_arr()[i][j] == 'O':
						self.heuristic[(i,j)]= self.dim-i-1 + self.dim-j-1
		else:
			for i in range(self.maze.get_dim()):
				for j in range(self.maze.get_dim()):
					if self.maze.get_arr()[i][j] == 'O':
						self.heuristic[(i,j)]=math.sqrt((self.dim-1-i)**2 + (self.dim-1-j)**2)
		self.heuristic[(self.dim-1, self.dim-1)] = 0

	class node:
		def __init__(self, i, j, total_cost):
			self.i = i
			self.j = j
			self.total_cost = total_cost
		def __gt__(self, node):
			return self.total_cost > node.total_cost

	def traverse(self):
		t0 = time.time()
		curr_i = 0
		curr_j = 0
		iterations = 0
		n1 = Astar.node(0, 0, 0)
		self.parent[(0,0)] = (-1, -1)
		heapq.heappush(self.fringe, n1)
		self.visited[0][0] = True

		while curr_i != (self.dim-1) or curr_j != (self.dim-1):
			if len(self.fringe) == 0:
				print("No solution exists")
				self.avg_fringe_size = self.total_fringe_size/iterations
				return 0
			iterations = iterations + 1
			if len(self.fringe) > self.max_fringe_size:
				self.max_fringe_size = len(self.fringe)

			self.total_fringe_size = self.total_fringe_size + len(self.fringe)
			curr_node = heapq.heappop(self.fringe)
			curr_i = curr_node.i
			curr_j = curr_node.j

			#for peeping up
			if ((curr_i-1)>=0 and self.visited[curr_i-1][ curr_j] == False and self.maze.get_arr()[curr_i-1][curr_j] != 'X'):
				self.actual_cost[(curr_i-1, curr_j)] = self.actual_cost[(curr_i, curr_j)] + 1
				temp = Astar.node(curr_i-1, curr_j, self.actual_cost[(curr_i-1, curr_j)]+self.heuristic[(curr_i-1,curr_j)])
				heapq.heappush(self.fringe, temp)
				self.parent[(curr_i-1, curr_j)] = (curr_i, curr_j)
				self.total_nodes_expanded = self.total_nodes_expanded + 1
				self.visited[curr_i-1][curr_j] = True

			#for peeping down
			if ((curr_i+1)<self.dim and self.visited[curr_i+1][ curr_j] == False and self.maze.get_arr()[curr_i+1][curr_j] != 'X'):
				self.actual_cost[(curr_i + 1, curr_j)] = self.actual_cost[(curr_i, curr_j)] + 1
				temp = Astar.node(curr_i+1, curr_j, self.actual_cost[(curr_i + 1, curr_j)]+self.heuristic[(curr_i+1,curr_j)])
				heapq.heappush(self.fringe, temp)
				self.parent[(curr_i+1, curr_j)] = (curr_i, curr_j)
				self.total_nodes_expanded = self.total_nodes_expanded + 1
				self.visited[curr_i+1][curr_j] = True

			#for peeping left
			if ((curr_j-1)>=0 and self.visited[curr_i][ curr_j-1] == False and self.maze.get_arr()[curr_i][curr_j-1] != 'X'):
				self.actual_cost[(curr_i, curr_j-1)] = self.actual_cost[(curr_i, curr_j)] + 1
				temp = Astar.node(curr_i, curr_j-1, self.actual_cost[(curr_i, curr_j-1)]+self.heuristic[(curr_i,curr_j-1)])
				heapq.heappush(self.fringe, temp)
				self.parent[(curr_i, curr_j-1)] = (curr_i, curr_j)
				self.total_nodes_expanded = self.total_nodes_expanded + 1
				self.visited[curr_i][curr_j-1] = True

			#for peeping right
			if ((curr_j+1)<self.dim and self.visited[curr_i][ curr_j+1] == False and self.maze.get_arr()[curr_i][curr_j+1] != 'X'):
				self.actual_cost[(curr_i, curr_j+1)] = self.actual_cost[(curr_i, curr_j)] + 1
				temp = Astar.node(curr_i, curr_j+1, self.actual_cost[(curr_i, curr_j+1)]+self.heuristic[(curr_i,curr_j+1)])
				heapq.heappush(self.fringe, temp)
				self.parent[(curr_i, curr_j+1)] = (curr_i, curr_j)
				self.total_nodes_expanded = self.total_nodes_expanded + 1
				self.visited[curr_i][curr_j+1] = True

			if self.timeout:
				t = time.time()
				if t - t0 > self.timeout:
					print("Solver timed out.")
					return

		self.solvable = True
		self.avg_fringe_size = self.total_fringe_size/iterations
		self.solve_time = round(time.time()-t0,2)


	def trace_path(self, display=False):
		curr_i = self.dim-1
		curr_j = self.dim-1
		if self.solvable == True:
			curr_i, curr_j = self.parent[(curr_i, curr_j)]
			self.path_length = self.path_length + 1
			while self.maze.get_arr()[curr_i][curr_j] != 'S':
				self.path_length = self.path_length + 1
				self.maze.get_arr()[curr_i][curr_j] = '#'
				self.final_path.insert(0, (curr_i, curr_j))
				curr_i, curr_j = self.parent[(curr_i, curr_j)]
			if display:
				for i in range(self.dim):
					print(*self.maze.get_arr()[i], sep = ' ')
		else:
			print("Maze is not solvable")

	def print_stats(self):
		print("A*\nPath length: ",self.path_length, "Max fringe size ", self.max_fringe_size, "avg fringe size ", self.avg_fringe_size, "total nodes expanded ", self.total_nodes_expanded)


class DFSSolver(Maze):
	path = []
	dfs_stack = []
	def __init__(self, MazeObject, timeout=None):
		super().__init__(0, 0, MazeObject.arr)
		self.visited = set()
		self.parent = dict()
		self.is_solvable = False
		self.timeout = timeout
		self.solve_time = None

	def find_path(self, cur_i, cur_j):
		t0 = time.time()
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
							self.solve_time = round(time.time()-t0, 2)
							return
					if self.timeout:
						t = time.time()
						if (t - t0) > self.timeout:
							print("Solver timed out.")
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
	max_fringe_size = 0
	avg_fringe_size = 0
	total_nodes_expanded = 0

	def __init__(self, MazeObject, timeout=None):
		super().__init__(0, 0, MazeObject.arr)
		self.visited = set()
		self.parent = dict()
		self.queue = []
		self.is_solvable = False
		self.timeout = timeout
		self.solve_time = None

	def find_path(self, cur_i, cur_j):
		t0 = time.time()
		iterations = 0
		total_fringe_size = 0
		self.queue.append((cur_i, cur_j))
		self.visited.add((cur_i, cur_j))
		while self.queue:
			iterations = iterations + 1
			if len(self.queue) > self.max_fringe_size:
				self.max_fringe_size = len(self.queue)
			total_fringe_size = total_fringe_size + len(self.queue)
			cur_i, cur_j = self.queue.pop(0)
			for i in range(cur_i - 1, cur_i + 2):
				for j in range(cur_j - 1, cur_j + 2):
					if 0 <= i < self.dim and 0 <= j < self.dim and abs(
							i - cur_i) + abs(j - cur_j) == 1 and self.arr[i][j] != 'X' and (i, j) not in self.visited:
						self.parent[(i, j)] = (cur_i, cur_j)
						self.visited.add((i, j))
						self.queue.append((i, j))
						self.total_nodes_expanded = self.total_nodes_expanded + 1
						if self.arr[i][j] == 'G':
							self.is_solvable = True
							self.avg_fringe_size = total_fringe_size/iterations
							self.solve_time = round(time.time()-t0,2)
							return
					if self.timeout:
						t = time.time()
						if t - t0 > self.timeout:
							print("Solver timed out.")
							return


	def trace_path(self, goal_i, goal_j):
		i, j = goal_i, goal_j
		while (i, j) != (0, 0):
			i, j = self.parent[(i, j)]
			self.path.append((i, j))
		self.path.pop()
		for i, j in self.path:
			self.arr[i][j] = '#'

	def display_solution(self, display=False):
		self.find_path(0, 0)
		if self.is_solvable:
			print("Displaying solution with BFS -")
			self.trace_path(self.dim - 1, self.dim - 1)
			if display:
				for i in range(self.dim):
					print(*self.arr[i], sep=' ')
		else:
			print("Maze is not solvable.")

	def print_stats(self):
		print("BFS\nPath length: ", len(self.path), "Max fringe size ", self.max_fringe_size, "avg fringe size ",
					self.avg_fringe_size, "total nodes expanded ", self.total_nodes_expanded)


def save_object(obj, filename):
	with open(filename, 'wb') as output:
		pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)

if __name__ == '__main__':
	heuristic_time = 0
	traversal_time = 0
	if len(sys.argv) == 4:
		M = Maze(int(sys.argv[1]), float(sys.argv[2]))
		save_object(M, "M.pkl")
		startTime = datetime.now()
		a = Astar(M, sys.argv[3])
		heuristic_time = datetime.now() - startTime
	elif len(sys.argv) == 3:
		M = Maze(int(sys.argv[1]), float(sys.argv[2]))
		save_object(M, "M.pkl")
		# m.display()
		startTime = datetime.now()
		a = Astar(M)
		heuristic_time = datetime.now() - startTime
	elif len(sys.argv) == 2:
		file = open("M.pkl", 'rb')
		object_file = pickle.load(file)
		M = object_file
		startTime = datetime.now()
		a = Astar(M, sys.argv[1])
		heuristic_time = datetime.now() - startTime
	else:
		print("enter dim, probability and M/E for Manhattan/Euclidean..or just M/E for using the previously generated maze")
		sys.exit(0)
	startTime = datetime.now()
	a.traverse()
	a.trace_path()
	traversal_time = datetime.now() - startTime
	a.print_stats()
	print("A* heuristic_time: ", heuristic_time, "  A* traversal_time: ", traversal_time, "  A* total time: ", heuristic_time+traversal_time)
	print()

	try:
		startTime = datetime.now()
		D = DFSSolver(M)
		D.display_solution()
		D.print_stats()
		print("Total time for DFS: ", datetime.now() - startTime)
		print()
	except Exception as e:
		print(str(e))
		print()

	startTime = datetime.now()
	B = BFSSolver(M)
	B.display_solution()
	B.print_stats()
	print("Total time for BFS: ", datetime.now() - startTime)
