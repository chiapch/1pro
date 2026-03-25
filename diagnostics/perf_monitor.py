import json
import time
from collections import defaultdict, deque
from contextlib import contextmanager
from pathlib import Path
from typing import Callable


class PerfMonitor:
    def __init__(
        self,
        enabled: bool = False,
        history_size: int = 180,
        log_every_frames: int = 120,
        output_path: str = "diagnostics/output/perf_log.jsonl",
    ) -> None:
        self.enabled = enabled
        self.history: deque[dict[str, float]] = deque(maxlen=history_size)
        self.current_frame_sections: dict[str, float] = defaultdict(float)
        self.frame_start: float = 0.0
        self.frame_index = 0
        self.log_every_frames = log_every_frames

        self.output_path = Path(output_path)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.extra_snapshot_provider: Callable[[], dict] | None = None

    def toggle(self) -> bool:
        self.enabled = not self.enabled
        if self.enabled:
            self.current_frame_sections.clear()
            self.frame_start = time.perf_counter()
        return self.enabled

    def begin_frame(self) -> None:
        if not self.enabled:
            return
        self.current_frame_sections.clear()
        self.frame_start = time.perf_counter()

    def end_frame(self) -> None:
        if not self.enabled:
            return

        total = time.perf_counter() - self.frame_start
        self.current_frame_sections["frame.total"] += total
        self.history.append(dict(self.current_frame_sections))
        self.frame_index += 1

        if self.frame_index % self.log_every_frames == 0:
            self._flush_snapshot_to_log()

    @contextmanager
    def measure(self, section: str):
        if not self.enabled:
            yield
            return

        start = time.perf_counter()
        try:
            yield
        finally:
            elapsed = time.perf_counter() - start
            self.current_frame_sections[section] += elapsed

    def get_top_sections(self, top_n: int = 5) -> list[tuple[str, float]]:
        if not self.history:
            return []

        aggregate: dict[str, float] = defaultdict(float)
        for frame_data in self.history:
            for section, value in frame_data.items():
                aggregate[section] += value

        frame_count = len(self.history)
        averages_ms = [
            (section, (total / frame_count) * 1000.0)
            for section, total in aggregate.items()
        ]
        averages_ms.sort(key=lambda item: item[1], reverse=True)
        return averages_ms[:top_n]

    def set_extra_snapshot_provider(self, provider: Callable[[], dict] | None) -> None:
        self.extra_snapshot_provider = provider

    def _flush_snapshot_to_log(self) -> None:
        snapshot = {
            "timestamp": time.time(),
            "frame_index": self.frame_index,
            "top_sections_ms": self.get_top_sections(top_n=12),
            "window_frames": len(self.history),
        }

        if self.extra_snapshot_provider is not None:
            try:
                extra = self.extra_snapshot_provider()
                if isinstance(extra, dict):
                    snapshot.update(extra)
            except Exception as exc:
                snapshot["extra_snapshot_error"] = str(exc)

        with self.output_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(snapshot, ensure_ascii=False) + "\n")
