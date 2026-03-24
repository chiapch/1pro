from objects.tree.tree import Tree
from objects.tree.tree_root import TreeRoot
from objects.tree.tree_sprout import TreeSprout
from objects.fallen_branch import FallenBranch
from objects.fallen_foliage import FallenFoliage

from ui.object_formatters.tree_formatter import format_tree_info
from ui.object_formatters.tree_root_formatter import format_tree_root_info
from ui.object_formatters.tree_sprout_formatter import format_tree_sprout_info
from ui.object_formatters.fallen_branch_formatter import format_fallen_branch_info
from ui.object_formatters.fallen_foliage_formatter import format_fallen_foliage_info


def format_object_info(world_object) -> list[str]:
    if world_object is None:
        return ["объект отсутствует"]

    if isinstance(world_object, Tree):
        return format_tree_info(world_object)

    if isinstance(world_object, TreeRoot):
        return format_tree_root_info(world_object)

    if isinstance(world_object, TreeSprout):
        return format_tree_sprout_info(world_object)

    if isinstance(world_object, FallenBranch):
        return format_fallen_branch_info(world_object)

    if isinstance(world_object, FallenFoliage):
        return format_fallen_foliage_info(world_object)

    return [
        f"неизвестный объект: {type(world_object).__name__}",
        f"id: {getattr(world_object, 'id', '-')}",
    ]