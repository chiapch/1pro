class LayerViewSettingsController:
    def __init__(self, visibility_controller) -> None:
        self.visibility_controller = visibility_controller
        self.is_open = False
        self.scroll_offset = 0
        self.layer_order = ["ground", "surface", "standing", "air"]
        self.selected_index = 0

    def toggle_open(self) -> None:
        self.is_open = not self.is_open
        if self.selected_index >= len(self.layer_order):
            self.selected_index = 0
        if self.is_open:
            self.scroll_offset = 0

    def close(self) -> None:
        self.is_open = False
        self.scroll_offset = 0

    def move_up(self) -> None:
        if not self.is_open:
            return
        self.selected_index = max(0, self.selected_index - 1)

    def move_down(self) -> None:
        if not self.is_open:
            return
        self.selected_index = min(len(self.layer_order) - 1, self.selected_index + 1)

    def toggle_current_visibility(self) -> None:
        if not self.is_open:
            return
        layer_name = self.layer_order[self.selected_index]
        self.visibility_controller.toggle_visible(layer_name)

    def increase_current_alpha(self) -> None:
        if not self.is_open:
            return
        layer_name = self.layer_order[self.selected_index]
        self.visibility_controller.increase_alpha(layer_name)

    def decrease_current_alpha(self) -> None:
        if not self.is_open:
            return
        layer_name = self.layer_order[self.selected_index]
        self.visibility_controller.decrease_alpha(layer_name)

    def scroll_up(self) -> None:
        self.scroll_offset = max(0, self.scroll_offset - 1)

    def scroll_down(self, max_scroll: int) -> None:
        self.scroll_offset = min(max_scroll, self.scroll_offset + 1)

    def get_lines(self) -> list[dict]:
        lines = []

        for i, layer_name in enumerate(self.layer_order):
            selected = i == self.selected_index
            settings = self.visibility_controller.settings[layer_name]

            visible_text = "ON" if settings["visible"] else "OFF"
            alpha_text = settings["alpha"]

            lines.append({
                "text": f"{settings['display_name']} | видимость: {visible_text} | alpha: {alpha_text}",
                "enabled": True,
                "selected": selected,
            })

        lines.append({"text": "", "enabled": False, "selected": False})
        lines.append({
            "text": "Enter - вкл/выкл слой",
            "enabled": False,
            "selected": False,
        })
        lines.append({
            "text": "Left/Right - менять прозрачность",
            "enabled": False,
            "selected": False,
        })

        return lines