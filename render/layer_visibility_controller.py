class LayerVisibilityController:
    def __init__(self) -> None:
        self.settings = {
            "ground": {"visible": True, "alpha": 1.0, "display_name": "грунт"},
            "surface": {"visible": True, "alpha": 1.0, "display_name": "поверхность"},
            "standing": {"visible": True, "alpha": 1.0, "display_name": "standing"},
            "air": {"visible": True, "alpha": 1.0, "display_name": "воздух"},
        }
        self.alpha_steps = [0.0, 0.1, 0.2, 0.35, 0.5, 0.7, 0.85, 1.0]

    def is_visible(self, layer_name: str) -> bool:
        return self.settings[layer_name]["visible"]

    def get_alpha(self, layer_name: str) -> float:
        return self.settings[layer_name]["alpha"]

    def toggle_visible(self, layer_name: str) -> None:
        self.settings[layer_name]["visible"] = not self.settings[layer_name]["visible"]

    def increase_alpha(self, layer_name: str) -> None:
        current = self.settings[layer_name]["alpha"]
        idx = self._closest_alpha_index(current)
        if idx < len(self.alpha_steps) - 1:
            self.settings[layer_name]["alpha"] = self.alpha_steps[idx + 1]

    def decrease_alpha(self, layer_name: str) -> None:
        current = self.settings[layer_name]["alpha"]
        idx = self._closest_alpha_index(current)
        if idx > 0:
            self.settings[layer_name]["alpha"] = self.alpha_steps[idx - 1]

    def _closest_alpha_index(self, value: float) -> int:
        best_index = 0
        best_diff = abs(self.alpha_steps[0] - value)

        for i, alpha in enumerate(self.alpha_steps):
            diff = abs(alpha - value)
            if diff < best_diff:
                best_diff = diff
                best_index = i

        return best_index