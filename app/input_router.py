import sys
import pygame


class InputRouter:
    def __init__(self, app) -> None:
        self.app = app

    def handle_events(self) -> None:
        app = self.app

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if app.window_resize.begin_resize(event.pos):
                        continue
                    if app.window_drag.begin_drag(event.pos):
                        continue

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    app.window_resize.end_resize()
                    app.window_drag.end_drag()

            if event.type == pygame.MOUSEMOTION:
                if app.window_resize.is_resizing:
                    if app.window_resize.update_resize(event.pos):
                        continue

                if app.window_drag.is_dragging:
                    if app.window_drag.update_drag(event.pos):
                        continue

            if event.type == pygame.MOUSEWHEEL:
                if self._handle_scroll(-event.y):
                    continue

                if event.y > 0:
                    app.camera.zoom_in()
                elif event.y < 0:
                    app.camera.zoom_out()

            if event.type == pygame.KEYDOWN:
                self._handle_keydown(event.key)

    def _handle_scroll(self, direction: int) -> bool:
        app = self.app
        target, _, _ = app.ui_manager.get_active_scroll_target()

        if target is None:
            return False

        max_scroll = app.ui_manager.get_scroll_max()

        if direction < 0:
            target.scroll_up()
        elif direction > 0:
            target.scroll_down(max_scroll)

        return True

    def _handle_keydown(self, key: int) -> None:
        app = self.app

        if key == pygame.K_PAGEUP:
            self._handle_scroll(-1)
            return

        if key == pygame.K_PAGEDOWN:
            self._handle_scroll(1)
            return

        if key == pygame.K_q:
            app.selection.handle_open_tags(app.state.hovered_cell)
            return

        if key == pygame.K_x:
            app.object_browser.open_for_cell(app.state.hovered_cell)
            return

        if key == pygame.K_l:
            app.layer_browser.open_for_cell(app.state.hovered_cell)
            return

        if key == pygame.K_t:
            app.time_window.toggle_open()
            return

        if key == pygame.K_v:
            app.layer_view_window.toggle_open()
            return

        if key == pygame.K_ESCAPE:
            app.selection.close_tags()
            app.object_browser.close()
            app.layer_browser.close()
            app.time_window.close()
            app.layer_view_window.close()
            return

        if key in (pygame.K_EQUALS, pygame.K_PLUS, pygame.K_KP_PLUS):
            app.camera.zoom_in()
            return

        if key in (pygame.K_MINUS, pygame.K_KP_MINUS):
            app.camera.zoom_out()
            return

        if key == pygame.K_LEFT:
            if app.time_window.is_open:
                app.time_window.apply_left()
            elif app.layer_view_window.is_open:
                app.layer_view_window.decrease_current_alpha()
            else:
                app.camera.move(40, 0)
            return

        if key == pygame.K_RIGHT:
            if app.time_window.is_open:
                app.time_window.apply_right()
            elif app.layer_view_window.is_open:
                app.layer_view_window.increase_current_alpha()
            else:
                app.camera.move(-40, 0)
            return

        if key == pygame.K_UP:
            app.camera.move(0, 40)
            return

        if key == pygame.K_DOWN:
            app.camera.move(0, -40)
            return

        if key == pygame.K_w:
            if app.time_window.is_open:
                app.time_window.move_up()
            elif app.layer_view_window.is_open:
                app.layer_view_window.move_up()
            elif app.layer_browser.mode != "closed":
                app.layer_browser.move_up()
            else:
                app.object_browser.move_up()
            return

        if key == pygame.K_s:
            if app.time_window.is_open:
                app.time_window.move_down()
            elif app.layer_view_window.is_open:
                app.layer_view_window.move_down()
            elif app.layer_browser.mode != "closed":
                app.layer_browser.move_down()
            else:
                app.object_browser.move_down()
            return

        if key == pygame.K_RETURN:
            if app.time_window.is_open:
                app.time_window.activate()
            elif app.layer_view_window.is_open:
                app.layer_view_window.toggle_current_visibility()
            elif app.layer_browser.mode != "closed":
                app.layer_browser.select_current()
            else:
                app.object_browser.select_current()
            return

        if key == pygame.K_BACKSPACE:
            if app.layer_browser.mode != "closed":
                app.layer_browser.go_back()
            else:
                app.object_browser.go_back()