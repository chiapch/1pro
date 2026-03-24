from dataclasses import dataclass, field


@dataclass
class TimeState:
    is_paused: bool = False
    direction: int = 1

    speed_steps: list[float] = field(default_factory=lambda: [
        0.25,
        0.5,
        1.0,
        2.0,
        5.0,
        10.0,
        20.0,
        50.0,
        100.0,
    ])
    speed_index: int = 2

    total_real_time: float = 0.0
    total_simulation_time: float = 0.0

    def current_speed(self) -> float:
        return self.speed_steps[self.speed_index]