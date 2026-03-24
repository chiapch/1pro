from objects.tree.tree_root import TreeRoot


def recalculate_tree_water_needs(tree) -> None:
    tree.maintenance_water_need_per_tick = round(
        0.004 + tree.height * 0.0008 + tree.trunk_thickness * 0.0012,
        5,
    )
    tree.growth_water_need_per_tick = round(
        0.002 + tree.height * 0.0007 + tree.trunk_thickness * 0.0010,
        5,
    )
    tree.water_buffer_capacity = round(
        0.25 + tree.height * 0.03 + tree.trunk_thickness * 0.08,
        4,
    )


def collect_water_from_roots(tree, world, dt: float) -> float:
    total = 0.0

    for root_x, root_y in tree.root_positions:
        cell = world.get_cell(root_x, root_y)
        if cell is None:
            continue

        for obj in cell.ground_layer.get_objects():
            if isinstance(obj, TreeRoot) and obj.parent_tree_id == tree.id:
                total += obj.absorb_water(cell.ground_layer, dt)

    return total


def process_tree_water(tree, dt: float, world) -> None:
    recalculate_tree_water_needs(tree)

    incoming = collect_water_from_roots(tree, world, dt)
    tree.last_water_income = round(incoming, 5)
    tree.water_buffer = min(tree.water_buffer_capacity, tree.water_buffer + incoming)