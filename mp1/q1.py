import Queue
import random

from mp1.parser import parse_args, parse_matrix, dump_matrix


def counter():
    """
    This is a counter to mark the order of pellets traversed.

    :return: Generator
    """
    order = ord('0')
    while 1:
        if order == ord('9'):
            order = ord('a')
        elif order == ord('z'):
            order = ord('A')
        else:
            order += 1
        yield chr(order)

_count = counter()


def finalize(matrix, dest, filename, nodes_expanded, dot=False):
    """
    Print the statistics and compute the cost (if necessary)

    :param matrix: The maze
    :param dest: The final pellet
    :param filename: Desired filename to dump the solution maze
    :param nodes_expanded: Number of nodes expanded
    :param dot: Whether to mark the path with dots
    """
    cost = 0
    tmp = dest
    if dot:
        # Trace maze
        while tmp:
            tmp.val = '.'
            cost += 1
            tmp = tmp.parent

    # Dump maze
    dump_matrix(matrix, filename)
    print 'Maze dumped to %s: Total cost %d, %d nodes expanded' % (filename, cost - 1 if dot else dest.cost, nodes_expanded)


def neighbors(matrix, x, y):
    """
    Return the array of neighbors based on current coordinates.

    :param matrix: The maze
    :param x: x coordinate
    :param y: y coordinate
    :return: Array of neighboring cells
    """
    retval = []
    if x > 0:
        retval.append(matrix[x - 1][y])
    if x < len(matrix) - 1:
        retval.append(matrix[x + 1][y])
    if y > 0:
        retval.append(matrix[x][y - 1])
    if y < len(matrix[0]) - 1:
        retval.append(matrix[x][y + 1])
    return retval


def manhattan(cell1, cell2):
    return abs(cell1.x - cell2.x) + abs(cell1.y - cell2.y)


def manhattan_heuristic(cell, pellets):
    """
    Calculate the heuristic based on the minimum Manhattan distance among all distances

    :param cell: Certain position
    :param pellets: The set of unvisited pellets
    :return: The proper heuristic value for cell
    """
    heuristic = None
    for pellet in pellets:
        if heuristic is None or manhattan(cell, pellet) < heuristic:
            heuristic = manhattan(cell, pellet)
    return heuristic


def suboptimal_heuristic(cell, pellets):
    """
    Suboptimal heuristic calculator using a random pellet among set of unvisited pellets.

    :param cell: Certain position
    :param pellets: The set of unvisited pellets
    :return: The proper heuristic value for cell
    """
    return manhattan_heuristic(cell, random.sample(pellets, 1))


def bfs(matrix, start_cell, filename):
    """
    BFS based search to single goal
    :param matrix: The maze
    :param start_cell: Starting cell
    :param filename: Filename to dump the result to
    """
    q = Queue.Queue()
    open_set = set()
    closed_set = set()
    expanded = 0

    q.put_nowait(start_cell)
    open_set.add(start_cell)
    while not q.empty():
        front = q.get_nowait()

        open_set.remove(front)
        closed_set.add(front)

        if front.val == '%':
            continue

        expanded += 1
        if front.val == '.':
            finalize(matrix, front, filename, expanded, True)
            return
        else:
            for neighbor in neighbors(matrix, front.x, front.y):
                if neighbor in open_set or neighbor in closed_set:
                    continue
                open_set.add(neighbor)
                neighbor.parent = front
                q.put_nowait(neighbor)


def dfs(matrix, start_cell, filename):
    """
    DFS based search to single goal
    :param matrix: The maze
    :param start_cell: Starting cell
    :param filename: Filename to dump the result to
    """
    s = []
    s.append(start_cell)
    traversed = set()
    expanded = 0

    traversed.add(start_cell)
    while s:
        front = s.pop()

        if front.val == '%':
            continue

        expanded += 1
        if front.val == '.':
            finalize(matrix, front, filename, expanded, True)
            return
        else:
            for neighbor in neighbors(matrix, front.x, front.y):
                if neighbor in traversed:
                    continue
                traversed.add(neighbor)
                neighbor.parent = front
                s.append(neighbor)


def greedy(matrix, start_cell, pellets, filename):
    """
    DFS based search to single goal

    :param matrix: The maze
    :param start_cell: Starting cell
    :param pellets: The set of pellets
    :param filename: Filename to dump the result to
    """
    q = Queue.PriorityQueue()
    open_set = set()
    closed_set = set()
    expanded = 0
    pellets_set = set(pellets)

    q.put(start_cell)
    open_set.add(start_cell)
    while not q.empty():
        front = q.get_nowait()
        if front in closed_set:
            continue

        open_set.remove(front)
        closed_set.add(front)
        if front.val == '%':
            continue

        x, y = front.x, front.y
        expanded += 1
        if front.val == '.':
            finalize(matrix, front, filename, expanded, True)
            return
        else:
            for neighbor in neighbors(matrix, x, y):
                if neighbor in closed_set:
                    continue

                heuristic = manhattan_heuristic(neighbor, pellets_set)
                if neighbor not in open_set or heuristic < neighbor.heuristic:
                    neighbor.heuristic = heuristic
                    neighbor.parent = front
                    open_set.add(neighbor)
                    q.put_nowait(neighbor)


def astar(matrix, start_cell, pellets, filename, dot=False, suboptimal=False):
    """
    A* Search to single or multiple goal

    :param matrix: The maze
    :param start_cell: Starting cell
    :param pellets: The set of pellets
    :param filename: Filename to dump the solution to
    :param dot: True to mark the solution path with dots (part 1)
        Otherwise only mark the order on pellets.
    :param suboptimal: True to run the A* Search using a suboptimal and inadmissible heuristic.
        Otherwise the heuristic will be based on the Manhattan distances of all unvisited pellets.
    """
    q = Queue.PriorityQueue()
    open_set = set()
    closed_set = set()
    pellets_set = set(pellets)
    expanded = 0

    q.put_nowait(start_cell)
    open_set.add(start_cell)
    while not q.empty():
        front = q.get_nowait()
        if front in closed_set:
            continue

        open_set.remove(front)
        closed_set.add(front)

        if front.val == '%':
            continue

        expanded += 1
        x, y = front.x, front.y
        if front.val == '.':
            pellets_set.remove(front)
            front.val = next(_count)
            if not pellets_set:
                finalize(matrix, front, filename, expanded, dot)
                return
            else:
                q = Queue.PriorityQueue()
                q.put_nowait(front)
                open_set = set([front])
                closed_set = set()
                tmp = front.cost
                for row in matrix:
                    for cell in row:
                        cell.cost = cell.heuristic = 0
                front.cost = tmp
        else:
            for neighbor in neighbors(matrix, x, y):
                if neighbor in closed_set:
                    continue
                cost = front.cost + 1
                if neighbor.x == 3 and neighbor.y == 15:
                    pass
                if not suboptimal:
                    heuristic = manhattan_heuristic(neighbor, pellets_set)
                else:
                    heuristic = suboptimal_heuristic(neighbor, pellets_set)
                if neighbor not in open_set or cost < neighbor.cost:
                    neighbor.cost = cost
                    neighbor.heuristic = heuristic
                    neighbor.parent = front
                    open_set.add(neighbor)
                    q.put_nowait(neighbor)


def main():
    args = parse_args()
    matrix, start_cell, pellets = parse_matrix(args.filename)

    if args.type == 'bfs':
        bfs(matrix, start_cell, '%s_%s_soln.txt' % (args.filename[:-4], args.type))
    elif args.type == 'dfs':
        dfs(matrix, start_cell, '%s_%s_soln.txt' % (args.filename[:-4], args.type))
    elif args.type == 'greedy':
        greedy(matrix, start_cell, pellets, '%s_%s_soln.txt' % (args.filename[:-4], args.type))
    elif args.type == 'astar':
        astar(matrix, start_cell, pellets, '%s_%s_soln.txt' % (args.filename[:-4], args.type), args.dot)
    elif args.type == 'suboptimal':
        astar(matrix, start_cell, pellets, '%s_%s_soln.txt' % (args.filename[:-4], args.type), args.dot, suboptimal=True)
    else:
        raise RuntimeError('Type not implemented')


if __name__ == '__main__':
    main()
