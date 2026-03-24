from time_system.time_state import TimeState
from time_system.time_stream import TimeStream


class TimeController:
    def __init__(self) -> None:
        self.main_stream = TimeStream(
            stream_id="main",
            display_name="main",
            state=TimeState(),
        )
        self.current_stream = self.main_stream

    def update(self, real_dt: float) -> float:
        state = self.current_stream.state
        state.total_real_time += real_dt

        if state.is_paused:
            return 0.0

        simulation_dt = real_dt * state.current_speed() * state.direction
        state.total_simulation_time += simulation_dt
        return simulation_dt

    def toggle_pause(self) -> None:
        state = self.current_stream.state
        state.is_paused = not state.is_paused

    def increase_speed(self) -> None:
        state = self.current_stream.state
        if state.speed_index < len(state.speed_steps) - 1:
            state.speed_index += 1

    def decrease_speed(self) -> None:
        state = self.current_stream.state
        if state.speed_index > 0:
            state.speed_index -= 1

    def get_state(self) -> TimeState:
        return self.current_stream.state

    def get_stream_name(self) -> str:
        return self.current_stream.display_name