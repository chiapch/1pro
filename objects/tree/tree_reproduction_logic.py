import random

from objects.tree.tree_root import TreeRoot
from objects.tree.tree_sprout import TreeSprout
from objects.tree.id_generator import next_tree_sprout_id


def process_tree_reproduction(tree, dt: float, world) -> None:
    tree._sprout_growth_progress += dt

    while tree._sprout_growth_progress >= tree.sprout_check_interval:
        tree._sprout_growth_progress -= tree.sprout_check_interval
        try_spawn_sprout_from_roots(tree, world)


def try_spawn_sprout_from_roots(tree, world) -> bool:
    if count_active_sprouts(tree, world) >= tree.max_active_sprouts:
        return False

    if tree.health < 0.8:
        return False

    if tree.last_growth_paid <= 0.0:
        return False

    if random.random() > tree.sprout_spawn_chance:
        return False

    candidate_roots = get_tip_roots_for_sprout(tree, world)
    random.shuffle(candidate_roots)

    for root in candidate_roots:
        cell = world.get_cell(root.cell_x, root.cell_y)
        if cell is None:
            continue

        if has_blocking_standing_object(cell):
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
        return True

    return False


def count_active_sprouts(tree, world) -> int:
    count = 0
    for row in world.cells:
        for cell in row:
            for obj in cell.standing_layer.get_objects():
                if isinstance(obj, TreeSprout) and obj.parent_tree_id == tree.id and obj.alive:
                    count += 1
    return count


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
