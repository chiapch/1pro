import random

from objects.tree.id_generator import next_tree_id
from objects.tree.tree import Tree


def clamp(value: float, min_value: float, max_value: float) -> float:
    return max(min_value, min(value, max_value))


def create_tree(age: int | None = None) -> Tree:
    if age is None:
        age = random.randint(6, 28)

    tree_id = next_tree_id()

    trunk_thickness = clamp(age * 0.04 + random.uniform(-0.15, 0.15), 0.12, 4.50)
    height = clamp(age * 0.35 + random.uniform(-1.0, 1.0), 1.5, 35.0)

    max_branch_count = max(1, int(age * 0.35 + random.randint(-2, 3)))
    max_leaf_count = max(10, int(height * 18 + max_branch_count * 4))

    return Tree(
        id=tree_id,
        age=age,
        trunk_thickness=round(trunk_thickness, 2),
        height=round(height, 2),
        branch_count=max_branch_count,
        max_branch_count=max_branch_count,
        leaf_count=max_leaf_count,
        max_leaf_count=max_leaf_count,
        branch_drop_check_interval=round(random.uniform(8.0, 18.0), 2),
        branch_drop_base_chance=round(random.uniform(0.02, 0.08), 3),
        branch_regrow_check_interval=round(random.uniform(15.0, 30.0), 2),
        branch_regrow_base_chance=round(random.uniform(0.10, 0.25), 3),
        leaf_drop_check_interval=round(random.uniform(1.0, 3.0), 2),
        leaf_drop_base_chance=round(random.uniform(0.08, 0.25), 3),
        leaf_regrow_check_interval=round(random.uniform(2.0, 5.0), 2),
        leaf_regrow_base_chance=round(random.uniform(0.12, 0.30), 3),
        species_id="default_tree",
    )
