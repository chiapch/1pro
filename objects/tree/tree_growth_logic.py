def process_tree_growth(tree, dt: float) -> None:
    tree.age += dt * 0.2

    maintenance_need = tree.maintenance_water_need_per_tick * dt
    growth_need = tree.growth_water_need_per_tick * dt

    tree.last_maintenance_paid = 0.0
    tree.last_growth_paid = 0.0

    if tree.water_buffer >= maintenance_need:
        tree.water_buffer -= maintenance_need
        tree.last_maintenance_paid = round(maintenance_need, 5)

        if tree.health < 1.0:
            tree.health += 0.01 * dt
            if tree.health > 1.0:
                tree.health = 1.0
    else:
        paid = tree.water_buffer
        tree.water_buffer = 0.0
        tree.last_maintenance_paid = round(paid, 5)

        deficit_ratio = 1.0
        if maintenance_need > 0:
            deficit_ratio = max(0.0, 1.0 - paid / maintenance_need)

        tree.health -= 0.03 * dt * deficit_ratio
        if tree.health < 0.0:
            tree.health = 0.0

        if tree.health <= 0.0:
            tree.alive = False
        return

    if tree.water_buffer >= growth_need:
        tree.water_buffer -= growth_need
        tree.last_growth_paid = round(growth_need, 5)
        tree.growth_progress += 0.10 * dt

        while tree.growth_progress >= 1.0:
            tree.growth_progress -= 1.0
            apply_tree_growth_step(tree)


def apply_tree_growth_step(tree) -> None:
    tree.height = round(tree.height + 0.12, 3)
    tree.trunk_thickness = round(tree.trunk_thickness + 0.015, 3)

    tree.max_leaf_count += 1
    if tree.leaf_count < tree.max_leaf_count:
        tree.leaf_count += 1

    if tree.max_branch_count < int(tree.height * 0.9) + 1:
        tree.max_branch_count += 1
        if tree.branch_count < tree.max_branch_count:
            tree.branch_count += 1
