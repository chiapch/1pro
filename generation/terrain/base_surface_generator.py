from world.grid import WorldGrid
from tags.appliers.base_surface_applier import apply_base_surface_tags


def generate_base_surface(world: WorldGrid) -> None:
    apply_base_surface_tags(world)
