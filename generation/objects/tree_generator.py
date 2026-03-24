from world.grid import WorldGrid
from generation.objects.tree_factory import create_tree
from objects.tree.tree_root import TreeRoot
from objects.tree.id_generator import next_tree_root_id, next_root_network_id


def generate_one_tree(world: WorldGrid, x: int, y: int):
    cell = world.get_cell(x, y)
    if cell is None:
        return None

    network_id = next_root_network_id()

    tree = create_tree()
    tree.root_network_id = network_id
    tree.root_positions.append((x, y))
    cell.add_object_to_layer("standing", tree)

    root = TreeRoot(
        id=next_tree_root_id(),
        parent_tree_id=tree.id,
        cell_x=x,
        cell_y=y,
        parent_root_id=None,
        strength=1.0,
        uptake_capacity_per_tick=0.03,
        self_need_per_tick=0.005,
        depth=0,
        branch_order=0,
        is_tip=True,
        growth_direction=(0, 1),
        root_network_id=network_id,
    )
    cell.add_object_to_layer("ground", root)

    cell.add_visible_tag("object.tree")
    cell.add_hidden_tag("object.tree.full")
    cell.add_hidden_tag("object.tree.rooted")

    return {
        "x": x,
        "y": y,
        "tree": tree,
    }