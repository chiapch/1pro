import random

from world.grid import WorldGrid


MIN_MOISTURE = 0.06
MAX_MOISTURE = 0.95


def clamp(value: float, low: float = MIN_MOISTURE, high: float = MAX_MOISTURE) -> float:
    return max(low, min(high, value))


def generate_static_moisture_map(
    world: WorldGrid,
    *,
    seed: int = 17,
    wet_spot_count: int = 8,
    smoothing_passes: int = 3,
) -> None:
    rng = random.Random(seed)

    anchors: list[tuple[int, int, float, float]] = [
        (
            world.width // 2,
            world.height // 2,
            0.48,
            min(world.width, world.height) * 0.16,
        )
    ]

    for _ in range(wet_spot_count):
        anchors.append(
            (
                rng.randrange(world.width),
                rng.randrange(world.height),
                rng.uniform(0.18, 0.62),
                rng.uniform(6.0, 18.0),
            )
        )

    for y, row in enumerate(world.cells):
        for x, cell in enumerate(row):
            moisture = 0.10 + rng.uniform(-0.015, 0.015)
            for anchor_x, anchor_y, strength, radius in anchors:
                dx = x - anchor_x
                dy = y - anchor_y
                distance = (dx * dx + dy * dy) ** 0.5
                if distance >= radius:
                    continue

                falloff = 1.0 - distance / radius
                moisture += strength * falloff * falloff

            cell.ground_layer.set_base_moisture(clamp(moisture))

    for _ in range(smoothing_passes):
        _smooth_moisture_map(world)


def _smooth_moisture_map(world: WorldGrid) -> None:
    snapshot = [
        [cell.ground_layer.base_moisture for cell in row]
        for row in world.cells
    ]

    for y, row in enumerate(world.cells):
        for x, cell in enumerate(row):
            acc = snapshot[y][x] * 0.55
            weight = 0.55

            for ny in range(max(0, y - 1), min(world.height - 1, y + 1) + 1):
                for nx in range(max(0, x - 1), min(world.width - 1, x + 1) + 1):
                    if nx == x and ny == y:
                        continue
                    acc += snapshot[ny][nx]
                    weight += 1.0

            cell.ground_layer.set_base_moisture(clamp(acc / weight))
