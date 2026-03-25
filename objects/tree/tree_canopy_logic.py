import random

from objects.fallen_branch import FallenBranch
from objects.fallen_foliage import FallenFoliage
from objects.tree.id_generator import (
    next_fallen_branch_id,
    next_fallen_foliage_id,
)
from world.grid_utils import pick_random_nearby_cell


def clamp_chance(value: float) -> float:
    return max(0.0, min(1.0, value))


def get_branch_drop_chance(tree) -> float:
    return clamp_chance(
        tree.branch_drop_base_chance + sum(tree.branch_drop_modifiers.values())
    )


def get_branch_regrow_chance(tree) -> float:
    return clamp_chance(
        tree.branch_regrow_base_chance + sum(tree.branch_regrow_modifiers.values())
    )


def get_leaf_drop_chance(tree) -> float:
    return clamp_chance(
        tree.leaf_drop_base_chance + sum(tree.leaf_drop_modifiers.values())
    )


def get_leaf_regrow_chance(tree) -> float:
    return clamp_chance(
        tree.leaf_regrow_base_chance + sum(tree.leaf_regrow_modifiers.values())
    )


def process_tree_canopy(tree, dt: float, world, cell_x: int, cell_y: int) -> None:
    tree._branch_drop_progress += dt
    tree._branch_regrow_progress += dt
    tree._leaf_drop_progress += dt
    tree._leaf_regrow_progress += dt

    _consume_progress_limited(
        tree,
        "_branch_drop_progress",
        tree.branch_drop_check_interval,
        tree.max_canopy_checks_per_update,
        lambda: try_branch_drop(tree, world, cell_x, cell_y),
    )
    _consume_progress_limited(
        tree,
        "_branch_regrow_progress",
        tree.branch_regrow_check_interval,
        tree.max_canopy_checks_per_update,
        lambda: try_branch_regrow(tree),
    )
    _consume_progress_limited(
        tree,
        "_leaf_drop_progress",
        tree.leaf_drop_check_interval,
        tree.max_canopy_checks_per_update,
        lambda: try_leaf_drop(tree, world, cell_x, cell_y),
    )
    _consume_progress_limited(
        tree,
        "_leaf_regrow_progress",
        tree.leaf_regrow_check_interval,
        tree.max_canopy_checks_per_update,
        lambda: try_leaf_regrow(tree),
    )


def _consume_progress_limited(tree, progress_attr: str, interval: float, max_checks: int, callback) -> None:
    checks_done = 0
    progress = getattr(tree, progress_attr)
    while progress >= interval and checks_done < max_checks:
        progress -= interval
        callback()
        checks_done += 1

    setattr(tree, progress_attr, min(progress, interval))


def try_branch_drop(tree, world, cell_x: int, cell_y: int) -> bool:
    if tree.branch_count <= 0:
        tree.last_canopy_event = "branch_drop_blocked_no_branches"
        return False

    chance = get_branch_drop_chance(tree)
    roll = random.random()
    tree.last_branch_drop_roll = round(roll, 5)

    if roll > chance:
        tree.last_canopy_event = f"branch_drop_failed_roll={round(roll, 5)} chance={round(chance, 5)}"
        return False

    target_cell = pick_random_nearby_cell(world, cell_x, cell_y, radius=2)
    if target_cell is None:
        tree.last_canopy_event = "branch_drop_failed_no_target_cell"
        return False

    tree.branch_count -= 1

    fallen_branch = FallenBranch(
        id=next_fallen_branch_id(),
        origin_object_id=tree.id,
        rot_speed=round(random.uniform(0.003, 0.02), 4),
        rot_amount=0.0,
    )
    target_cell.add_object_to_layer("surface", fallen_branch)
    target_cell.add_hidden_tag("ground.fallen_branch")

    tree.dropped_branches_total += 1
    tree.last_canopy_event = f"branch_drop_success_to=({target_cell.x},{target_cell.y})"
    return True


def try_leaf_drop(tree, world, cell_x: int, cell_y: int) -> bool:
    if tree.leaf_count <= 0:
        tree.last_canopy_event = "leaf_drop_blocked_no_leaves"
        return False

    chance = get_leaf_drop_chance(tree)
    roll = random.random()
    tree.last_leaf_drop_roll = round(roll, 5)

    if roll > chance:
        tree.last_canopy_event = f"leaf_drop_failed_roll={round(roll, 5)} chance={round(chance, 5)}"
        return False

    target_cell = pick_random_nearby_cell(world, cell_x, cell_y, radius=2)
    if target_cell is None:
        tree.last_canopy_event = "leaf_drop_failed_no_target_cell"
        return False

    tree.leaf_count -= 1

    fallen_foliage = FallenFoliage(
        id=next_fallen_foliage_id(),
        origin_object_id=tree.id,
        rot_speed=round(random.uniform(0.005, 0.03), 4),
        rot_amount=0.0,
    )
    target_cell.add_object_to_layer("surface", fallen_foliage)
    target_cell.add_hidden_tag("ground.fallen_leaves")

    tree.dropped_leaves_total += 1
    tree.last_canopy_event = f"leaf_drop_success_to=({target_cell.x},{target_cell.y})"
    return True


def try_branch_regrow(tree) -> bool:
    if tree.branch_count >= tree.max_branch_count:
        return False

    if random.random() > get_branch_regrow_chance(tree):
        return False

    tree.branch_count += 1
    return True


def try_leaf_regrow(tree) -> bool:
    if tree.leaf_count >= tree.max_leaf_count:
        return False

    if random.random() > get_leaf_regrow_chance(tree):
        return False

    tree.leaf_count += 1
    return True
