import pygame


class WindowResizeController:
    def __init__(self, ui_manager) -> None:
        self.ui_manager = ui_manager

        self.is_resizing = False
        self.active_panel_key: str | None = None
        self.resize_mode: str | None = None

        self.start_mouse_x = 0
        self.start_mouse_y = 0
        self.start_rect = None

        self.edge_size = 10
        self.corner_size = 16

        self.min_width = 220
        self.min_height = 140

    def begin_resize(self, mouse_pos: tuple[int, int]) -> bool:
        mx, my = mouse_pos

        for key, rect in reversed(self.ui_manager.get_resizable_panel_items()):
            hit_mode = self._detect_hit(rect, mx, my)
            if hit_mode is not None:
                self.is_resizing = True
                self.active_panel_key = key
                self.resize_mode = hit_mode
                self.start_mouse_x = mx
                self.start_mouse_y = my
                self.start_rect = rect.copy()
                return True

        return False

    def update_resize(self, mouse_pos: tuple[int, int]) -> bool:
        if not self.is_resizing or self.active_panel_key is None or self.start_rect is None:
            return False

        mx, my = mouse_pos
        dx = mx - self.start_mouse_x
        dy = my - self.start_mouse_y

        rect = self.ui_manager.get_panel_rect(self.active_panel_key)
        if rect is None:
            return False

        new_width = self.start_rect.width
        new_height = self.start_rect.height

        if self.resize_mode in ("right", "corner"):
            new_width = max(self.min_width, self.start_rect.width + dx)

        if self.resize_mode in ("bottom", "corner"):
            new_height = max(self.min_height, self.start_rect.height + dy)

        rect.width = new_width
        rect.height = new_height
        return True

    def end_resize(self) -> None:
        self.is_resizing = False
        self.active_panel_key = None
        self.resize_mode = None
        self.start_rect = None

    def _detect_hit(self, rect: pygame.Rect, mx: int, my: int) -> str | None:
        if not rect.collidepoint(mx, my):
            return None

        near_right = abs(mx - rect.right) <= self.edge_size
        near_bottom = abs(my - rect.bottom) <= self.edge_size
        in_corner = (
            rect.right - self.corner_size <= mx <= rect.right
            and rect.bottom - self.corner_size <= my <= rect.bottom
        )

        if in_corner:
            return "corner"
        if near_right:
            return "right"
        if near_bottom:
            return "bottom"
        return None