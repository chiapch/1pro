import pygame

from config import (
    PANEL_BG_COLOR,
    PANEL_BORDER_COLOR,
    TEXT_COLOR,
    SUBTEXT_COLOR,
)


class TimeWindowPanel:
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

        wrapped_lines = self._wrap_line_items(line_items, content_rect.width)

        max_visible_lines = max(1, content_rect.height // self.line_height)
        max_scroll = max(0, len(wrapped_lines) - max_visible_lines)
        scroll_offset = max(0, min(scroll_offset, max_scroll))

        old_clip = surface.get_clip()
        surface.set_clip(content_rect)

        start = scroll_offset
        end = min(len(wrapped_lines), scroll_offset + max_visible_lines)

        y = content_rect.y
        for item in wrapped_lines[start:end]:
            text = item["text"]
            enabled = item.get("enabled", True)
            selected = item.get("selected", False)

            prefix = "> " if selected else "  "
            color = TEXT_COLOR if enabled else SUBTEXT_COLOR

            txt = self.small_font.render(prefix + str(text), True, color)
            surface.blit(txt, (content_rect.x, y))
            y += self.line_height

        surface.set_clip(old_clip)

        self._draw_scrollbar(
            surface=surface,
            rect=rect,
            content_rect=content_rect,
            total_lines=len(wrapped_lines),
            visible_lines=max_visible_lines,
            scroll_offset=scroll_offset,
        )

        footer = footer_text
        if footer is None:
            footer = f"строки: {min(len(wrapped_lines), start + 1)}-{end} / {len(wrapped_lines)}"

        footer_surf = self.small_font.render(footer, True, SUBTEXT_COLOR)
        surface.blit(footer_surf, (footer_rect.x, footer_rect.y))

    def _wrap_line_items(self, items: list[dict], max_width: int) -> list[dict]:
        wrapped: list[dict] = []

        for item in items:
            text = str(item.get("text", ""))
            parts = self._wrap_text(text, max_width)

            for idx, part in enumerate(parts):
                wrapped.append({
                    "text": part,
                    "enabled": item.get("enabled", True),
                    "selected": item.get("selected", False) if idx == 0 else False,
                })

        return wrapped

    def _wrap_text(self, text: str, max_width: int) -> list[str]:
        if text == "":
            return [""]

        words = text.split(" ")
        lines: list[str] = []
        current = ""

        for word in words:
            test = word if current == "" else current + " " + word
            test_width = self.small_font.size("  " + test)[0]

            if test_width <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                    current = word
                else:
                    lines.append(word)

        if current:
            lines.append(current)

        return lines if lines else [""]

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