from tags.tag import Tag


TAG_REGISTRY: dict[str, Tag] = {}


def register_tag(tag: Tag) -> None:
    TAG_REGISTRY[tag.tag_id] = tag


def get_tag(tag_id: str) -> Tag | None:
    return TAG_REGISTRY.get(tag_id)


def get_tag_name(tag_id: str) -> str:
    tag = get_tag(tag_id)
    if tag is None:
        return tag_id
    return tag.name
