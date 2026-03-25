from objects.tree.tree import Tree
from objects.tree.tree_root import TreeRoot
from objects.tree.tree_sprout import TreeSprout
from objects.tree.id_generator import next_tree_id


def find_support_root_for_sprout(sprout: TreeSprout, world):
    cell = world.get_cell(sprout.cell_x, sprout.cell_y)
    if cell is None:
        return None

    if sprout.origin_root_id is not None:
        for obj in cell.ground_layer.get_objects():
            if isinstance(obj, TreeRoot) and obj.id == sprout.origin_root_id:
                return obj

    for obj in cell.ground_layer.get_objects():
        if not isinstance(obj, TreeRoot):
            continue

        if obj.parent_tree_id == sprout.parent_tree_id:
            return obj

        if sprout.root_network_id is not None and obj.root_network_id == sprout.root_network_id:
            return obj

    return None


def process_tree_sprout_growth(sprout: TreeSprout, dt: float, world) -> None:
    if not sprout.alive:
        return

    sprout.age += dt

    incoming = 0.0
    if hasattr(world, "pull_network_water"):
        network_key = sprout.root_network_id or sprout.parent_tree_id
        requested = (sprout.support_need_per_tick + sprout.growth_need_per_tick) * dt
        incoming = world.pull_network_water(network_key, requested)
    else:
        root = find_support_root_for_sprout(sprout, world)
        if root is not None:
            incoming = root.last_transferred * 0.7

    sprout.last_support_income = round(incoming, 5)

    support_need = sprout.support_need_per_tick * dt
    growth_need = sprout.growth_need_per_tick * dt

    sprout.last_support_paid = 0.0
    sprout.last_growth_paid = 0.0

    if incoming >= support_need:
        sprout.last_support_paid = round(support_need, 5)

        if sprout.health < 1.0:
            sprout.health += 0.01 * dt
            if sprout.health > 1.0:
                sprout.health = 1.0

        available_for_growth = incoming - support_need
        if growth_need > 0 and available_for_growth > 0:
            growth_ratio = min(1.0, available_for_growth / growth_need)
            sprout.last_growth_paid = round(min(growth_need, available_for_growth), 5)
            sprout.growth_progress += 0.12 * dt * growth_ratio
    else:
        deficit_ratio = 1.0
        if support_need > 0:
            deficit_ratio = max(0.0, 1.0 - incoming / support_need)

        sprout.last_support_paid = round(incoming, 5)
        sprout.health -= 0.03 * dt * deficit_ratio
        if sprout.health < 0.0:
            sprout.health = 0.0

        if sprout.health <= 0.0:
            sprout.alive = False
            parent_tree = find_parent_tree(sprout, world)
            if parent_tree is not None:
                parent_tree.active_sprout_count = max(0, parent_tree.active_sprout_count - 1)
            cell = world.get_cell(sprout.cell_x, sprout.cell_y)
            if cell is not None:
                cell.remove_object_from_layer("standing", sprout)
            return

    if sprout.growth_progress >= 1.0:
        convert_sprout_to_tree(sprout, world)


def convert_sprout_to_tree(sprout: TreeSprout, world) -> None:
    cell = world.get_cell(sprout.cell_x, sprout.cell_y)
    if cell is None:
        return

    new_tree = Tree(
        id=next_tree_id(),
        age=1,
        trunk_thickness=0.12,
        height=1.2,
        branch_count=1,
        max_branch_count=1,
        leaf_count=6,
        max_leaf_count=6,
        branch_drop_check_interval=12.0,
        branch_drop_base_chance=0.04,
        branch_regrow_check_interval=18.0,
        branch_regrow_base_chance=0.12,
        leaf_drop_check_interval=2.0,
        leaf_drop_base_chance=0.12,
        leaf_regrow_check_interval=3.0,
        leaf_regrow_base_chance=0.18,
        species_id=sprout.species_id,
        root_network_id=sprout.root_network_id,
    )

    support_root = find_support_root_for_sprout(sprout, world)
    if support_root is not None:
        new_tree.support_roots.append(support_root)
    new_tree.water_buffer = 0.15

    new_tree.has_active_sprout = False

    parent_tree = find_parent_tree(sprout, world)
    if parent_tree is not None:
        parent_tree.active_sprout_count = max(0, parent_tree.active_sprout_count - 1)

    cell.remove_object_from_layer("standing", sprout)
    cell.add_object_to_layer("standing", new_tree)


def find_parent_tree(sprout: TreeSprout, world):
    for row in world.cells:
        for cell in row:
            for obj in cell.standing_layer.get_objects():
                if isinstance(obj, Tree) and obj.id == sprout.parent_tree_id:
                    return obj
    return None
