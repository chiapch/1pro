from tags.tag import Tag
from tags.registry import register_tag


HIDDEN_TAGS = [
    Tag("object.tree.full", "полноценное дерево", "object_state", False),
    Tag("zone.tree", "зона дерева", "tree_zone", False),
    Tag("zone.trunk_near", "рядом со стволом", "tree_zone", False),
    Tag("zone.crown", "крона дерева", "tree_zone", False),
    Tag("zone.roots", "влияние корней", "tree_zone", False),
]


def register_hidden_tags() -> None:
    for tag in HIDDEN_TAGS:
        register_tag(tag)
