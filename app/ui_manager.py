import pygame

from config import (
    PANEL_WIDTH,
    PANEL_HEIGHT,
    PANEL_GAP,
    PANEL_X,
    PANEL_Y,
    SCREEN_HEIGHT,
    TEXT_COLOR,
    SUBTEXT_COLOR,
)


class UIManager:
    def __init__(self, app) -> None:
        self.app = app

        self.panel_rects = {
            "visible_tags": pygame.Rect(
                PANEL_X,
                PANEL_Y,
                PANEL_WIDTH,
                PANEL_HEIGHT,
            ),
            "hidden_tags": pygame.Rect(
                PANEL_X,
                PANEL_Y + PANEL_HEIGHT + PANEL_GAP,
                PANEL_WIDTH,
                PANEL_HEIGHT,
            ),
            "object_panel": pygame.Rect(
                PANEL_X,
                PANEL_Y + (PANEL_HEIGHT + PANEL_GAP) * 2,
                PANEL_WIDTH + 200,
                PANEL_HEIGHT + 200,
            ),
            "time_panel": pygame.Rect(
                PANEL_X - 20,
                PANEL_Y + 20,
                PANEL_WIDTH + 140,
                PANEL_HEIGHT + 200,
            ),
            "layer_view_panel": pygame.Rect(
                PANEL_X - 20,
                PANEL_Y + 20,
                PANEL_WIDTH + 200,
                PANEL_HEIGHT + 140,
            ),
        }

    def get_panel_rect(self, key: str):
        return self.panel_rects.get(key)

    def get_resizable_panel_items(self):
        return [
            ("visible_tags", self.panel_rects["visible_tags"]),
            ("hidden_tags", self.panel_rects["hidden_tags"]),
            ("object_panel", self.panel_rects["object_panel"]),
            ("time_panel", self.panel_rects["time_panel"]),
            ("layer_view_panel", self.panel_rects["layer_view_panel"]),
        ]

    def get_draggable_panel_items(self):
        return [
            ("visible_tags", self.panel_rects["visible_tags"]),
            ("hidden_tags", self.panel_rects["hidden_tags"]),
            ("object_panel", self.panel_rects["object_panel"]),
            ("time_panel", self.panel_rects["time_panel"]),
            ("layer_view_panel", self.panel_rects["layer_view_panel"]),
        ]

    def draw_info(self) -> None:
        app = self.app
        title = app.font.render("Мир 100x100", True, TEXT_COLOR)
        app.screen.blit(title, (20, SCREEN_HEIGHT - 110))

        hint1 = app.small_font.render(
            "Q — теги | X — объекты | L — слои | T — время | V — видимость слоев | F3/F6 — perf | ESC — закрыть",
            True,
            SUBTEXT_COLOR,
        )
        app.screen.blit(hint1, (20, SCREEN_HEIGHT - 78))

        hint2 = app.small_font.render(
            "W/S — выбор | Enter — открыть/вкл-выкл | Left/Right — менять значение | колесо/PageUp/PageDown — прокрутка",
            True,
            SUBTEXT_COLOR,
        )
        app.screen.blit(hint2, (20, SCREEN_HEIGHT - 54))

        hint3 = app.small_font.render(
            "левая ручка — перетаскивать | правый/нижний край — менять размер | стрелки — сдвиг мира",
            True,
            SUBTEXT_COLOR,
        )
        app.screen.blit(hint3, (20, SCREEN_HEIGHT - 30))

        state = app.time_controller.get_state()
        zoom_txt = app.small_font.render(
            f"time: {'PAUSE' if state.is_paused else 'RUN'} | speed: x{state.current_speed()} | масштаб: {app.camera.cell_size}px",
            True,
            TEXT_COLOR,
        )
        app.screen.blit(zoom_txt, (720, SCREEN_HEIGHT - 30))

        perf_status = app.small_font.render(
            f"perf: {'ON' if app.perf_monitor.enabled else 'OFF'} (F3/F6)",
            True,
            TEXT_COLOR if app.perf_monitor.enabled else SUBTEXT_COLOR,
        )
        app.screen.blit(perf_status, (720, SCREEN_HEIGHT - 54))

        if app.state.hovered_cell is not None:
            hover_txt = app.small_font.render(
                f"hover: x={app.state.hovered_cell.x}, y={app.state.hovered_cell.y}, objects={len(app.state.hovered_cell.get_all_objects())}",
                True,
                TEXT_COLOR,
            )
            app.screen.blit(hover_txt, (1040, SCREEN_HEIGHT - 30))

        if app.perf_monitor.enabled:
            perf_title = app.small_font.render("perf top (ms):", True, TEXT_COLOR)
            app.screen.blit(perf_title, (20, 12))

            top_sections = app.perf_monitor.get_top_sections(top_n=5)
            if not top_sections:
                collecting = app.small_font.render("collecting...", True, SUBTEXT_COLOR)
                app.screen.blit(collecting, (20, 34))

            for idx, (section, ms) in enumerate(top_sections):
                row = app.small_font.render(
                    f"{idx + 1}. {section}: {ms:.2f}",
                    True,
                    SUBTEXT_COLOR,
                )
                app.screen.blit(row, (20, 34 + idx * 18))

    def draw_tag_panels(self) -> None:
        app = self.app

        if not app.selection.show_tag_windows or app.selection.selected_cell is None:
            return

        visible_rect = self.panel_rects["visible_tags"]
        hidden_rect = self.panel_rects["hidden_tags"]

        visible_tags = app.selection.selected_cell.open_visible_window()
        hidden_tags = app.selection.selected_cell.open_hidden_window()

        selected_info = app.small_font.render(
            f"клетка: x={app.selection.selected_cell.x}, y={app.selection.selected_cell.y}",
            True,
            TEXT_COLOR,
        )
        app.screen.blit(
            selected_info,
            (visible_rect.x, visible_rect.y - 28),
        )

        app.panels.draw_panel(
            app.screen,
            visible_rect,
            "Видные теги",
            visible_tags,
            scroll_offset=0,
            lines_are_tag_ids=True,
        )

        app.panels.draw_panel(
            app.screen,
            hidden_rect,
            "Скрытые теги",
            hidden_tags,
            scroll_offset=0,
            lines_are_tag_ids=False,
        )

        self._draw_drag_handle(visible_rect)
        self._draw_drag_handle(hidden_rect)
        self._draw_resize_handle(visible_rect)
        self._draw_resize_handle(hidden_rect)

    def draw_object_browser_panel(self) -> None:
        app = self.app

        if app.object_browser.mode == "closed" or app.object_browser.selected_cell is None:
            return

        rect = self.panel_rects["object_panel"]
        cell = app.object_browser.selected_cell
        lines = app.object_browser.get_lines()
        title = app.object_browser.get_title()

        selected_info = app.small_font.render(
            f"клетка: x={cell.x}, y={cell.y}",
            True,
            TEXT_COLOR,
        )
        app.screen.blit(
            selected_info,
            (rect.x, rect.y - 28),
        )

        app.panels.draw_panel(
            app.screen,
            rect,
            title,
            lines,
            scroll_offset=app.object_browser.scroll_offset,
        )

        self._draw_drag_handle(rect)
        self._draw_resize_handle(rect)

    def draw_layer_browser_panel(self) -> None:
        app = self.app

        if app.layer_browser.mode == "closed" or app.layer_browser.selected_cell is None:
            return

        rect = self.panel_rects["object_panel"]
        cell = app.layer_browser.selected_cell
        lines = app.layer_browser.get_lines()
        title = app.layer_browser.get_title()

        selected_info = app.small_font.render(
            f"клетка: x={cell.x}, y={cell.y}",
            True,
            TEXT_COLOR,
        )
        app.screen.blit(
            selected_info,
            (rect.x, rect.y - 28),
        )

        app.panels.draw_panel(
            app.screen,
            rect,
            title,
            lines,
            scroll_offset=app.layer_browser.scroll_offset,
        )

        self._draw_drag_handle(rect)
        self._draw_resize_handle(rect)

    def draw_time_panel(self) -> None:
        app = self.app

        if not app.time_window.is_open:
            return

        rect = self.panel_rects["time_panel"]
        lines = app.time_window.get_lines()

        app.time_panel.draw_panel(
            app.screen,
            rect,
            "Управление временем",
            lines,
            scroll_offset=app.time_window.scroll_offset,
        )

        self._draw_drag_handle(rect)
        self._draw_resize_handle(rect)

    def draw_layer_view_panel(self) -> None:
        app = self.app

        if not app.layer_view_window.is_open:
            return

        rect = self.panel_rects["layer_view_panel"]
        lines = app.layer_view_window.get_lines()

        app.layer_view_panel.draw_panel(
            app.screen,
            rect,
            "Отображение слоев",
            lines,
            scroll_offset=app.layer_view_window.scroll_offset,
        )

        self._draw_drag_handle(rect)
        self._draw_resize_handle(rect)

    def draw_main_side_panels(self) -> None:
        if self.app.layer_browser.mode != "closed":
            self.draw_layer_browser_panel()
        else:
            self.draw_object_browser_panel()

    def get_active_scroll_target(self):
        app = self.app

        if app.time_window.is_open:
            return app.time_window, self.panel_rects["time_panel"], app.time_window.get_lines()

        if app.layer_view_window.is_open:
            return app.layer_view_window, self.panel_rects["layer_view_panel"], app.layer_view_window.get_lines()

        if app.layer_browser.mode != "closed":
            return app.layer_browser, self.panel_rects["object_panel"], app.layer_browser.get_lines()

        if app.object_browser.mode != "closed":
            return app.object_browser, self.panel_rects["object_panel"], app.object_browser.get_lines()

        return None, None, None

    def get_scroll_max(self):
        target, rect, lines = self.get_active_scroll_target()
        if target is None:
            return 0

        _, max_scroll = self.app.panels.get_scroll_limits(rect, lines)
        return max_scroll

    def _draw_resize_handle(self, rect: pygame.Rect) -> None:
        screen = self.app.screen
        color = (180, 180, 180)

        pygame.draw.line(screen, color, (rect.right - 12, rect.bottom - 4), (rect.right - 4, rect.bottom - 12), 2)
        pygame.draw.line(screen, color, (rect.right - 18, rect.bottom - 4), (rect.right - 4, rect.bottom - 18), 2)
        pygame.draw.line(screen, color, (rect.right - 24, rect.bottom - 4), (rect.right - 4, rect.bottom - 24), 2)

    def _draw_drag_handle(self, rect: pygame.Rect) -> None:
        screen = self.app.screen
        color = (190, 190, 190)
        x = rect.x + 4

        pygame.draw.line(screen, color, (x, rect.y + 8), (x, rect.bottom - 8), 2)
        pygame.draw.line(screen, color, (x + 4, rect.y + 8), (x + 4, rect.bottom - 8), 2)

    def draw_all(self) -> None:
        self.draw_info()
        self.draw_tag_panels()
        self.draw_main_side_panels()
        self.draw_time_panel()
        self.draw_layer_view_panel()
