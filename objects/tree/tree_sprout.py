from dataclasses import dataclass

from objects.world_object import WorldObject


@dataclass
class TreeSprout(WorldObject):
    parent_tree_id: str = ""
    origin_root_id: str | None = None
    root_network_id: str | None = None
    species_id: str = "default_tree"

    age: float = 0.0
    health: float = 1.0
    growth_progress: float = 0.0
    alive: bool = True

    cell_x: int = 0
    cell_y: int = 0

    last_support_income: float = 0.0
    support_need_per_tick: float = 0.0015
    growth_need_per_tick: float = 0.001
    last_support_paid: float = 0.0
    last_growth_paid: float = 0.0

    def __init__(
        self,
        id: str,
        parent_tree_id: str,
        origin_root_id: str | None,
        root_network_id: str | None,
        species_id: str,
        cell_x: int,
        cell_y: int,
    ) -> None:
        super().__init__(
            id=id,
            object_type="tree_sprout",
            display_name="росток",
            stackable=False,
            layer="standing",
            origin_object_id=parent_tree_id,
        )
        self.parent_tree_id = parent_tree_id
        self.origin_root_id = origin_root_id
        self.root_network_id = root_network_id
        self.species_id = species_id

        self.age = 0.0
        self.health = 1.0
        self.growth_progress = 0.0
        self.alive = True

        self.cell_x = cell_x
        self.cell_y = cell_y

        self.last_support_income = 0.0
        self.support_need_per_tick = 0.0015
        self.growth_need_per_tick = 0.001
        self.last_support_paid = 0.0
        self.last_growth_paid = 0.0

    def update(self, dt: float, world, cell_x: int, cell_y: int) -> None:
        from objects.tree.tree_sprout_growth_logic import process_tree_sprout_growth

        self.cell_x = cell_x
        self.cell_y = cell_y
        process_tree_sprout_growth(self, dt, world)
