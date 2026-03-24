from tags.tag import Tag
from tags.registry import register_tag


VISIBLE_TAGS = [
    Tag("base.earth", "земля", "base_surface", True),
    Tag("cover.turf", "дерн", "surface_cover", True),
    Tag("cover.grass", "трава", "surface_cover", True),
    Tag("object.tree", "дерево", "object", True),
    Tag("cover.branches", "ветки", "tree_cover", True),
    Tag("cover.leaves", "листва", "tree_cover", True),
]


def register_visible_tags() -> None:
    for tag in VISIBLE_TAGS:
        register_tag(tag)
