# Written by Cameron Palmer

import timeit

# A tile is a container for a name and values for each side
class Tile():

    def __init__(self, name, values):
        self.name = name
        self.values = values

    def __repr__(self):
        return self.name + "(" + str(self.values)[1:-1] + ")"


# The board is represented as a 2D array of tiles
board = [
    [Tile("A", [1, 6, 1, 4]), Tile("B", [2, 4, 7, 5]), Tile("C", [7, 1, 1, 4]), Tile("D", [1, 7, 0, 2])],
    [Tile("E", [0, 0, 1, 5]), Tile("F", [0, 5, 4, 2]), Tile("G", [4, 2, 4, 4]), Tile("H", [1, 0, 6, 3])],
    [Tile("I", [7, 3, 5, 1]), Tile("J", [3, 5, 5, 1]), Tile("K", [0, 2, 7, 1]), Tile("L", [0, 6, 5, 2])],
    [Tile("M", [5, 4, 7, 5]), Tile("N", [5, 1, 4, 0]), Tile("O", [6, 7, 4, 2]), Tile("P", [6, 6, 6, 3])]
]

# The rotations of each tile are cached in a dictionary to avoid recalculating them
cached_rotations = {}


# Solves the given board and returns a list of solution board states
def solve_board(board):
    return solve([], [], flatten_board(board), len(board[0]))


# Recursive solve function - takes the current state of a board (the current row and the completed rows above it), and
# a list of unused tiles, and tries placing each rotation of each remaining tile in the next spot. For any placements
# that are valid (the tile sides match up), the function calls itself to advance that possible solution. When a board
# is filled with valid placements, its added to the list of solutions and returns
def solve(current_row, board_above, remaining_tiles, row_length):
    solutions = []

    # Iterate through all possible tiles that could be placed next
    for tile in remaining_tiles:
        for rotated_tile in get_rotations(tile):

            # If the placement is valid
            if valid_tile(rotated_tile, current_row, board_above):
                # Remove the tile from the remaining tiles list
                new_remaining_tiles = remaining_tiles[:]
                new_remaining_tiles.remove(tile)

                # Add it to the current row
                new_row = current_row + [rotated_tile]

                # If the row is full
                if len(new_row) >= row_length:
                    # If all tiles have been used
                    if new_remaining_tiles == []:
                        # Add the current state as a solution
                        new_solution = [board_above + [new_row]]
                        solutions += new_solution

                    # Recurse with the new state of the board on a new row
                    deep_solutions = solve([], board_above + [new_row], new_remaining_tiles, row_length)
                    solutions += deep_solutions

                else:
                    # Recurse with the new state of the board on the current row
                    deep_solutions = solve(new_row, board_above, new_remaining_tiles, row_length)
                    solutions += deep_solutions

    return solutions


# Returns true if a tile is valid as the next placement in the row
def valid_tile(tile, current_row, board_above):
    # If the tile has a tile above it, it must match sides with both the tile above and the tile to the left (unless its
    # the first tile in the row)
    if board_above:
        return valid_vert(board_above[-1][len(current_row)], tile) and (current_row == [] or valid_horz(current_row[-1], tile))

    # If a tile is in the first row its valid if its the first tile or if it matches the tile to the left
    else:
        return current_row == [] or valid_horz(current_row[-1], tile)


# Returns true if a tile matches horizontally with another
def valid_horz(tile_a, tile_b):
     return tile_a.values[1] == tile_b.values[3]


# Returns true if a tile matches vertically with another
def valid_vert(tile_a, tile_b):
    return tile_a.values[2] == tile_b.values[0]


# Returns a list of all rotations of a tile
def get_rotations(tile):
    # If the rotations have already been calculated for this tile, then return those
    if tile in cached_rotations:
        return cached_rotations[tile]

    rotations = []

    for i in range(4):
        rotated_tile = Tile(tile.name, tile.values[i:] + tile.values[:i])
        rotations.append(rotated_tile)

    cached_rotations[tile] = rotations

    return rotations


# Turns a board into a flat list of tiles
def flatten_board(board):
    return [item for sublist in board for item in sublist]


# Prints out a list of solutions
def print_solutions(solutions):
    print("Solutions:")

    for board in solutions:
        print_board(board)
        print("-")


# Prints out a board
def print_board(board):
    for row in board:
        print(" ".join(["⌜ {} ⌝".format(tile.values[0]) for tile in row]))
        print(" ".join(["{} {} {}".format(tile.values[3], tile.name, tile.values[1]) for tile in row]))
        print(" ".join(["⌞ {} ⌟".format(tile.values[2]) for tile in row]))


def run():
    solutions = solve_board(board)
    print_solutions(solutions)


time = timeit.timeit(run, number = 1)
print("Took {}s".format(round(time, 3)))
