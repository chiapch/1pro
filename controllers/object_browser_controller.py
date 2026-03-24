from ui.object_grouping import group_objects


class ObjectBrowserController:
    def __init__(self) -> None:
        self.mode = "closed"
        self.selected_cell = None

        self.group_index = 0
        self.object_index = 0
        self.scroll_offset = 0

        self.current_groups: list[dict] = []
        self.current_group: dict | None = None
        self.current_object = None

    def open_for_cell(self, hovered_cell) -> None:
        if hovered_cell is None:
            return

        self.selected_cell = hovered_cell
        self.current_groups = group_objects(hovered_cell.get_all_objects())
        self.current_group = None
        self.current_object = None
        self.group_index = 0
        self.object_index = 0
        self.scroll_offset = 0
        self.mode = "cell_object_groups"

    def close(self) -> None:
        self.mode = "closed"
        self.selected_cell = None
        self.current_groups = []
        self.current_group = None
        self.current_object = None
        self.group_index = 0
        self.object_index = 0
        self.scroll_offset = 0

    def move_up(self) -> None:
        if self.mode == "cell_object_groups" and self.current_groups:
            self.group_index = max(0, self.group_index - 1)
        elif self.mode == "group_objects_list" and self.current_group is not None:
            self.object_index = max(0, self.object_index - 1)

    def move_down(self) -> None:
        if self.mode == "cell_object_groups" and self.current_groups:
            self.group_index = min(len(self.current_groups) - 1, self.group_index + 1)
        elif self.mode == "group_objects_list" and self.current_group is not None:
            objects = self.current_group["objects"]
            self.object_index = min(len(objects) - 1, self.object_index + 1)

    def select_current(self) -> None:
        if self.mode == "cell_object_groups":
            if not self.current_groups:
                return

            self.current_group = self.current_groups[self.group_index]
            self.object_index = 0
            self.scroll_offset = 0
            self.mode = "group_objects_list"
            return

        if self.mode == "group_objects_list":
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
            self.mode = "group_objects_list"
            return

        if self.mode == "group_objects_list":
            self.current_group = None
            self.object_index = 0
            self.scroll_offset = 0
            self.mode = "cell_object_groups"
            return

        if self.mode == "cell_object_groups":
            self.close()

    def scroll_up(self) -> None:
        self.scroll_offset = max(0, self.scroll_offset - 1)

    def scroll_down(self, max_scroll: int) -> None:
        self.scroll_offset = min(max_scroll, self.scroll_offset + 1)

    def get_lines(self) -> list[dict]:
        if self.mode == "closed":
            return []

        if self.mode == "cell_object_groups":
            return self._build_group_lines()

        if self.mode == "group_objects_list":
            return self._build_object_lines()

        if self.mode == "object_detail":
            return self._build_detail_lines()

        return []

    def get_title(self) -> str:
        if self.mode == "cell_object_groups":
            return "Группы объектов клетки"
        if self.mode == "group_objects_list":
            return "Объекты группы"
        if self.mode == "object_detail":
            return "Подробности объекта"
        return "Объекты"

    def _build_group_lines(self) -> list[dict]:
        if not self.current_groups:
            return [{"text": "объекты отсутствуют", "enabled": False, "selected": False}]

        lines: list[dict] = []
        for i, group in enumerate(self.current_groups):
            lines.append({
                "text": f"{group['display_name']} - {group['count']} шт.",
                "enabled": True,
                "selected": i == self.group_index,
            })
        return lines

    def _build_object_lines(self) -> list[dict]:
        if self.current_group is None:
            return [{"text": "группа не выбрана", "enabled": False, "selected": False}]

        objects = self.current_group["objects"]
        if not objects:
            return [{"text": "объекты отсутствуют", "enabled": False, "selected": False}]

        lines: list[dict] = []
        for i, obj in enumerate(objects):
            lines.append({
                "text": f"{obj.display_name} | id={obj.id}",
                "enabled": True,
                "selected": i == self.object_index,
            })
        return lines

    def _build_detail_lines(self) -> list[dict]:
        if self.current_object is None:
            return [{"text": "объект не выбран", "enabled": False, "selected": False}]

        from ui.object_formatters import format_object_info
        return [{"text": line, "enabled": True, "selected": False} for line in format_object_info(self.current_object)]