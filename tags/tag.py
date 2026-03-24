from dataclasses import dataclass


@dataclass(frozen=True)
class Tag:
    tag_id: str
    name: str
    category: str
    visible_by_default: bool
