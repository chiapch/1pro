import random

from objects.tree.tree_root import TreeRoot
from objects.tree.tree_sprout import TreeSprout
from objects.tree.id_generator import next_tree_sprout_id


def process_tree_reproduction(tree, dt: float, world) -> None:
    tree._sprout_growth_progress += dt

    checks_done = 0
    while (
        tree._sprout_growth_progress >= tree.sprout_check_interval
        and checks_done < tree.max_sprout_checks_per_update
    ):
        tree._sprout_growth_progress -= tree.sprout_check_interval
        try_spawn_sprout_from_roots(tree, world)
        checks_done += 1

    tree._sprout_growth_progress = min(
        tree._sprout_growth_progress,
        tree.sprout_check_interval,
    )


def try_spawn_sprout_from_roots(tree, world) -> bool:
    if tree.active_sprout_count >= tree.max_active_sprouts:
        return False

    if tree.age < tree.min_reproduction_age:
        return False

    water_ratio = 0.0
    if tree.water_buffer_capacity > 0:
        water_ratio = tree.water_buffer / tree.water_buffer_capacity
    demand = tree.maintenance_water_need_per_tick + tree.growth_water_need_per_tick
    has_network_supply = tree.last_water_income >= max(0.0001, demand * 0.6)
    if water_ratio < tree.min_reproduction_water_ratio and not has_network_supply:
        return False

    if tree.health < 0.8:
        return False

    if tree.last_growth_paid <= 0.0 and not has_network_supply:
        return False

    candidate_roots = get_tip_roots_for_sprout(tree, world)
    random.shuffle(candidate_roots)

    for root in candidate_roots:
        cell = world.get_cell(root.cell_x, root.cell_y)
        if cell is None:
            continue

        if has_blocking_standing_object(cell):
            continue

        nearby_trees = count_nearby_trees(world, root.cell_x, root.cell_y, radius=3)
        local_density_factor = max(0.0, 1.0 - (nearby_trees / 9.0))
        effective_spawn_chance = tree.sprout_spawn_chance * local_density_factor
        if effective_spawn_chance <= 0.0:
            continue

        if random.random() > effective_spawn_chance:
            continue

        sprout = TreeSprout(
            id=next_tree_sprout_id(),
            parent_tree_id=tree.id,
            origin_root_id=root.id,
            root_network_id=tree.root_network_id,
            species_id=tree.species_id,
            cell_x=root.cell_x,
            cell_y=root.cell_y,
        )
        cell.add_object_to_layer("standing", sprout)
        tree.active_sprout_count += 1
        return True

    return False


def get_tip_roots_for_sprout(tree, world):
    result = []

    for root_x, root_y in tree.root_positions:
        cell = world.get_cell(root_x, root_y)
        if cell is None:
            continue

        for obj in cell.ground_layer.get_objects():
            if isinstance(obj, TreeRoot) and obj.parent_tree_id == tree.id and obj.is_tip:
                result.append(obj)

    return result


def has_blocking_standing_object(cell) -> bool:
    for obj in cell.standing_layer.get_objects():
        if obj.object_type in ("tree", "tree_sprout"):
            return True
    return False


def count_nearby_trees(world, center_x: int, center_y: int, radius: int) -> int:
    count = 0
    for y in range(max(0, center_y - radius), min(world.height - 1, center_y + radius) + 1):
        for x in range(max(0, center_x - radius), min(world.width - 1, center_x + radius) + 1):
            cell = world.get_cell(x, y)
            if cell is None:
                continue
            for obj in cell.standing_layer.get_objects():
                if obj.object_type == "tree":
                    count += 1
    return count
