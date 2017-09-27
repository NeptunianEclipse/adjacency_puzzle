import timeit

class Tile():

    def __init__(self, name, values):
        self.name = name
        self.values = values

    def __repr__(self):
        return self.name + "(" + str(self.values)[1:-1] + ")"

board = [
    [Tile("A", [1, 6, 1, 4]), Tile("B", [2, 4, 7, 5]), Tile("C", [7, 1, 1, 4]), Tile("D", [1, 7, 0, 2])],
    [Tile("E", [0, 0, 1, 5]), Tile("F", [0, 5, 4, 2]), Tile("G", [4, 2, 4, 4]), Tile("H", [1, 0, 6, 3])],
    [Tile("I", [7, 3, 5, 1]), Tile("J", [3, 5, 5, 1]), Tile("K", [0, 2, 7, 1]), Tile("L", [0, 6, 5, 2])],
    [Tile("M", [5, 4, 7, 5]), Tile("N", [5, 1, 4, 0]), Tile("O", [6, 7, 4, 2]), Tile("P", [6, 6, 6, 3])]
]

cached_rotations = {}

def solve(currentRow, boardAbove, remaining_tiles, row_length):
    solutions = []

    for tile in remaining_tiles:
        for rotated_tile in get_rotations(tile):

            if valid_tile(rotated_tile, currentRow, boardAbove):
                new_remaining_tiles = remaining_tiles[:]
                new_remaining_tiles.remove(tile)

                new_row = currentRow + [rotated_tile]

                if len(new_row) >= row_length:
                    if new_remaining_tiles == []:
                        new_solution = [boardAbove + [new_row]]
                        solutions += new_solution

                    deep_result = solve([], boardAbove + [new_row], new_remaining_tiles, row_length)
                    solutions += deep_result

                else:
                    deep_result = solve(new_row, boardAbove, new_remaining_tiles, row_length)
                    solutions += deep_result

    return solutions


def valid_tile(tile, currentRow, boardAbove):
    if boardAbove:
        return valid_vert(boardAbove[-1][len(currentRow)], tile) and (currentRow == [] or valid_horz(currentRow[-1], tile))

    else:
        return currentRow == [] or valid_horz(currentRow[-1], tile)


def valid_horz(tileA, tileB):
     return tileA.values[1] == tileB.values[3]



def valid_vert(tileA, tileB):
    return tileA.values[2] == tileB.values[0]


def get_rotations(tile):
    if tile in cached_rotations:
        return cached_rotations[tile]

    rotations = []

    for i in range(4):
        rotated_tile = Tile(tile.name, tile.values[i:] + tile.values[:i])
        rotations.append(rotated_tile)

    cached_rotations[tile] = rotations

    return rotations


def flatten_board(board):
    return [item for sublist in board for item in sublist]


def print_solutions(solutions, print_full):
    print("Solutions:")

    for board in solutions:
        print_board(board)
        print("-")


def print_board(board):
    for row in board:
        print(" ".join(["⌜ {} ⌝".format(tile.values[0]) for tile in row]))
        print(" ".join(["{} {} {}".format(tile.values[3], tile.name, tile.values[1]) for tile in row]))
        print(" ".join(["⌞ {} ⌟".format(tile.values[2]) for tile in row]))


def run():
    solutions = solve([], [], flatten_board(board), 4)
    print_solutions(solutions, False)


time = timeit.timeit(run, number = 1)
print("Took {}s".format(round(time, 3)))
