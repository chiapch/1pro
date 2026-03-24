import pygame

from config import (
    PANEL_BG_COLOR,
    PANEL_BORDER_COLOR,
    TEXT_COLOR,
    SUBTEXT_COLOR,
)


class LayerViewSettingsPanel:
    def __init__(self, font: pygame.font.Font, small_font: pygame.font.Font) -> None:
        self.font = font
        self.small_font = small_font
        self.line_height = 20
        self.header_height = 48
        self.footer_height = 24
        self.padding_x = 12
        self.scrollbar_width = 10

    def draw_panel(
        self,
        surface: pygame.Surface,
        rect: pygame.Rect,
        title: str,
        line_items: list[dict],
        scroll_offset: int = 0,
        footer_text: str | None = None,
    ) -> None:
        pygame.draw.rect(surface, PANEL_BG_COLOR, rect)
        pygame.draw.rect(surface, PANEL_BORDER_COLOR, rect, 2)

        title_surf = self.font.render(title, True, TEXT_COLOR)
        surface.blit(title_surf, (rect.x + self.padding_x, rect.y + 10))

        content_rect = pygame.Rect(
            rect.x + self.padding_x,
            rect.y + self.header_height,
            rect.width - self.padding_x * 2 - self.scrollbar_width - 4,
            rect.height - self.header_height - self.footer_height - 6,
        )

        footer_rect = pygame.Rect(
            rect.x + self.padding_x,
            rect.bottom - self.footer_height,
            rect.width - self.padding_x * 2,
            self.footer_height,
        )

        max_visible_lines = max(1, content_rect.height // self.line_height)
        max_scroll = max(0, len(line_items) - max_visible_lines)
        scroll_offset = max(0, min(scroll_offset, max_scroll))

        old_clip = surface.get_clip()
        surface.set_clip(content_rect)

        start = scroll_offset
        end = min(len(line_items), scroll_offset + max_visible_lines)

        y = content_rect.y
        for item in line_items[start:end]:
            text = item["text"]
            enabled = item.get("enabled", True)
            selected = item.get("selected", False)

            prefix = "> " if selected else "  "
            color = TEXT_COLOR if enabled else SUBTEXT_COLOR

            txt = self.small_font.render(prefix + str(text), True, color)
            surface.blit(txt, (content_rect.x, y))
            y += self.line_height

            if y > content_rect.bottom:
                break

        surface.set_clip(old_clip)

        self._draw_scrollbar(
            surface=surface,
            rect=rect,
            content_rect=content_rect,
            total_lines=len(line_items),
            visible_lines=max_visible_lines,
            scroll_offset=scroll_offset,
        )

        footer = footer_text
        if footer is None:
            footer = f"строки: {min(len(line_items), start + 1)}-{end} / {len(line_items)}"

        footer_surf = self.small_font.render(footer, True, SUBTEXT_COLOR)
        surface.blit(footer_surf, (footer_rect.x, footer_rect.y))

    def _draw_scrollbar(
        self,
        surface: pygame.Surface,
        rect: pygame.Rect,
        content_rect: pygame.Rect,
        total_lines: int,
        visible_lines: int,
        scroll_offset: int,
    ) -> None:
        bar_x = rect.right - self.scrollbar_width - 6
        bar_y = content_rect.y
        bar_h = content_rect.height

        track_rect = pygame.Rect(bar_x, bar_y, self.scrollbar_width, bar_h)
        pygame.draw.rect(surface, (70, 70, 70), track_rect)

        if total_lines <= 0 or total_lines <= visible_lines:
            thumb_rect = pygame.Rect(bar_x, bar_y, self.scrollbar_width, bar_h)
            pygame.draw.rect(surface, (130, 130, 130), thumb_rect)
            return

        thumb_h = max(20, int(bar_h * (visible_lines / total_lines)))
        max_scroll = total_lines - visible_lines
        travel = bar_h - thumb_h
        thumb_y = bar_y + int(travel * (scroll_offset / max_scroll))

        thumb_rect = pygame.Rect(bar_x, thumb_y, self.scrollbar_width, thumb_h)
        pygame.draw.rect(surface, (170, 170, 170), thumb_rect)