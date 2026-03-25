from world.cell import Cell
from config import WORLD_WIDTH, WORLD_HEIGHT


class WorldGrid:
    def __init__(self) -> None:
        self.width = WORLD_WIDTH
        self.height = WORLD_HEIGHT
        self.cells = [
            [Cell(x=x, y=y) for x in range(self.width)]
            for y in range(self.height)
        ]
        self._update_tick = 0
        self._tree_update_stride = 1
        self._tree_count_cache = 0

    def get_cell(self, x: int, y: int) -> Cell | None:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.cells[y][x]
        return None

    def update(self, dt: float) -> None:
        self._update_tick += 1
        if self._update_tick % 30 == 0:
            self._refresh_tree_update_stride()

        for row in self.cells:
            for cell in row:
                for layer in cell.get_layers_in_order():
                    if hasattr(layer, "update"):
                        layer.update(dt)

        for row in self.cells:
            for cell in row:
                for layer in cell.get_layers_in_order():
                    objects = layer.get_objects()
                    if not objects:
                        continue

                    for obj in list(objects):
                        if hasattr(obj, "update"):
                            obj_dt = dt
                            if getattr(obj, "object_type", "") == "tree" and self._tree_update_stride > 1:
                                if not self._should_update_tree_this_tick(obj):
                                    pending = getattr(obj, "_pending_dt", 0.0)
                                    setattr(obj, "_pending_dt", pending + dt)
                                    continue
                                pending = getattr(obj, "_pending_dt", 0.0)
                                if pending > 0.0:
                                    obj_dt += pending
                                    setattr(obj, "_pending_dt", 0.0)
                            try:
                                obj.update(obj_dt, self, cell.x, cell.y)
                            except TypeError:
                                obj.update(obj_dt)

    def _refresh_tree_update_stride(self) -> None:
        tree_count = 0
        for row in self.cells:
            for cell in row:
                for obj in cell.standing_layer.get_objects():
                    if getattr(obj, "object_type", "") == "tree":
                        tree_count += 1

        self._tree_count_cache = tree_count

        if tree_count >= 3500:
            self._tree_update_stride = 6
        elif tree_count >= 2200:
            self._tree_update_stride = 4
        elif tree_count >= 900:
            self._tree_update_stride = 3
        elif tree_count >= 350:
            self._tree_update_stride = 2
        else:
            self._tree_update_stride = 1

    def _should_update_tree_this_tick(self, tree_obj) -> bool:
        bucket = abs(hash(tree_obj.id)) % self._tree_update_stride
        return (self._update_tick % self._tree_update_stride) == bucket

    def collect_diagnostics(self) -> dict:
        object_type_counts: dict[str, int] = {}
        layer_counts = {
            "ground": 0,
            "surface": 0,
            "standing": 0,
            "air": 0,
        }
        non_empty_cells = 0
        total_moisture = 0.0

        for row in self.cells:
            for cell in row:
                cell_object_count = 0

                for layer in cell.get_layers_in_order():
                    objects = layer.get_objects()
                    layer_counts[layer.layer_name] += len(objects)
                    cell_object_count += len(objects)

                    for obj in objects:
                        object_type_counts[obj.object_type] = object_type_counts.get(obj.object_type, 0) + 1

                if cell_object_count > 0:
                    non_empty_cells += 1

                total_moisture += cell.ground_layer.moisture

        total_cells = self.width * self.height
        avg_moisture = total_moisture / total_cells if total_cells > 0 else 0.0
        return {
            "world_size": {"width": self.width, "height": self.height},
            "tree_update_stride": self._tree_update_stride,
            "tree_count_cache": self._tree_count_cache,
            "objects_total": sum(layer_counts.values()),
            "non_empty_cells": non_empty_cells,
            "avg_ground_moisture": round(avg_moisture, 6),
            "layer_object_counts": layer_counts,
            "object_type_counts": object_type_counts,
        }
