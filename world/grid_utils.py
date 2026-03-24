import random


def get_neighbor_cells(world, x: int, y: int):
    result = []
    for ny in range(y - 1, y + 2):
        for nx in range(x - 1, x + 2):
            if nx == x and ny == y:
                continue
            cell = world.get_cell(nx, ny)
            if cell is not None:
                result.append((nx, ny, cell))
    return result


def pick_random_nearby_cell(world, cell_x: int, cell_y: int, radius: int):
    variants = []

    for y in range(cell_y - radius, cell_y + radius + 1):
        for x in range(cell_x - radius, cell_x + radius + 1):
            if x == cell_x and y == cell_y:
                continue

            cell = world.get_cell(x, y)
            if cell is not None:
                variants.append(cell)

    if not variants:
        return None
    return random.choice(variants)
