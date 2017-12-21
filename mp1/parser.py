import argparse


class Cell(object):
    """
    A Wrapper class for each position in a maze.
    """

    def __init__(self, x, y, val):
        self.x = x
        self.y = y
        self.val = val
        self.cost = 0
        self.heuristic = 0
        self.parent = None

    def __lt__(self, other):
        return self.cost + self.heuristic < other.cost + other.heuristic

    def __le__(self, other):
        return self.cost + self.heuristic <= other.cost + other.heuristic

    def __repr__(self):
        return '%d, %d' % (self.x, self.y)


def parse_matrix(filename):
    """
    Parse the text file into a 2D array with positions wrapped as Cell objects.

    :param filename: Path and filename of target maze
    :return: A tuple of: resulting 2D array, starting position and array of all pellets.
    """
    matrix = []
    pellets = []
    start_cell = None
    with open(filename) as f:
        x = 0
        for line in f.readlines():
            # Create a new row
            matrix.append([None] * len(line))

            for i in xrange(len(line)):
                matrix[x][i] = Cell(x, i, line[i])
                if line[i] == '.':
                    # If it's a pellet, add to pellets array
                    pellets.append(matrix[x][i])
                elif line[i] == 'P':
                    # Else if it's the start, set the starting position
                    start_cell = matrix[x][i]

            # Increase line number
            x += 1

    return matrix, start_cell, pellets


def parse_args():
    parser = argparse.ArgumentParser(description='CS 440 MP1: Search')
    parser.add_argument('-f', '--filename', type=str, help='Maze filename', required=True)
    parser.add_argument('-t', '--type', type=str, help='Type of search', default='bfs')
    parser.add_argument('-d', '--dot', help='Drawing dots on solution', action='store_true')
    return parser.parse_args()


def dump_matrix(matrix, filename):
    with open(filename, 'w+') as f:
        for row in matrix:
            tokens = []
            for c in row:
                tokens.append(c.val)
            f.write(''.join(tokens))


def test_dump():
    matrix, start_cell, pellets = parse_matrix('./assets/bigMaze.txt')
    dump_matrix(matrix, './assets/testDump.txt')


def test_parse_matrix():
    args = parse_args()

    matrix, start_cell, pellets = parse_matrix(args.filename)
    for row in matrix:
        print ''.join(map(lambda c: c.val, row))
    print 'x: %d, y: %d' % (start_cell.x, start_cell.y)


if __name__ == '__main__':
    test_dump()
