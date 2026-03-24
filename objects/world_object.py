from dataclasses import dataclass


@dataclass
class WorldObject:
    id: str
    object_type: str
    display_name: str
    stackable: bool
    layer: str = "ground"
    origin_object_id: str | None = None