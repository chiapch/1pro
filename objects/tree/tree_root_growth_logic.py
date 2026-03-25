import random

from objects.tree.tree_root import TreeRoot
from objects.tree.id_generator import next_tree_root_id
from world.grid_utils import get_neighbor_cells


CARDINAL_DIRECTIONS = [
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1),
]


def get_tree_roots(tree, world) -> list[TreeRoot]:
    roots: list[TreeRoot] = []

    for root_x, root_y in tree.root_positions:
        cell = world.get_cell(root_x, root_y)
        if cell is None:
            continue

        for obj in cell.ground_layer.get_objects():
            if isinstance(obj, TreeRoot) and obj.parent_tree_id == tree.id:
                roots.append(obj)

    return roots


def get_tip_roots(tree, world) -> list[TreeRoot]:
    return [root for root in get_tree_roots(tree, world) if root.is_tip]


def has_own_root_in_cell(tree, cell) -> bool:
    for obj in cell.ground_layer.get_objects():
        if isinstance(obj, TreeRoot) and obj.parent_tree_id == tree.id:
            return True
    return False


def process_tree_root_growth(tree, dt: float, world, cell_x: int, cell_y: int) -> None:
    tree._root_growth_progress += dt

    interval = get_effective_root_growth_interval(tree)
    cycles_done = 0
    while (
        tree._root_growth_progress >= interval
        and cycles_done < tree.max_root_growth_cycles_per_update
    ):
        tree._root_growth_progress -= interval
        process_root_growth_step(tree, world, cell_x, cell_y)
        cycles_done += 1

    tree._root_growth_progress = min(tree._root_growth_progress, interval)


def process_root_growth_step(tree, world, cell_x: int, cell_y: int) -> None:
    if len(tree.root_positions) >= tree.max_root_count:
        return

    enough_for_growth = tree.last_growth_paid > 0.0
    if not enough_for_growth:
        return

    tip_roots = get_tip_roots(tree, world)

    if not tip_roots:
        return

    random.shuffle(tip_roots)

    attempts_left = min(tree.max_root_growth_attempts_per_cycle, len(tip_roots))
    processed = 0

    for tip in tip_roots:
        if attempts_left <= 0:
            break

        if processed >= tree.max_new_roots_per_cycle:
            break

        attempts_left -= 1

        growth_chance = get_effective_root_growth_chance(tree)
        if random.random() > growth_chance:
            continue

        grew = grow_from_root_tip(tree, tip, world)
        if grew:
            processed += 1


def get_effective_root_growth_interval(tree) -> float:
    root_count = len(tree.root_positions)
    load_penalty = min(12.0, root_count * 0.04)
    return tree.root_growth_check_interval + load_penalty


def get_effective_root_growth_chance(tree) -> float:
    size_penalty = max(0.08, 1.0 - (len(tree.root_positions) / max(1, tree.max_root_count)))
    health_factor = 0.5 + max(0.0, min(1.0, tree.health)) * 0.5
    return max(0.02, tree.root_growth_base_chance * size_penalty * health_factor)


def grow_from_root_tip(tree, root: TreeRoot, world) -> bool:
    candidates = choose_growth_targets_for_root(tree, root, world)
    if not candidates:
        return False

    spawned_any = False

    main_target = weighted_choice(candidates)
    if main_target is None:
        return False

    spawn_child_root(
        tree=tree,
        parent_root=root,
        target=main_target,
        world=world,
        branch_order=root.branch_order,
    )
    spawned_any = True

    branch_chance = get_branching_chance(root)
    if random.random() < branch_chance:
        side_candidates = [item for item in candidates if item != main_target]
        if side_candidates:
            side_target = weighted_choice(side_candidates)
            if side_target is not None:
                spawn_child_root(
                    tree=tree,
                    parent_root=root,
                    target=side_target,
                    world=world,
                    branch_order=root.branch_order + 1,
                )

    if spawned_any:
        root.is_tip = False

    return spawned_any


def choose_growth_targets_for_root(tree, root: TreeRoot, world):
    candidates = []

    neighbors = get_neighbor_cells(world, root.cell_x, root.cell_y)

    for nx, ny, cell in neighbors:
        if has_own_root_in_cell(tree, cell):
            continue

        if cell.ground_layer.moisture < 0.08:
            continue

        direction = (nx - root.cell_x, ny - root.cell_y)
        if abs(direction[0]) + abs(direction[1]) != 1:
            continue

        weight = compute_directional_weight(root.growth_direction, direction)
        weight += cell.ground_layer.moisture * 5.0

        if weight <= 0:
            continue

        candidates.append({
            "x": nx,
            "y": ny,
            "cell": cell,
            "direction": direction,
            "weight": weight,
        })

    return candidates


def compute_directional_weight(current_direction, candidate_direction) -> float:
    if current_direction is None:
        return 2.0

    if candidate_direction == current_direction:
        return 5.0

    if candidate_direction == (-current_direction[0], -current_direction[1]):
        return 0.2

    return 2.5


def get_branching_chance(root: TreeRoot) -> float:
    base = 0.35
    depth_penalty = min(0.20, root.depth * 0.02)
    return max(0.05, base - depth_penalty)


def weighted_choice(candidates):
    if not candidates:
        return None

    total = sum(item["weight"] for item in candidates)
    if total <= 0:
        return None

    r = random.uniform(0, total)
    acc = 0.0

    for item in candidates:
        acc += item["weight"]
        if r <= acc:
            return item

    return candidates[-1]


def spawn_child_root(tree, parent_root: TreeRoot, target, world, branch_order: int) -> None:
    if len(tree.root_positions) >= tree.max_root_count:
        return

    nx = target["x"]
    ny = target["y"]
    cell = target["cell"]
    direction = target["direction"]

    new_root = TreeRoot(
        id=next_tree_root_id(),
        parent_tree_id=tree.id,
        cell_x=nx,
        cell_y=ny,
        parent_root_id=parent_root.id,
        strength=1.0,
        uptake_capacity_per_tick=0.03,
        self_need_per_tick=0.005,
        depth=parent_root.depth + 1,
        branch_order=branch_order,
        is_tip=True,
        growth_direction=direction,
        root_network_id=tree.root_network_id,
    )

    cell.add_object_to_layer("ground", new_root)
    tree.register_root(new_root)
