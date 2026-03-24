from itertools import count


_tree_id_counter = count(1)
_tree_root_id_counter = count(1)
_tree_sprout_id_counter = count(1)
_root_network_id_counter = count(1)
_fallen_branch_id_counter = count(1)
_fallen_foliage_id_counter = count(1)


def next_tree_id() -> str:
    return f"tree_{next(_tree_id_counter)}"


def next_tree_root_id() -> str:
    return f"tree_root_{next(_tree_root_id_counter)}"


def next_tree_sprout_id() -> str:
    return f"tree_sprout_{next(_tree_sprout_id_counter)}"


def next_root_network_id() -> str:
    return f"root_network_{next(_root_network_id_counter)}"


def next_fallen_branch_id() -> str:
    return f"fallen_branch_{next(_fallen_branch_id_counter)}"


def next_fallen_foliage_id() -> str:
    return f"fallen_foliage_{next(_fallen_foliage_id_counter)}"