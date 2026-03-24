import pygame

from objects.tree.tree import Tree
from objects.tree.tree_root import TreeRoot
from objects.tree.tree_sprout import TreeSprout
from objects.fallen_branch import FallenBranch
from objects.fallen_foliage import FallenFoliage


TREE_COLOR = (110, 70, 35)
TREE_OUTLINE_COLOR = (70, 45, 20)

ROOT_COLOR = (90, 55, 30)

BRANCH_COLOR = (150, 110, 70)
FOLIAGE_COLOR = (90, 120, 70)
SPROUT_COLOR = (130, 190, 95)


class ObjectRenderer:
    def draw_cell_objects(
        self,
        screen: pygame.Surface,
        rect: pygame.Rect,
        cell,
        layer_visibility,
    ) -> None:
        ground_objects = cell.ground_layer.get_objects()
        surface_objects = cell.surface_layer.get_objects()
        standing_objects = cell.standing_layer.get_objects()
        air_objects = cell.air_layer.get_objects()

        if layer_visibility.is_visible("ground"):
            alpha = layer_visibility.get_alpha("ground")
            self.draw_ground_objects(screen, rect, ground_objects, alpha)

        if layer_visibility.is_visible("surface"):
            alpha = layer_visibility.get_alpha("surface")
            self.draw_surface_objects(screen, rect, surface_objects, alpha)

        if layer_visibility.is_visible("standing"):
            alpha = layer_visibility.get_alpha("standing")
            self.draw_standing_objects(screen, rect, standing_objects, alpha)

        if layer_visibility.is_visible("air"):
            alpha = layer_visibility.get_alpha("air")
            self.draw_air_objects(screen, rect, air_objects, alpha)

    def draw_ground_objects(self, screen: pygame.Surface, rect: pygame.Rect, objects: list, alpha: float) -> None:
        root_count = sum(1 for obj in objects if isinstance(obj, TreeRoot))
        if root_count > 0:
            self.draw_root_marker(screen, rect, root_count, alpha)

    def draw_surface_objects(self, screen: pygame.Surface, rect: pygame.Rect, objects: list, alpha: float) -> None:
        ground_branch_count = sum(1 for obj in objects if isinstance(obj, FallenBranch))
        ground_foliage_count = sum(1 for obj in objects if isinstance(obj, FallenFoliage))

        if ground_branch_count > 0:
            self.draw_ground_branch_marker(screen, rect, ground_branch_count, alpha)

        if ground_foliage_count > 0:
            self.draw_ground_foliage_marker(screen, rect, ground_foliage_count, alpha)

    def draw_standing_objects(self, screen: pygame.Surface, rect: pygame.Rect, objects: list, alpha: float) -> None:
        for obj in objects:
            if isinstance(obj, Tree):
                self.draw_tree(screen, rect, obj, alpha)
            elif isinstance(obj, TreeSprout):
                self.draw_tree_sprout(screen, rect, alpha)

    def draw_air_objects(self, screen: pygame.Surface, rect: pygame.Rect, objects: list, alpha: float) -> None:
        pass

    def draw_tree(self, screen: pygame.Surface, rect: pygame.Rect, tree: Tree, alpha: float) -> None:
        size = min(rect.width, rect.height)
        if size < 3 or alpha <= 0.0:
            return

        overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)

        trunk_height_ratio = min(0.95, 0.25 + tree.height / 40.0)
        trunk_width_ratio = min(0.8, 0.12 + tree.trunk_thickness / 6.0)

        trunk_height = max(3, int(rect.height * trunk_height_ratio))
        trunk_width = max(2, int(rect.width * trunk_width_ratio))

        trunk_x = (rect.width - trunk_width) // 2
        trunk_y = rect.height - trunk_height

        fill = (*TREE_COLOR, int(255 * alpha))
        outline = (*TREE_OUTLINE_COLOR, int(255 * alpha))

        trunk_rect = pygame.Rect(trunk_x, trunk_y, trunk_width, trunk_height)
        pygame.draw.rect(overlay, fill, trunk_rect)

        if rect.width >= 8:
            pygame.draw.rect(overlay, outline, trunk_rect, 1)

        screen.blit(overlay, (rect.x, rect.y))

    def draw_root_marker(self, screen: pygame.Surface, rect: pygame.Rect, count: int, alpha: float) -> None:
        if rect.width < 6 or rect.height < 6 or alpha <= 0.0:
            return

        overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        color = (*ROOT_COLOR, int(255 * alpha))

        start = (2, rect.height - 3)
        mid = (rect.width // 2, rect.height // 2)
        end = (rect.width - 3, 2)

        pygame.draw.line(overlay, color, start, mid, 2)
        pygame.draw.line(overlay, color, mid, end, 2)

        if count > 1:
            pygame.draw.line(
                overlay,
                color,
                (rect.width // 2, rect.height // 2),
                (rect.width // 3, 2),
                2,
            )

        screen.blit(overlay, (rect.x, rect.y))

    def draw_ground_branch_marker(self, screen: pygame.Surface, rect: pygame.Rect, count: int, alpha: float) -> None:
        if rect.width < 6 or rect.height < 6 or alpha <= 0.0:
            return

        overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        color = (*BRANCH_COLOR, int(255 * alpha))

        line_y = rect.height - max(2, rect.height // 5)
        start_x = 2
        end_x = min(rect.width - 2, start_x + max(4, min(count * 2, rect.width - 4)))
        pygame.draw.line(overlay, color, (start_x, line_y), (end_x, line_y), 2)

        screen.blit(overlay, (rect.x, rect.y))

    def draw_ground_foliage_marker(self, screen: pygame.Surface, rect: pygame.Rect, count: int, alpha: float) -> None:
        if rect.width < 6 or rect.height < 6 or alpha <= 0.0:
            return

        overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        color = (*FOLIAGE_COLOR, int(255 * alpha))

        radius = 2
        x = rect.width - 4
        y = 4
        pygame.draw.circle(overlay, color, (x, y), radius)

        screen.blit(overlay, (rect.x, rect.y))

    def draw_tree_sprout(self, screen: pygame.Surface, rect: pygame.Rect, alpha: float) -> None:
        if rect.width < 4 or rect.height < 4 or alpha <= 0.0:
            return

        overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        color = (*SPROUT_COLOR, int(255 * alpha))

        stem_bottom = (rect.width // 2, rect.height - 2)
        stem_top = (rect.width // 2, max(1, rect.height // 3))
        pygame.draw.line(overlay, color, stem_bottom, stem_top, 2)

        leaf_radius = max(1, rect.width // 6)
        pygame.draw.circle(
            overlay,
            color,
            (max(1, rect.width // 2 - leaf_radius), max(1, rect.height // 3)),
            leaf_radius,
        )
        pygame.draw.circle(
            overlay,
            color,
            (min(rect.width - 2, rect.width // 2 + leaf_radius), max(1, rect.height // 3)),
            leaf_radius,
        )

        screen.blit(overlay, (rect.x, rect.y))
