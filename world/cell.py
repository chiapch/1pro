from dataclasses import dataclass, field
from typing import Any

from world.layers.ground_layer import GroundLayer
from world.layers.surface_layer import SurfaceLayer
from world.layers.standing_layer import StandingLayer
from world.layers.air_layer import AirLayer


@dataclass
class Cell:
    x: int
    y: int

    visible_tags: list[str] = field(default_factory=list)
    hidden_tags: list[str] = field(default_factory=list)
    hidden_data: dict[str, Any] = field(default_factory=dict)

    ground_layer: GroundLayer = field(default_factory=GroundLayer)
    surface_layer: SurfaceLayer = field(default_factory=SurfaceLayer)
    standing_layer: StandingLayer = field(default_factory=StandingLayer)
    air_layer: AirLayer = field(default_factory=AirLayer)

    def add_visible_tag(self, tag_id: str) -> None:
        if tag_id not in self.visible_tags:
            self.visible_tags.append(tag_id)

    def add_hidden_tag(self, tag_id: str) -> None:
        if tag_id not in self.hidden_tags:
            self.hidden_tags.append(tag_id)

    def has_visible_tag(self, tag_id: str) -> bool:
        return tag_id in self.visible_tags

    def has_hidden_tag(self, tag_id: str) -> bool:
        return tag_id in self.hidden_tags

    def set_hidden_data(self, key: str, value: Any) -> None:
        self.hidden_data[key] = value

    def get_hidden_data(self, key: str, default=None):
        return self.hidden_data.get(key, default)

    def get_layer(self, layer_name: str):
        if layer_name == "ground":
            return self.ground_layer
        if layer_name == "surface":
            return self.surface_layer
        if layer_name == "standing":
            return self.standing_layer
        if layer_name == "air":
            return self.air_layer
        raise ValueError(f"Неизвестный слой: {layer_name}")

    def get_layers_in_order(self) -> list:
        return [
            self.ground_layer,
            self.surface_layer,
            self.standing_layer,
            self.air_layer,
        ]

    def add_object_to_layer(self, layer_name: str, obj: Any) -> None:
        self.get_layer(layer_name).add_object(obj)

    def remove_object_from_layer(self, layer_name: str, obj: Any) -> None:
        self.get_layer(layer_name).remove_object(obj)

    def get_all_objects(self) -> list[Any]:
        result: list[Any] = []
        for layer in self.get_layers_in_order():
            result.extend(layer.get_objects())
        return result

    def open_visible_window(self) -> list[str]:
        return self.visible_tags

    def open_hidden_window(self) -> list[str]:
        lines = list(self.hidden_tags)

        for key, value in self.hidden_data.items():
            lines.append(f"{key}: {value}")

        return lines