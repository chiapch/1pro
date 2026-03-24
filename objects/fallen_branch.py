from dataclasses import dataclass

from objects.world_object import WorldObject


@dataclass
class FallenBranch(WorldObject):
    rot_speed: float = 0.0
    rot_amount: float = 0.0

    def __init__(
        self,
        id: str,
        origin_object_id: str | None,
        rot_speed: float,
        rot_amount: float = 0.0,
    ) -> None:
        super().__init__(
            id=id,
            object_type="fallen_branch",
            display_name="ветка",
            stackable=True,
            layer="ground",
            origin_object_id=origin_object_id,
        )
        self.rot_speed = rot_speed
        self.rot_amount = rot_amount

    def update(self, dt: float) -> None:
        self.rot_amount += self.rot_speed * dt
        if self.rot_amount > 1.0:
            self.rot_amount = 1.0