from objects.tree.tree import Tree
from objects.tree.tree_root import TreeRoot
from objects.tree.tree_sprout import TreeSprout
from objects.tree.id_generator import next_tree_id, next_tree_root_id


def find_support_root_for_sprout(sprout: TreeSprout, world):
    cell = world.get_cell(sprout.cell_x, sprout.cell_y)
    if cell is None:
        return None

    for obj in cell.ground_layer.get_objects():
        if isinstance(obj, TreeRoot) and obj.parent_tree_id == sprout.parent_tree_id:
            return obj

    return None


def process_tree_sprout_growth(sprout: TreeSprout, dt: float, world) -> None:
    if not sprout.alive:
        return

    sprout.age += dt

    root = find_support_root_for_sprout(sprout, world)
    incoming = 0.0
    if root is not None:
        incoming = root.last_transferred * 0.5

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
        if available_for_growth >= growth_need:
            sprout.last_growth_paid = round(growth_need, 5)
            sprout.growth_progress += 0.12 * dt
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

    new_tree.root_positions.append((sprout.cell_x, sprout.cell_y))
    new_tree.water_buffer = 0.15

    new_root = TreeRoot(
        id=next_tree_root_id(),
        parent_tree_id=new_tree.id,
        cell_x=sprout.cell_x,
        cell_y=sprout.cell_y,
        parent_root_id=sprout.origin_root_id,
        strength=1.0,
        uptake_capacity_per_tick=0.03,
        self_need_per_tick=0.005,
        depth=0,
        branch_order=0,
        is_tip=True,
        growth_direction=(0, 1),
        root_network_id=sprout.root_network_id,
    )

    new_tree.has_active_sprout = False

    cell.remove_object_from_layer("standing", sprout)
    cell.add_object_to_layer("standing", new_tree)
    cell.add_object_to_layer("ground", new_root)