import pickle
from os import listdir
from os.path import isfile, join
from maze import Maze
from maze_solver import DFSSolver, AStarSolver
import matplotlib.pyplot as plt

pvals = [x/100 for x in range(10,35,5)]
dim = 1000
nodes_expanded = dict(
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

            nodes_expanded['ase'][p].append(s1.nodes_expanded)
            nodes_expanded['asm'][p].append(s2.nodes_expanded)
    
asm = [sum(nodes_expanded['asm'][p])/len(nodes_expanded['asm'][p]) for p in pvals]
ase = [sum(nodes_expanded['ase'][p])/len(nodes_expanded['ase'][p]) for p in pvals]

plt.plot(pvals,asm,pvals,ase)
ax = plt.gca()
ax.legend(('A* (M)', 'A* (E)'))
plt.xlabel("p-value")
plt.ylabel("Avg. No. of Nodes Expanded")
plt.savefig("q6.png")
plt.show()