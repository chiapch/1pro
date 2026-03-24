from world.grid import WorldGrid
from tags import register_all_tags
from generation import generate_world


def main() -> None:
    register_all_tags()
    world = WorldGrid()
    generate_world(world)

    for y in range(world.height):
        row = []
        for x in range(world.width):
            cell = world.get_cell(x, y)
            row.append("T" if cell.get_all_objects() else ".")
        print("".join(row))


if __name__ == "__main__":
    main()
