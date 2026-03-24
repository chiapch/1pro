from typing import Any


class BaseLayer:
    def __init__(self, layer_name: str, display_name: str) -> None:
        self.layer_name = layer_name
        self.display_name = display_name
        self.objects: list[Any] = []
        self.data: dict[str, Any] = {}

    def add_object(self, obj: Any) -> None:
        self.objects.append(obj)

    def remove_object(self, obj: Any) -> None:
        if obj in self.objects:
            self.objects.remove(obj)

    def get_objects(self) -> list[Any]:
        return self.objects

    def set_data(self, key: str, value: Any) -> None:
        self.data[key] = value

    def get_data(self, key: str, default=None):
        return self.data.get(key, default)

    def object_count(self) -> int:
        return len(self.objects)

    def build_summary_lines(self) -> list[str]:
        lines = [
            f"слой: {self.display_name}",
            f"объектов: {self.object_count()}",
        ]

        for key, value in self.data.items():
            lines.append(f"{key}: {value}")

        return lines