from world.layers.base_layer import BaseLayer


class GroundLayer(BaseLayer):
    def __init__(self) -> None:
        super().__init__(layer_name="ground", display_name="грунт")
        self.moisture: float = 0.35
        self.max_moisture: float = 1.0
        self.moisture_regen_per_second: float = 0.003

        self.composition: dict[str, float] = {
            "земля": 0.7,
            "камушки": 0.2,
            "дерн": 0.1,
        }

    def set_moisture(self, value: float) -> None:
        self.moisture = max(0.0, min(self.max_moisture, value))

    def set_composition_part(self, part_name: str, value: float) -> None:
        self.composition[part_name] = max(0.0, value)

    def normalize_composition(self) -> None:
        total = sum(self.composition.values())
        if total <= 0:
            return

        for key in list(self.composition.keys()):
            self.composition[key] = round(self.composition[key] / total, 3)

    def update(self, dt: float) -> None:
        self.set_moisture(self.moisture + self.moisture_regen_per_second * dt)

    def build_summary_lines(self) -> list[str]:
        lines = [
            f"слой: {self.display_name}",
            f"объектов: {self.object_count()}",
            f"влажность: {round(self.moisture, 3)}",
            f"макс. влажность: {round(self.max_moisture, 3)}",
            f"восст. влаги/сек: {round(self.moisture_regen_per_second, 4)}",
            "состав:",
        ]

        for key, value in self.composition.items():
            lines.append(f"  {key}: {value}")

        for key, value in self.data.items():
            lines.append(f"{key}: {value}")

        return lines