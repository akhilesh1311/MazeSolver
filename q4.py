import pickle
from os import listdir
from os.path import isfile, join
from maze import Maze
from maze_solver import DFSSolver, AStarSolver
import matplotlib.pyplot as plt

pvals = [x/100 for x in range(10,35,5)]
dim = 1000
paths = {p:[] for p in pvals}

for p in pvals:
    count = 0
    while count < 30:
        m = Maze(dim, p)
        d = DFSSolver(m)
        d.display_solution(display=False)
        if d.is_solvable:
            count += 1
            s = AStarSolver(m, 'M')
            print(f"solving maze {count} for p={p}...")
            s.display_solution(display=False, method='M')
            paths[p].append(len(s.path)+1)
    
avg_path_length = [sum(paths[p])/len(paths[p]) for p in pvals]
plt.plot(pvals,avg_path_length)
plt.xlabel("p-value")
plt.ylabel("Expected Path Length")
plt.savefig("q4.png")
plt.show()

