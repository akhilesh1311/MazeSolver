import pickle
from os import listdir
from os.path import isfile, join
from maze import Maze
from maze_solver import DFSSolver, AStarSolver
import matplotlib.pyplot as plt

pvals = [x/100 for x in range(10,35,5)]
dim = 1000
paths = dict(
    dfs={p:[] for p in pvals},
    ase={p:[] for p in pvals},
    asm={p:[] for p in pvals}
)

for p in pvals:
    count = 0
    while count < 30:
        m = Maze(dim, p)
        d = DFSSolver(m)
        d.display_solution(display=False)
        if d.is_solvable:
            count += 1

            s1 = AStarSolver(m, 'M')
            print(f"solving maze {count} for p={p}...")
            s1.display_solution(display=False)

            assert s1.is_solvable == True

            s2 = AStarSolver(m, 'E')
            print(f"solving maze {count} for p={p}...")
            s2.display_solution(display=False)

            assert s2.is_solvable == True

            paths['dfs'][p].append(len(d.path)+1)
            paths['asm'][p].append(len(s1.path)+1)
            paths['ase'][p].append(len(s2.path)+1)
    
dfs_path_length = [sum(paths['dfs'][p])/len(paths['dfs'][p]) for p in pvals]
asm_path_length = [sum(paths['asm'][p])/len(paths['asm'][p]) for p in pvals]
ase_path_length = [sum(paths['ase'][p])/len(paths['ase'][p]) for p in pvals]

plt.plot(pvals,dfs_path_length,pvals,asm_path_length,pvals,ase_path_length)
ax = plt.gca()
ax.legend(('DFS', 'A* (M)', 'A* (E)'))
plt.xlabel("p-value")
plt.ylabel("Expected Path Length")
plt.savefig("q5.png")
plt.show()

