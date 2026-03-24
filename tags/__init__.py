from tags.visible_tags import register_visible_tags
from tags.hidden_tags import register_hidden_tags


def register_all_tags() -> None:
    register_visible_tags()
    register_hidden_tags()
