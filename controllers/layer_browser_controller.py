from ui.object_grouping import group_objects


class LayerBrowserController:
    def __init__(self) -> None:
        self.mode = "closed"

        self.selected_cell = None
        self.layers = []
        self.layer_index = 0

        self.current_layer = None
        self.group_index = 0
        self.object_index = 0
        self.scroll_offset = 0

        self.current_groups = []
        self.current_group = None
        self.current_object = None

    def open_for_cell(self, hovered_cell) -> None:
        if hovered_cell is None:
            return

        self.selected_cell = hovered_cell
        self.layers = hovered_cell.get_layers_in_order()
        self.layer_index = 0
        self.group_index = 0
        self.object_index = 0
        self.scroll_offset = 0
        self.current_layer = None
        self.current_groups = []
        self.current_group = None
        self.current_object = None
        self.mode = "layers_list"

    def close(self) -> None:
        self.mode = "closed"
        self.selected_cell = None
        self.layers = []
        self.layer_index = 0
        self.group_index = 0
        self.object_index = 0
        self.scroll_offset = 0
        self.current_layer = None
        self.current_groups = []
        self.current_group = None
        self.current_object = None

    def move_up(self) -> None:
        if self.mode == "layers_list" and self.layers:
            self.layer_index = max(0, self.layer_index - 1)
        elif self.mode == "layer_groups" and self.current_groups:
            self.group_index = max(0, self.group_index - 1)
        elif self.mode == "group_objects" and self.current_group is not None:
            self.object_index = max(0, self.object_index - 1)

    def move_down(self) -> None:
        if self.mode == "layers_list" and self.layers:
            self.layer_index = min(len(self.layers) - 1, self.layer_index + 1)
        elif self.mode == "layer_groups" and self.current_groups:
            self.group_index = min(len(self.current_groups) - 1, self.group_index + 1)
        elif self.mode == "group_objects" and self.current_group is not None:
            objects = self.current_group["objects"]
            self.object_index = min(len(objects) - 1, self.object_index + 1)

    def select_current(self) -> None:
        if self.mode == "layers_list":
            if not self.layers:
                return

            self.current_layer = self.layers[self.layer_index]
            self.current_groups = group_objects(self.current_layer.get_objects())
            self.group_index = 0
            self.scroll_offset = 0
            self.mode = "layer_groups"
            return

        if self.mode == "layer_groups":
            if not self.current_groups:
                return

            self.current_group = self.current_groups[self.group_index]
            self.object_index = 0
            self.scroll_offset = 0
            self.mode = "group_objects"
            return

        if self.mode == "group_objects":
            if self.current_group is None:
                return

            objects = self.current_group["objects"]
            if not objects:
                return

            self.current_object = objects[self.object_index]
            self.scroll_offset = 0
            self.mode = "object_detail"

    def go_back(self) -> None:
        if self.mode == "object_detail":
            self.current_object = None
            self.scroll_offset = 0
            self.mode = "group_objects"
            return

        if self.mode == "group_objects":
            self.current_group = None
            self.object_index = 0
            self.scroll_offset = 0
            self.mode = "layer_groups"
            return

        if self.mode == "layer_groups":
            self.current_layer = None
            self.current_groups = []
            self.group_index = 0
            self.scroll_offset = 0
            self.mode = "layers_list"
            return

        if self.mode == "layers_list":
            self.close()

    def scroll_up(self) -> None:
        self.scroll_offset = max(0, self.scroll_offset - 1)

    def scroll_down(self, max_scroll: int) -> None:
        self.scroll_offset = min(max_scroll, self.scroll_offset + 1)

    def get_title(self) -> str:
        if self.mode == "layers_list":
            return "Слои клетки"
        if self.mode == "layer_groups":
            return "Слой и группы объектов"
        if self.mode == "group_objects":
            return "Объекты группы слоя"
        if self.mode == "object_detail":
            return "Подробности объекта"
        return "Слои"

    def get_lines(self) -> list[dict]:
        if self.mode == "closed":
            return []

        if self.mode == "layers_list":
            return self._build_layers_lines()

        if self.mode == "layer_groups":
            return self._build_layer_groups_lines()

        if self.mode == "group_objects":
            return self._build_group_objects_lines()

        if self.mode == "object_detail":
            return self._build_object_detail_lines()

        return []

    def _build_layers_lines(self) -> list[dict]:
        if not self.layers:
            return [{"text": "слои отсутствуют", "enabled": False, "selected": False}]

        lines = []
        for i, layer in enumerate(self.layers):
            extra = ""

            if layer.layer_name == "ground":
                extra = f" | obj={layer.object_count()} | влажн={round(layer.moisture, 3)}"
            else:
                extra = f" | obj={layer.object_count()}"

            lines.append({
                "text": f"{layer.display_name}{extra}",
                "enabled": True,
                "selected": i == self.layer_index,
            })

        return lines

    def _build_layer_groups_lines(self) -> list[dict]:
        if self.current_layer is None:
            return [{"text": "слой не выбран", "enabled": False, "selected": False}]

        lines: list[dict] = []

        for line in self.current_layer.build_summary_lines():
            lines.append({"text": line, "enabled": False, "selected": False})

        lines.append({"text": "", "enabled": False, "selected": False})

        if not self.current_groups:
            lines.append({"text": "группы объектов отсутствуют", "enabled": False, "selected": False})
            return lines

        lines.append({"text": "группы:", "enabled": False, "selected": False})

        for i, group in enumerate(self.current_groups):
            lines.append({
                "text": f"{group['display_name']} - {group['count']} шт.",
                "enabled": True,
                "selected": i == self.group_index,
            })

        return lines

    def _build_group_objects_lines(self) -> list[dict]:
        if self.current_group is None:
            return [{"text": "группа не выбрана", "enabled": False, "selected": False}]

        objects = self.current_group["objects"]
        if not objects:
            return [{"text": "объекты отсутствуют", "enabled": False, "selected": False}]

        lines = [
            {"text": f"группа: {self.current_group['display_name']}", "enabled": False, "selected": False},
            {"text": f"количество: {self.current_group['count']}", "enabled": False, "selected": False},
            {"text": "", "enabled": False, "selected": False},
        ]

        for i, obj in enumerate(objects):
            lines.append({
                "text": f"{obj.display_name} | id={obj.id}",
                "enabled": True,
                "selected": i == self.object_index,
            })

        return lines

    def _build_object_detail_lines(self) -> list[dict]:
        if self.current_object is None:
            return [{"text": "объект не выбран", "enabled": False, "selected": False}]

        from ui.object_formatters import format_object_info
        return [{"text": line, "enabled": True, "selected": False} for line in format_object_info(self.current_object)]