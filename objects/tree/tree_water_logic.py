from objects.tree.tree_root import TreeRoot


def recalculate_tree_water_needs(tree) -> None:
    signature = (round(tree.height, 4), round(tree.trunk_thickness, 4))
    if tree._water_needs_signature == signature:
        return
    tree._water_needs_signature = signature

    tree.maintenance_water_need_per_tick = round(
        0.002 + tree.height * 0.00045 + tree.trunk_thickness * 0.0007,
        5,
    )
    tree.growth_water_need_per_tick = round(
        0.001 + tree.height * 0.0004 + tree.trunk_thickness * 0.0006,
        5,
    )
    tree.water_buffer_capacity = round(
        0.25 + tree.height * 0.03 + tree.trunk_thickness * 0.08,
        4,
    )


def collect_water_from_roots(tree, world, dt: float) -> float:
    total = 0.0

    if len(tree.root_objects) != len(tree.root_positions):
        tree.root_objects = _rebuild_root_cache(tree, world)

    all_roots = list(tree.root_objects)
    for root in tree.support_roots:
        if any(existing.id == root.id for existing in all_roots):
            continue
        all_roots.append(root)

    for root in all_roots:
        cell = world.get_cell(root.cell_x, root.cell_y)
        if cell is None:
            continue
        total += root.absorb_water(cell.ground_layer, dt)

    return total


def _rebuild_root_cache(tree, world) -> list[TreeRoot]:
    roots: list[TreeRoot] = []
    for root_x, root_y in tree.root_positions:
        cell = world.get_cell(root_x, root_y)
        if cell is None:
            continue
        for obj in cell.ground_layer.get_objects():
            if isinstance(obj, TreeRoot) and obj.parent_tree_id == tree.id:
                roots.append(obj)
                break
    return roots


def process_tree_water(tree, dt: float, world) -> None:
    recalculate_tree_water_needs(tree)

    if hasattr(world, "pull_network_water"):
        network_key = tree.root_network_id or tree.id
        demand = (tree.maintenance_water_need_per_tick + tree.growth_water_need_per_tick) * dt
        reserve_target = demand * 1.5
        requested = max(0.0, reserve_target - tree.water_buffer)
        incoming = world.pull_network_water(network_key, requested)
    else:
        incoming = collect_water_from_roots(tree, world, dt)

    tree.last_water_income = round(incoming, 5)
    tree.water_buffer = min(tree.water_buffer_capacity, tree.water_buffer + incoming)
