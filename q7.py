import pickle
from os import listdir
from os.path import isfile, join
from maze import Maze
from maze_solver import DFSSolver, BFSSolver
import matplotlib.pyplot as plt

pvals = [x/100 for x in range(10,35,5)]
dim = 1000
nodes_expanded = dict(
    dfs={p:[] for p in pvals},
    bfs={p:[] for p in pvals}
)

for p in pvals:
    count = 0
    while count < 30:
        m = Maze(dim, p)
        d = DFSSolver(m)
        d.display_solution(display=False)
        if d.is_solvable:
            count += 1

            s = BFSSolver(m)
            print(f"solving maze {count} for p={p}...")
            s.display_solution(display=False)

            assert s.is_solvable == True

            nodes_expanded['dfs'][p].append(s.nodes_expanded)
            nodes_expanded['bfs'][p].append(s2.nodes_expanded)
    
bfs = [sum(nodes_expanded['bfs'][p])/len(nodes_expanded['bfs'][p]) for p in pvals]
dfs = [sum(nodes_expanded['dfs'][p])/len(nodes_expanded['dfs'][p]) for p in pvals]

plt.plot(pvals,bfs,pvals,dfs)
ax = plt.gca()
ax.legend(('BFS', 'DFS'))
plt.xlabel("p-value")
plt.ylabel("Avg. No. of Nodes Expanded")
plt.savefig("q7.png")
plt.show()

