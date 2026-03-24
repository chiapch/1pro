from world.grid import WorldGrid


def apply_tree_zone_tags(world: WorldGrid, tree_x: int, tree_y: int) -> None:
    for y in range(tree_y - 2, tree_y + 3):
        for x in range(tree_x - 2, tree_x + 3):
            cell = world.get_cell(x, y)
            if cell is None:
                continue

            dx = x - tree_x
            dy = y - tree_y
            dist2 = dx * dx + dy * dy

            if x == tree_x and y == tree_y:
                continue

            cell.add_hidden_tag("zone.tree")
            cell.add_hidden_tag("zone.roots")

            if abs(dx) <= 1 and abs(dy) <= 1:
                cell.add_hidden_tag("zone.trunk_near")
                cell.add_visible_tag("cover.branches")

            if dist2 <= 4:
                cell.add_hidden_tag("zone.crown")
                cell.add_visible_tag("cover.leaves")
