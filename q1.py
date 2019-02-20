from maze import Maze
from maze_solver import AStarSolver, DFSSolver, BFSSolver
import time
import sys

""" Question 1 """

def search(solver, d=1000, p=0.1):
    
    solve_time = dict()
    timeout = 60
    maze = construct_maze(d, p)
    t = get_solve_time(maze, solver)
    solve_time[d] = t
    previous_d = d
    while True: # find maximum dimension
        if t is None:
            return
        if t < timeout: 
            previous_d = d
            d *= 2
            maze = construct_maze(d, p)
            time.sleep(2)
            t = get_solve_time(maze, solver)
            solve_time[d] = t
            continue
        else: 
            d0 = previous_d
            t0 = solve_time[d0]
            dmax = d
            break
    
    while True: # perform a binary search
        if t is None:
            return

        mid = (d0 + dmax) / 2
        maze = construct_maze(int(mid), p)
        time.sleep(2)
        t = get_solve_time(maze, solver)
        solve_time[mid] = t

        delta = abs(dmax - d0)
        if delta <= 1000 and (t<timeout):
            return #mid, t, solve_time

        if t is None:
            return

        if (t > timeout):
            dmax = mid
            continue
        elif (t > t0):
            d0 = mid
            t0 = t
            continue
        else:
            return #mid, t, solve_time
            

def construct_maze(d, p):

    print(f"constructing maze({d},{p})...")
    M = Maze(d, p)
    return M

def get_solve_time(maze, solver):

    if solver.name == 'bfs' or solver.name == 'dfs':
        print(f"solving maze({maze.dim},{maze.p})...")
        s = solver(maze)
        t0 = time.time()
        s.display_solution(display=False)
        td = round(time.time() - t0, 2)
        if s.is_solvable:  
            print(f"maze({maze.dim},{maze.p}) solved with {s.name} in {td}s.")
            return td
        else:
            print(f"maze({maze.dim},{maze.p}) not solvable.")
            return None
    elif solver.name == 'astar':
        s1 = solver(maze, 'E')
        t0 = time.time()
        s1.display_solution(display=False)
        td = round(time.time() - t0, 2)
        if s1.solvable:  
            print(f"maze({maze.dim},{maze.p}) solved with {s1.name}-{s1.heuristic_type} in {td}s.")
            return td
        else:
            print(f"maze({maze.dim},{maze.p}) not solvable.")
            return None
        
        s2 = solver(maze, 'M')
        t0 = time.time()
        s2.display_solution(display=False)
        td = round(time.time() - t0, 2)
        if s2.solvable:  
            print(f"maze({maze.dim},{maze.p}) solved with {s2.name}-{s2.heuristic_type} in {td}s.")
            return td
        else:
            print(f"maze({maze.dim},{maze.p}) not solvable.")
            return None
    

if __name__ == "__main__":

    # for i in range(10):
    #     m = Maze(2000,0.4)
    #     s = DFSSolver(m)
    #     t0 = time.time()
    #     s.find_path(0, 0)
    #     td = round(time.time() - t0, 2)
    #     if s.is_solvable:  
    #         print(f"maze({m.dim},{m.p}) solved in {td}s.")
    #     else:
    #         print(f"maze({m.dim},{m.p}) not solvable.")

    search(DFSSolver, d=2000, p=0.1)
    # search(BFSSolver, d=1000, p=0.1)
    # search(Astar, d=1000, p=0.1)