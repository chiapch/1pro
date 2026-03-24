from world.grid import WorldGrid


def apply_base_surface_tags(world: WorldGrid) -> None:
    for row in world.cells:
        for cell in row:
            cell.add_visible_tag("base.earth")
            cell.add_visible_tag("cover.turf")
            cell.add_visible_tag("cover.grass")
