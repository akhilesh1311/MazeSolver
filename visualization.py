import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
from main import Maze, DFSSolver, BFSSolver, Astar


class MazeVisualization(object):

	def __init__(self, maze, solver=None, cell_size=1, fname='maze'):
		self.maze = maze
		self.cell_size = cell_size
		self.fname = fname
		self.ax = None
		self.cells = dict()
		self.solver = solver

	def initialize(self):

		fig = plt.figure()
		self.ax = plt.axes()
		self.ax.set_aspect("equal")
		plt.axis('off')

		return fig

	def plot_maze_grid(self):

		# plot maze boundaries, start, and goal cells
		for i in range(len(self.maze.arr)):
			for j in range(len(self.maze.arr[i])):

				# cell boundaries
				self.ax.plot([j*self.cell_size, (j+1)*self.cell_size],
									[i*self.cell_size, i*self.cell_size], color="gray")
				self.ax.plot([(j+1)*self.cell_size, (j+1)*self.cell_size],
									[i*self.cell_size, (i+1)*self.cell_size], color="gray")
				self.ax.plot([(j+1)*self.cell_size, j*self.cell_size],
									[(i+1)*self.cell_size, (i+1)*self.cell_size], color="gray")
				self.ax.plot([j*self.cell_size, j*self.cell_size],
									[(i+1)*self.cell_size, i*self.cell_size], color="gray")

				# occupied cell
				if self.maze.arr[-(i+1)][j] == 'X':
					rect = plt.Rectangle([j*self.cell_size, i*self.cell_size], self.cell_size, self.cell_size,
																facecolor="k", edgecolor="k")
					self.ax.add_patch(rect)

				# start cell
				if self.maze.arr[-(i+1)][j] == 'S':
					self.ax.text(j*self.cell_size+0.25, i*self.cell_size+0.25, "S", fontsize=7, weight="bold")

				# goal cell
				if self.maze.arr[-(i+1)][j] == 'G':
					self.ax.text(j*self.cell_size+0.25, i*self.cell_size+0.25, "G", fontsize=7, weight="bold")
				
				# add cells for showing solution path
				self.cells[f"{i},{j}"] = plt.Rectangle((j*self.cell_size,
							-(i-self.maze.dim+1)*self.cell_size), self.cell_size, self.cell_size,
							facecolor = "blue", alpha = 0.4, visible = False)
				self.ax.add_patch(self.cells[f"{i},{j}"])

	def display_maze(self):

		fig = self.initialize()
		self.plot_maze_grid()
		plt.show()

	def maze_animation(self):

		if self.solver.name.lower() == 'bfs' or self.solver.name.lower() == 'dfs': 
			# self.solver.find_path(0,0)
			solvable = self.solver.is_solvable
		elif self.solver.name.lower() == 'ase' or self.solver.name.lower() == 'asm':
			# self.solver.traverse()
			solvable = self.solver.solvable
		

		if solvable:

			fig = self.initialize()
			self.plot_maze_grid()

			if self.solver.name.lower() == 'bfs' or self.solver.name.lower() == 'dfs':
				# get solution path
				self.solver.trace_path(self.maze.dim - 1, self.maze.dim - 1)
				# reverse solution so it displays from start to goal
				self.solver.path.reverse()
			elif self.solver.name.lower() == 'ase' or self.solver.name.lower() == 'asm':
				# get solution path
				self.solver.trace_path()

			# enable start and goal nodes
			self.cells["0,0"].set_alpha(0.8)
			self.cells["0,0"].set_visible(True)
			self.cells[f"{self.maze.dim-1},{self.maze.dim-1}"].set_alpha(0.8)
			self.cells[f"{self.maze.dim-1},{self.maze.dim-1}"].set_visible(True)
			
			def animate_cells(frame):
				if frame > 0:
					if self.solver.name.lower() == 'bfs' or self.solver.name.lower() == 'dfs':
						self.cells[f"{self.solver.path[frame-1][0]},{self.solver.path[frame-1][1]}"].set_visible(True)
					elif self.solver.name.lower() == 'ase' or self.solver.name.lower() == 'asm':
						self.cells[f"{self.solver.final_path[frame-1][0]},{self.solver.final_path[frame-1][1]}"].set_visible(True)
				return []

			def animate(frame):
				animate_cells(frame)
				return []

			# get number of frames
			if self.solver.name.lower() == 'bfs' or self.solver.name.lower() == 'dfs':
				num_frames = len(self.solver.path) + 1
			elif self.solver.name.lower() == 'ase' or self.solver.name.lower() == 'asm':
				num_frames = len(self.solver.final_path) + 1

			anim = animation.FuncAnimation(fig, animate, frames=num_frames,
					interval=100, blit=True, repeat=True)

			if self.solver.name.lower() == 'bfs':
				title = "BFS"
			elif self.solver.name.lower() == 'dfs':
				title = "DFS"
			elif self.solver.name.lower() == 'ase':
				title = "A* w/ Euclidean Distance"
			elif self.solver.name.lower() == 'asm':
				title = "A* w/ Manhattan Distance"

			plt.title(title)
			plt.show()

			# Handle any saving
			if self.fname:
				
				print('Saving animation...')
				mpeg_writer = animation.FFMpegWriter(fps=24, bitrate=-1)
				anim.save(f"{self.fname}_{self.maze.dim}x{self.maze.dim}_{self.maze.p}_solution.mp4",  writer=mpeg_writer)
				print('Done.')
		else: 
			print("Maze is not solvable.")

if __name__ == '__main__':

	
	M = Maze(10,0.3)
	D = DFSSolver(M)
	B = BFSSolver(M)
	A = Astar(M)
	Vis = MazeVisualization(M, solver=A, cell_size=1, fname=None)
	Vis.maze_animation()

