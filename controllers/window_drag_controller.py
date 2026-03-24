import pygame


class WindowDragController:
    def __init__(self, ui_manager) -> None:
        self.ui_manager = ui_manager

        self.is_dragging = False
        self.active_panel_key: str | None = None

        self.start_mouse_x = 0
        self.start_mouse_y = 0
        self.start_rect = None

        self.handle_visible_width = 6
        self.handle_hit_width = 16

    def begin_drag(self, mouse_pos: tuple[int, int]) -> bool:
        mx, my = mouse_pos

        for key, rect in reversed(self.ui_manager.get_draggable_panel_items()):
            if self._is_in_drag_handle(rect, mx, my):
                self.is_dragging = True
                self.active_panel_key = key
                self.start_mouse_x = mx
                self.start_mouse_y = my
                self.start_rect = rect.copy()
                return True

        return False

    def update_drag(self, mouse_pos: tuple[int, int]) -> bool:
        if not self.is_dragging or self.active_panel_key is None or self.start_rect is None:
            return False

        mx, my = mouse_pos
        dx = mx - self.start_mouse_x
        dy = my - self.start_mouse_y

        rect = self.ui_manager.get_panel_rect(self.active_panel_key)
        if rect is None:
            return False

        rect.x = self.start_rect.x + dx
        rect.y = self.start_rect.y + dy
        return True

    def end_drag(self) -> None:
        self.is_dragging = False
        self.active_panel_key = None
        self.start_rect = None

    def _is_in_drag_handle(self, rect: pygame.Rect, mx: int, my: int) -> bool:
        hit_rect = pygame.Rect(
            rect.x,
            rect.y,
            self.handle_hit_width,
            rect.height,
        )
        return hit_rect.collidepoint(mx, my)