from dataclasses import dataclass

from objects.world_object import WorldObject


@dataclass
class TreeRoot(WorldObject):
    parent_tree_id: str = ""
    parent_root_id: str | None = None
    root_network_id: str | None = None

    strength: float = 1.0

    uptake_capacity_per_tick: float = 0.03
    self_need_per_tick: float = 0.0015

    depth: int = 0
    branch_order: int = 0
    is_tip: bool = True
    growth_direction: tuple[int, int] | None = None

    last_cell_moisture_before: float = 0.0
    last_cell_moisture_after: float = 0.0
    last_absorbed: float = 0.0
    last_kept: float = 0.0
    last_transferred: float = 0.0

    cell_x: int = 0
    cell_y: int = 0

    def __init__(
        self,
        id: str,
        parent_tree_id: str,
        cell_x: int,
        cell_y: int,
        parent_root_id: str | None = None,
        strength: float = 1.0,
        uptake_capacity_per_tick: float = 0.03,
        self_need_per_tick: float = 0.0015,
        depth: int = 0,
        branch_order: int = 0,
        is_tip: bool = True,
        growth_direction: tuple[int, int] | None = None,
        root_network_id: str | None = None,
    ) -> None:
        super().__init__(
            id=id,
            object_type="tree_root",
            display_name="корень",
            stackable=True,
            layer="ground",
            origin_object_id=parent_tree_id,
        )
        self.parent_tree_id = parent_tree_id
        self.parent_root_id = parent_root_id
        self.root_network_id = root_network_id

        self.cell_x = cell_x
        self.cell_y = cell_y

        self.strength = strength
        self.uptake_capacity_per_tick = uptake_capacity_per_tick
        self.self_need_per_tick = self_need_per_tick

        self.depth = depth
        self.branch_order = branch_order
        self.is_tip = is_tip
        self.growth_direction = growth_direction

        self.last_cell_moisture_before = 0.0
        self.last_cell_moisture_after = 0.0
        self.last_absorbed = 0.0
        self.last_kept = 0.0
        self.last_transferred = 0.0

    def absorb_water(self, ground_layer, dt: float) -> float:
        available = max(0.0, ground_layer.moisture)
        self.last_cell_moisture_before = round(available, 4)

        max_take = self.uptake_capacity_per_tick * dt
        absorbed = min(available, max_take)

        kept = min(absorbed, self.self_need_per_tick * dt)
        transferred = max(0.0, absorbed - kept)

        self.last_absorbed = round(absorbed, 4)
        self.last_kept = round(kept, 4)
        self.last_transferred = round(transferred, 4)
        self.last_cell_moisture_after = round(available, 4)

        return transferred
