import pygame

from config import (
    WORLD_WIDTH,
    WORLD_HEIGHT,
    BASE_CELL_SIZE,
    MIN_CELL_SIZE,
    MAX_CELL_SIZE,
    ZOOM_STEP,
)


class Camera:
    def __init__(self, viewport_rect: pygame.Rect) -> None:
        self.viewport_rect = viewport_rect
        self.world_width = WORLD_WIDTH
        self.world_height = WORLD_HEIGHT
        self.cell_size = BASE_CELL_SIZE
        self.offset_x = 0
        self.offset_y = 0
        self.clamp_offset()

    def get_world_pixel_size(self) -> tuple[int, int]:
        return (
            self.world_width * self.cell_size,
            self.world_height * self.cell_size,
        )

    def clamp_offset(self) -> None:
        world_px_w, world_px_h = self.get_world_pixel_size()

        if world_px_w <= self.viewport_rect.width:
            self.offset_x = (self.viewport_rect.width - world_px_w) // 2
        else:
            min_x = self.viewport_rect.width - world_px_w
            max_x = 0
            self.offset_x = max(min_x, min(self.offset_x, max_x))

        if world_px_h <= self.viewport_rect.height:
            self.offset_y = (self.viewport_rect.height - world_px_h) // 2
        else:
            min_y = self.viewport_rect.height - world_px_h
            max_y = 0
            self.offset_y = max(min_y, min(self.offset_y, max_y))

    def _zoom_keep_center(self, new_cell_size: int) -> None:
        old_cell_size = self.cell_size
        center_screen_x = self.viewport_rect.width / 2
        center_screen_y = self.viewport_rect.height / 2

        world_x = (center_screen_x - self.offset_x) / old_cell_size
        world_y = (center_screen_y - self.offset_y) / old_cell_size

        self.cell_size = new_cell_size
        self.offset_x = int(center_screen_x - world_x * self.cell_size)
        self.offset_y = int(center_screen_y - world_y * self.cell_size)
        self.clamp_offset()

    def zoom_in(self) -> None:
        new_size = min(MAX_CELL_SIZE, self.cell_size + ZOOM_STEP)
        if new_size != self.cell_size:
            self._zoom_keep_center(new_size)

    def zoom_out(self) -> None:
        new_size = max(MIN_CELL_SIZE, self.cell_size - ZOOM_STEP)
        if new_size != self.cell_size:
            self._zoom_keep_center(new_size)

    def move(self, dx: int, dy: int) -> None:
        self.offset_x += dx
        self.offset_y += dy
        self.clamp_offset()

    def screen_to_cell_coords(self, screen_x: int, screen_y: int) -> tuple[int, int] | None:
        if not self.viewport_rect.collidepoint(screen_x, screen_y):
            return None

        local_x = screen_x - self.viewport_rect.x
        local_y = screen_y - self.viewport_rect.y
        world_px_x = local_x - self.offset_x
        world_px_y = local_y - self.offset_y

        if world_px_x < 0 or world_px_y < 0:
            return None

        cell_x = int(world_px_x // self.cell_size)
        cell_y = int(world_px_y // self.cell_size)

        if not (0 <= cell_x < self.world_width and 0 <= cell_y < self.world_height):
            return None

        return cell_x, cell_y

    def get_cell_rect(self, x: int, y: int) -> pygame.Rect:
        screen_x = self.viewport_rect.x + self.offset_x + x * self.cell_size
        screen_y = self.viewport_rect.y + self.offset_y + y * self.cell_size
        return pygame.Rect(screen_x, screen_y, self.cell_size, self.cell_size)

    def get_visible_cell_bounds(self) -> tuple[int, int, int, int]:
        left = (-self.offset_x) // self.cell_size
        top = (-self.offset_y) // self.cell_size
        right = (self.viewport_rect.width - self.offset_x - 1) // self.cell_size
        bottom = (self.viewport_rect.height - self.offset_y - 1) // self.cell_size

        x_start = max(0, int(left))
        y_start = max(0, int(top))
        x_end = min(self.world_width - 1, int(right))
        y_end = min(self.world_height - 1, int(bottom))
        return x_start, x_end, y_start, y_end
