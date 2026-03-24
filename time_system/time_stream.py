from dataclasses import dataclass

from time_system.time_state import TimeState


@dataclass
class TimeStream:
    stream_id: str
    display_name: str
    state: TimeState