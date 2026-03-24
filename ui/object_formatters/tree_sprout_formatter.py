from objects.tree.tree_sprout import TreeSprout


def format_tree_sprout_info(sprout: TreeSprout) -> list[str]:
    return [
        "объект: росток",
        f"id: {sprout.id}",
        f"родительское дерево: {sprout.parent_tree_id}",
        f"исходный корень: {sprout.origin_root_id}",
        f"сеть корней: {sprout.root_network_id}",
        f"тип: {sprout.species_id}",
        f"позиция: ({sprout.cell_x}, {sprout.cell_y})",
        f"возраст: {round(sprout.age, 3)}",
        f"здоровье: {round(sprout.health, 4)}",
        f"прогресс роста: {round(sprout.growth_progress, 4)}",
        f"живой: {sprout.alive}",
        f"вход поддержки: {sprout.last_support_income}",
        f"нужно на поддержку/тик: {sprout.support_need_per_tick}",
        f"нужно на рост/тик: {sprout.growth_need_per_tick}",
        f"оплачено поддержки: {sprout.last_support_paid}",
        f"оплачено роста: {sprout.last_growth_paid}",
        f"слой: {sprout.layer}",
    ]