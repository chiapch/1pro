from objects.tree.tree import Tree


def format_object_info(world_object) -> list[str]:
    if world_object is None:
        return ["объект отсутствует"]

    if isinstance(world_object, Tree):
        return format_tree_info(world_object)

    return [f"неизвестный объект: {type(world_object).__name__}"]


def format_tree_info(tree: Tree) -> list[str]:
    foliage = tree.foliage

    leaf_count = 0
    fall_interval = "-"
    regrow_interval = "-"

    if foliage is not None:
        leaf_count = foliage.leaf_count
        fall_interval = f"{foliage.fall_interval}"
        regrow_interval = f"{foliage.regrow_interval}"

    return [
        "объект: дерево",
        f"возраст: {tree.age}",
        f"толщина ствола: {tree.trunk_thickness}",
        f"высота: {tree.height}",
        f"веток сейчас: {tree.branch_count()} / {tree.max_branch_count()}",
        f"листьев: {leaf_count}",
        f"падение листьев: {fall_interval}",
        f"рост листьев: {regrow_interval}",
        f"падение веток: {tree.branch_fall_interval}",
        f"рост веток: {tree.branch_regrow_interval}",
    ]