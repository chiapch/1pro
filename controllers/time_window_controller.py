class TimeWindowController:
    def __init__(self, time_controller) -> None:
        self.time_controller = time_controller
        self.is_open = False
        self.scroll_offset = 0

        self.items = [
            {"id": "pause", "label": "состояние", "enabled": True},
            {"id": "speed", "label": "скорость", "enabled": True},
            {"id": "direction", "label": "направление", "enabled": False},
            {"id": "step_forward", "label": "шаг вперед", "enabled": False},
            {"id": "step_backward", "label": "шаг назад", "enabled": False},
            {"id": "stream", "label": "поток времени", "enabled": False},
            {"id": "jump", "label": "прыжок во времени", "enabled": False},
        ]

        self.selected_index = 0
        self._clamp_to_enabled()

    def toggle_open(self) -> None:
        self.is_open = not self.is_open
        if self.is_open:
            self._clamp_to_enabled()
            self.scroll_offset = 0

    def close(self) -> None:
        self.is_open = False
        self.scroll_offset = 0

    def move_up(self) -> None:
        if not self.is_open:
            return

        i = self.selected_index - 1
        while i >= 0:
            if self.items[i]["enabled"]:
                self.selected_index = i
                return
            i -= 1

    def move_down(self) -> None:
        if not self.is_open:
            return

        i = self.selected_index + 1
        while i < len(self.items):
            if self.items[i]["enabled"]:
                self.selected_index = i
                return
            i += 1

    def apply_left(self) -> None:
        if not self.is_open:
            return

        current_id = self.items[self.selected_index]["id"]

        if current_id == "pause":
            self.time_controller.toggle_pause()
        elif current_id == "speed":
            self.time_controller.decrease_speed()

    def apply_right(self) -> None:
        if not self.is_open:
            return

        current_id = self.items[self.selected_index]["id"]

        if current_id == "pause":
            self.time_controller.toggle_pause()
        elif current_id == "speed":
            self.time_controller.increase_speed()

    def activate(self) -> None:
        if not self.is_open:
            return

        current_id = self.items[self.selected_index]["id"]

        if current_id == "pause":
            self.time_controller.toggle_pause()

    def scroll_up(self) -> None:
        self.scroll_offset = max(0, self.scroll_offset - 1)

    def scroll_down(self, max_scroll: int) -> None:
        self.scroll_offset = min(max_scroll, self.scroll_offset + 1)

    def get_lines(self) -> list[dict]:
        state = self.time_controller.get_state()
        result: list[dict] = []

        for index, item in enumerate(self.items):
            selected = index == self.selected_index and item["enabled"]

            value = self._get_item_value(item["id"], state)
            result.append({
                "text": f"{item['label']}: {value}",
                "enabled": item["enabled"],
                "selected": selected,
            })

        result.append({"text": "", "enabled": False, "selected": False})
        result.append({
            "text": f"real time: {round(state.total_real_time, 2)}",
            "enabled": False,
            "selected": False,
        })
        result.append({
            "text": f"simulation time: {round(state.total_simulation_time, 2)}",
            "enabled": False,
            "selected": False,
        })

        return result

    def _get_item_value(self, item_id: str, state) -> str:
        if item_id == "pause":
            return "PAUSE" if state.is_paused else "RUN"
        if item_id == "speed":
            return f"x{state.current_speed()}"
        if item_id == "direction":
            return "FORWARD"
        if item_id == "step_forward":
            return "недоступно"
        if item_id == "step_backward":
            return "недоступно"
        if item_id == "stream":
            return self.time_controller.get_stream_name()
        if item_id == "jump":
            return "недоступно"
        return "-"

    def _clamp_to_enabled(self) -> None:
        for i, item in enumerate(self.items):
            if item["enabled"]:
                self.selected_index = i
                return