from world.grid import WorldGrid
from tags.appliers.tree_zone_applier import apply_tree_zone_tags


def generate_tree_zone(world: WorldGrid, tree_x: int, tree_y: int) -> None:
    apply_tree_zone_tags(world, tree_x, tree_y)
