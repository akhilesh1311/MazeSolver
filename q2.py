from visualization import MazeVisualization
import sys
import pickle

# handle arguments
if len(sys.argv) == 1:
    raise Exception("please provide valid argument.")
elif sys.argv[1] not in ('bfs', 'dfs', 'ase','asm'):
    raise Exception("please provide valid argument.")
elif len(sys.argv) > 2:
    raise Exception("too many input arguments. please provide valid argument.")

# load maze and solver objects
with open('q2.p','rb') as f:
    q2 = pickle.load(f)

maze = q2['maze']
if sys.argv[1] == 'bfs':
    s = q2['bfs']
    s.name = 'bfs'
elif sys.argv[1] == 'dfs':
    s = q2['dfs']
    s.name = 'dfs'
elif sys.argv[1] == 'ase':
    s = q2['ase']
    s.name = 'ase'
elif sys.argv[1] == 'asm':
    s = q2['asm']
    s.name = 'asm'

# show animation
vis = MazeVisualization(maze, solver=s, cell_size=1, fname=None)
vis.maze_animation()

