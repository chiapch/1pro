from world.grid import WorldGrid
from generation.terrain.base_surface_generator import generate_base_surface
from generation.terrain.moisture_map_generator import generate_static_moisture_map
from generation.objects.tree_generator import generate_one_tree
from generation.zones.tree_zone_generator import generate_tree_zone


def generate_world(world: WorldGrid) -> None:
    generate_base_surface(world)
    generate_static_moisture_map(world)

    tree_data = generate_one_tree(world, 50, 50)
    if tree_data is None:
        return

    generate_tree_zone(world, tree_data["x"], tree_data["y"])
