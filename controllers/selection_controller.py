class SelectionController:
    def __init__(self) -> None:
        self.selected_cell = None
        self.show_tag_windows = False

    def handle_open_tags(self, hovered_cell) -> None:
        if hovered_cell is None:
            return
        self.selected_cell = hovered_cell
        self.show_tag_windows = True

    def close_tags(self) -> None:
        self.selected_cell = None
        self.show_tag_windows = False
