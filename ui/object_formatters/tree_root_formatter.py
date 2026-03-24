from objects.tree.tree_root import TreeRoot


def format_tree_root_info(root: TreeRoot) -> list[str]:
    return [
        "объект: корень",
        f"id: {root.id}",
        f"родительское дерево: {root.parent_tree_id}",
        f"родительский корень: {root.parent_root_id}",
        f"позиция: ({root.cell_x}, {root.cell_y})",
        f"глубина: {root.depth}",
        f"порядок ветвления: {root.branch_order}",
        f"кончик роста: {root.is_tip}",
        f"направление: {root.growth_direction}",
        f"сила: {root.strength}",
        f"макс. забор/тик: {root.uptake_capacity_per_tick}",
        f"минимум себе/тик: {root.self_need_per_tick}",
        f"влага до забора: {root.last_cell_moisture_before}",
        f"забрано: {root.last_absorbed}",
        f"оставлено себе: {root.last_kept}",
        f"передано дереву: {root.last_transferred}",
        f"влага после забора: {root.last_cell_moisture_after}",
        f"слой: {root.layer}",
    ]