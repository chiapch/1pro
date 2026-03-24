from world.grid import WorldGrid
from generation.objects.tree_factory import create_tree
from objects.tree.tree_root import TreeRoot
from objects.tree.id_generator import next_tree_root_id, next_root_network_id


def add_root(
    world: WorldGrid,
    tree,
    network_id: str,
    x: int,
    y: int,
    parent_root_id: str | None,
    depth: int,
    branch_order: int,
    is_tip: bool,
    growth_direction: tuple[int, int] | None,
) -> str:
    root_id = next_tree_root_id()

    root = TreeRoot(
        id=root_id,
        parent_tree_id=tree.id,
        cell_x=x,
        cell_y=y,
        parent_root_id=parent_root_id,
        strength=1.0,
        uptake_capacity_per_tick=0.03,
        self_need_per_tick=0.005,
        depth=depth,
        branch_order=branch_order,
        is_tip=is_tip,
        growth_direction=growth_direction,
        root_network_id=network_id,
    )

    cell = world.get_cell(x, y)
    if cell is not None:
        cell.add_object_to_layer("ground", root)
    tree.register_root(root)
    return root_id


def generate_one_tree(world: WorldGrid, x: int, y: int):
    cell = world.get_cell(x, y)
    if cell is None:
        return None

    network_id = next_root_network_id()

    tree = create_tree()
    tree.root_network_id = network_id
    cell.add_object_to_layer("standing", tree)

    trunk_root_id = add_root(
        world=world,
        tree=tree,
        network_id=network_id,
        x=x,
        y=y,
        parent_root_id=None,
        depth=0,
        branch_order=0,
        is_tip=False,
        growth_direction=None,
    )

    directions = [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1),
    ]
    for dx, dy in directions:
        nx = x + dx
        ny = y + dy
        neighbor = world.get_cell(nx, ny)
        if neighbor is None:
            continue

        add_root(
            world=world,
            tree=tree,
            network_id=network_id,
            x=nx,
            y=ny,
            parent_root_id=trunk_root_id,
            depth=1,
            branch_order=0,
            is_tip=True,
            growth_direction=(dx, dy),
        )

    cell.add_visible_tag("object.tree")
    cell.add_hidden_tag("object.tree.full")
    cell.add_hidden_tag("object.tree.rooted")

    return {
        "x": x,
        "y": y,
        "tree": tree,
    }
