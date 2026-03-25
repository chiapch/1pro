from dataclasses import dataclass, field

from objects.world_object import WorldObject
from objects.tree.tree_water_logic import process_tree_water
from objects.tree.tree_root import TreeRoot
from objects.tree.tree_growth_logic import process_tree_growth
from objects.tree.tree_root_growth_logic import process_tree_root_growth
from objects.tree.tree_canopy_logic import (
    get_branch_drop_chance,
    get_branch_regrow_chance,
    get_leaf_drop_chance,
    get_leaf_regrow_chance,
    process_tree_canopy,
)
from objects.tree.tree_reproduction_logic import process_tree_reproduction


@dataclass
class Tree(WorldObject):
    species_id: str = "default_tree"
    root_network_id: str | None = None

    age: int = 0
    trunk_thickness: float = 0.0
    height: float = 0.0

    branch_count: int = 0
    max_branch_count: int = 0

    leaf_count: int = 0
    max_leaf_count: int = 0

    branch_drop_check_interval: float = 10.0
    branch_drop_base_chance: float = 0.05

    branch_regrow_check_interval: float = 20.0
    branch_regrow_base_chance: float = 0.10

    leaf_drop_check_interval: float = 2.0
    leaf_drop_base_chance: float = 0.15

    leaf_regrow_check_interval: float = 4.0
    leaf_regrow_base_chance: float = 0.20

    branch_drop_modifiers: dict[str, float] = field(default_factory=dict)
    branch_regrow_modifiers: dict[str, float] = field(default_factory=dict)
    leaf_drop_modifiers: dict[str, float] = field(default_factory=dict)
    leaf_regrow_modifiers: dict[str, float] = field(default_factory=dict)

    root_positions: list[tuple[int, int]] = field(default_factory=list)
    root_objects: list[TreeRoot] = field(default_factory=list)

    last_water_income: float = 0.0
    water_buffer: float = 0.0
    water_buffer_capacity: float = 1.0
    _water_needs_signature: tuple[float, float] | None = None

    maintenance_water_need_per_tick: float = 0.0
    growth_water_need_per_tick: float = 0.0

    last_maintenance_paid: float = 0.0
    last_growth_paid: float = 0.0

    growth_progress: float = 0.0
    health: float = 1.0
    alive: bool = True

    root_growth_check_interval: float = 8.0
    root_growth_base_chance: float = 0.35
    max_root_growth_attempts_per_cycle: int = 24
    max_new_roots_per_cycle: int = 3
    max_root_count: int = 1200
    max_root_growth_cycles_per_update: int = 2
    _root_growth_progress: float = 0.0

    sprout_check_interval: float = 12.0
    sprout_spawn_chance: float = 0.18
    min_reproduction_age: float = 12.0
    min_reproduction_water_ratio: float = 0.45
    has_active_sprout: bool = False
    max_active_sprouts: int = 3
    max_sprout_checks_per_update: int = 2
    active_sprout_count: int = 0
    _sprout_growth_progress: float = 0.0

    _branch_drop_progress: float = 0.0
    _branch_regrow_progress: float = 0.0
    _leaf_drop_progress: float = 0.0
    _leaf_regrow_progress: float = 0.0
    max_canopy_checks_per_update: int = 3

    last_canopy_event: str = "none"
    last_leaf_drop_roll: float = -1.0
    last_branch_drop_roll: float = -1.0
    dropped_leaves_total: int = 0
    dropped_branches_total: int = 0

    def __init__(
        self,
        id: str,
        age: int,
        trunk_thickness: float,
        height: float,
        branch_count: int,
        max_branch_count: int,
        leaf_count: int,
        max_leaf_count: int,
        branch_drop_check_interval: float,
        branch_drop_base_chance: float,
        branch_regrow_check_interval: float,
        branch_regrow_base_chance: float,
        leaf_drop_check_interval: float,
        leaf_drop_base_chance: float,
        leaf_regrow_check_interval: float,
        leaf_regrow_base_chance: float,
        species_id: str = "default_tree",
        root_network_id: str | None = None,
    ) -> None:
        super().__init__(
            id=id,
            object_type="tree",
            display_name="дерево",
            stackable=False,
            layer="standing",
            origin_object_id=None,
        )

        self.species_id = species_id
        self.root_network_id = root_network_id

        self.age = age
        self.trunk_thickness = trunk_thickness
        self.height = height

        self.branch_count = branch_count
        self.max_branch_count = max_branch_count

        self.leaf_count = leaf_count
        self.max_leaf_count = max_leaf_count

        self.branch_drop_check_interval = branch_drop_check_interval
        self.branch_drop_base_chance = branch_drop_base_chance

        self.branch_regrow_check_interval = branch_regrow_check_interval
        self.branch_regrow_base_chance = branch_regrow_base_chance

        self.leaf_drop_check_interval = leaf_drop_check_interval
        self.leaf_drop_base_chance = leaf_drop_base_chance

        self.leaf_regrow_check_interval = leaf_regrow_check_interval
        self.leaf_regrow_base_chance = leaf_regrow_base_chance

        self.branch_drop_modifiers = {}
        self.branch_regrow_modifiers = {}
        self.leaf_drop_modifiers = {}
        self.leaf_regrow_modifiers = {}

        self.root_positions = []
        self.root_objects = []

        self.last_water_income = 0.0
        self.water_buffer_capacity = round(
            0.25 + self.height * 0.03 + self.trunk_thickness * 0.08,
            4,
        )
        self.water_buffer = round(self.water_buffer_capacity * 0.55, 4)
        self._water_needs_signature = None

        self.maintenance_water_need_per_tick = 0.0
        self.growth_water_need_per_tick = 0.0
        self.last_maintenance_paid = 0.0
        self.last_growth_paid = 0.0

        self.growth_progress = 0.0
        self.health = 1.0
        self.alive = True

        self.root_growth_check_interval = 8.0
        self.root_growth_base_chance = 0.35
        self.max_root_growth_attempts_per_cycle = 24
        self.max_new_roots_per_cycle = 3
        self.max_root_count = 1200
        self.max_root_growth_cycles_per_update = 2
        self._root_growth_progress = 0.0

        self.sprout_check_interval = 12.0
        self.sprout_spawn_chance = 0.18
        self.min_reproduction_age = 12.0
        self.min_reproduction_water_ratio = 0.45
        self.has_active_sprout = False
        self.max_active_sprouts = 3
        self.max_sprout_checks_per_update = 2
        self.active_sprout_count = 0
        self._sprout_growth_progress = 0.0

        self._branch_drop_progress = 0.0
        self._branch_regrow_progress = 0.0
        self._leaf_drop_progress = 0.0
        self._leaf_regrow_progress = 0.0
        self.max_canopy_checks_per_update = 3

        self.last_canopy_event = "none"
        self.last_leaf_drop_roll = -1.0
        self.last_branch_drop_roll = -1.0
        self.dropped_leaves_total = 0
        self.dropped_branches_total = 0

    def set_branch_drop_modifier(self, source: str, value: float) -> None:
        self.branch_drop_modifiers[source] = value

    def remove_branch_drop_modifier(self, source: str) -> None:
        self.branch_drop_modifiers.pop(source, None)

    def set_branch_regrow_modifier(self, source: str, value: float) -> None:
        self.branch_regrow_modifiers[source] = value

    def remove_branch_regrow_modifier(self, source: str) -> None:
        self.branch_regrow_modifiers.pop(source, None)

    def set_leaf_drop_modifier(self, source: str, value: float) -> None:
        self.leaf_drop_modifiers[source] = value

    def remove_leaf_drop_modifier(self, source: str) -> None:
        self.leaf_drop_modifiers.pop(source, None)

    def set_leaf_regrow_modifier(self, source: str, value: float) -> None:
        self.leaf_regrow_modifiers[source] = value

    def remove_leaf_regrow_modifier(self, source: str) -> None:
        self.leaf_regrow_modifiers.pop(source, None)

    def get_branch_drop_chance(self) -> float:
        return get_branch_drop_chance(self)

    def get_branch_regrow_chance(self) -> float:
        return get_branch_regrow_chance(self)

    def get_leaf_drop_chance(self) -> float:
        return get_leaf_drop_chance(self)

    def get_leaf_regrow_chance(self) -> float:
        return get_leaf_regrow_chance(self)

    def update(self, dt: float, world, cell_x: int, cell_y: int) -> None:
        if not self.alive:
            return

        monitor = getattr(world, "perf_monitor", None)
        if monitor is None:
            process_tree_water(self, dt, world)
            process_tree_growth(self, dt)
            process_tree_root_growth(self, dt, world, cell_x, cell_y)
            process_tree_reproduction(self, dt, world)
            process_tree_canopy(self, dt, world, cell_x, cell_y)
            return

        with monitor.measure("tree.water"):
            process_tree_water(self, dt, world)
        with monitor.measure("tree.growth"):
            process_tree_growth(self, dt)
        with monitor.measure("tree.root_growth"):
            process_tree_root_growth(self, dt, world, cell_x, cell_y)
        with monitor.measure("tree.reproduction"):
            process_tree_reproduction(self, dt, world)
        with monitor.measure("tree.canopy"):
            process_tree_canopy(self, dt, world, cell_x, cell_y)

    def register_root(self, root: TreeRoot) -> None:
        self.root_positions.append((root.cell_x, root.cell_y))
        self.root_objects.append(root)
