import pygame

from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    BG_COLOR,
    WORLD_VIEW_BG_COLOR,
    WORLD_VIEW_BORDER_COLOR,
    CELL_COLOR,
    CELL_HOVER_COLOR,
    CELL_SELECTED_COLOR,
    GRID_LINE_COLOR,
)
from app.app_state import AppState
from app.input_router import InputRouter
from app.ui_manager import UIManager
from world.grid import WorldGrid
from ui.panels import TagPanels
from ui.time_window_panel import TimeWindowPanel
from ui.layer_view_settings_panel import LayerViewSettingsPanel
from view.viewport import WorldViewport
from view.camera import Camera
from controllers.selection_controller import SelectionController
from controllers.object_browser_controller import ObjectBrowserController
from controllers.layer_browser_controller import LayerBrowserController
from controllers.time_window_controller import TimeWindowController
from controllers.layer_view_settings_controller import LayerViewSettingsController
from render.object_renderer import ObjectRenderer
from render.layer_visibility_controller import LayerVisibilityController
from tags import register_all_tags
from generation import generate_world
from time_system import TimeController
from controllers.window_resize_controller import WindowResizeController
from controllers.window_drag_controller import WindowDragController
from diagnostics import PerfMonitor


class Application:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Мир 100x100")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("arial", 24)
        self.small_font = pygame.font.SysFont("arial", 18)

        self.state = AppState()
        self.perf_monitor = PerfMonitor(enabled=False)

        register_all_tags()

        self.world = WorldGrid()
        self.world.perf_monitor = self.perf_monitor
        generate_world(self.world)

        self.time_controller = TimeController()
        self.layer_visibility = LayerVisibilityController()

        self.panels = TagPanels(self.font, self.small_font)
        self.time_panel = TimeWindowPanel(self.font, self.small_font)
        self.layer_view_panel = LayerViewSettingsPanel(self.font, self.small_font)

        self.selection = SelectionController()
        self.object_browser = ObjectBrowserController()
        self.layer_browser = LayerBrowserController()
        self.time_window = TimeWindowController(self.time_controller)
        self.layer_view_window = LayerViewSettingsController(self.layer_visibility)

        self.object_renderer = ObjectRenderer()

        self.viewport = WorldViewport()
        self.camera = Camera(self.viewport.rect)

        self.input_router = InputRouter(self)
        self.ui_manager = UIManager(self)
        self.window_resize = WindowResizeController(self.ui_manager)
        self.window_drag = WindowDragController(self.ui_manager)

    def screen_to_cell(self, mouse_x: int, mouse_y: int):
        coords = self.camera.screen_to_cell_coords(mouse_x, mouse_y)
        if coords is None:
            return None
        x, y = coords
        return self.world.get_cell(x, y)

    def update_hover(self) -> None:
        mx, my = pygame.mouse.get_pos()
        self.state.hovered_cell = self.screen_to_cell(mx, my)

    def update(self, real_dt: float) -> None:
        with self.perf_monitor.measure("app.update.total"):
            simulation_dt = self.time_controller.update(real_dt)
            with self.perf_monitor.measure("world.update"):
                self.world.update(simulation_dt)
            self.update_hover()

    def draw_world_area(self) -> None:
        pygame.draw.rect(self.screen, WORLD_VIEW_BG_COLOR, self.viewport.rect)
        pygame.draw.rect(self.screen, WORLD_VIEW_BORDER_COLOR, self.viewport.rect, 2)

        old_clip = self.screen.get_clip()
        self.screen.set_clip(self.viewport.rect)

        x_start, x_end, y_start, y_end = self.camera.get_visible_cell_bounds()

        for y in range(y_start, y_end + 1):
            for x in range(x_start, x_end + 1):
                cell = self.world.get_cell(x, y)
                rect = self.camera.get_cell_rect(x, y)

                color = CELL_COLOR

                if self.state.hovered_cell is not None and cell == self.state.hovered_cell:
                    color = CELL_HOVER_COLOR

                if self.selection.selected_cell is not None and cell == self.selection.selected_cell:
                    color = CELL_SELECTED_COLOR

                pygame.draw.rect(self.screen, color, rect)

                self.object_renderer.draw_cell_objects(
                    self.screen,
                    rect,
                    cell,
                    self.layer_visibility,
                )

                if self.camera.cell_size >= 8:
                    pygame.draw.rect(self.screen, GRID_LINE_COLOR, rect, 1)

        self.screen.set_clip(old_clip)

    def draw(self) -> None:
        with self.perf_monitor.measure("app.draw.total"):
            self.screen.fill(BG_COLOR)
            with self.perf_monitor.measure("draw.world"):
                self.draw_world_area()
            with self.perf_monitor.measure("draw.ui"):
                self.ui_manager.draw_all()
            pygame.display.flip()

    def run(self) -> None:
        while True:
            real_dt = self.clock.tick(FPS) / 1000.0
            self.perf_monitor.begin_frame()
            self.input_router.handle_events()
            self.update(real_dt)
            self.draw()
            self.perf_monitor.end_frame()
