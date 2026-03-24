import pygame

from config import (
    WORLD_VIEW_X,
    WORLD_VIEW_Y,
    WORLD_VIEW_WIDTH,
    WORLD_VIEW_HEIGHT,
)


class WorldViewport:
    def __init__(self) -> None:
        self.rect = pygame.Rect(
            WORLD_VIEW_X,
            WORLD_VIEW_Y,
            WORLD_VIEW_WIDTH,
            WORLD_VIEW_HEIGHT,
        )
