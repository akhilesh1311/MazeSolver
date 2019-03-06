# MazeSolver

We generate a random maze, and use A*, BFS and DFS algorithms to solve it.
Next, we use local search algorithm of random walk to find a maze that is difficult to be solved by A*, BFS and DFS.

### Prerequisites

```
pip install -r requirements.txt
```

## Running the application

For help on input:
```
python main.py -h
```

For generating an easy maze:
```
python3 main.py -d 20 -p 0.2 -type easy -solver ase
```

For generating a hard maze:
```
python3 main.py -d 20 -p 0.2 -type hard -solver ase -step 800 -diff 2 -iters 5000
```

For visualization:
```
python q2.py
```

### Runtime Parameters

* -h, --help : Show help message and exit
* -d <int> : maze of dimension (dim, dim)
* -p <float> : probability of each cell being a blocked cell
* -type <easy/hard> : easy/hard maze
* -solver <bfs/dfs/ase/asm> : solver from a set of solvers of {dfs, bfs, ase, asm} ase - A* with Manhattan Distance, asm - A* with Euclidean Distance
* -step <int> : set a value of step to generate a hard maze.
* -diff <float> : set a % threshold difference value to generate a hard maze.
* -iters <int> : set the maximum number of iterations of hill climbing to generate a hard maze.


## Sample Visualizations

A hard maze found using local search for A* with Euclidean distance.

![Alt text](ase_1.png?raw=true "A* Euclidean")


A hard maze found using local search for BFS.

![Alt text](bfs_1.png?raw=true "BFS")


A hard maze found using local search for DFS.

![Alt text](dfs_1.png?raw=true "DFS")


## Acknowledgments

* Kunal Shah
* Vedang Mehta
* Nick Romanov
