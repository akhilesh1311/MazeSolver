import maze
import maze_solver

if __name__ == '__main__':
	M = maze.HardMaze(30, 0.2)	# Creating hard maze with given dimension and initial probability
	M.terminate(500, 2)	# Do hill climbing to make the maze harder with step = 500 and percentage difference = 2
	B = maze_solver.BFSSolver(M)
	D = maze_solver.DFSSolver(M)
	B.display_solution()
	D.display_solution()
	print("BFS Solution:\n(i) Solution length - {}\n(ii) Number of nodes expanded - {}\n(iii) Maximum size of the fringe - {}\n".format(B.solution_length, B.nodes_expanded, B.max_fringe_size))
	print("DFS Solution:\n(i) Solution length - {}\n(ii) Number of nodes expanded - {}\n(iii) Maximum size of the fringe - {}\n".format(D.solution_length, D.nodes_expanded, D.max_fringe_size))	