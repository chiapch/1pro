from objects.fallen_foliage import FallenFoliage


def format_fallen_foliage_info(foliage: FallenFoliage) -> list[str]:
    return [
        "объект: листва",
        f"id: {foliage.id}",
        f"родитель: {foliage.origin_object_id}",
        f"скорость гниения: {foliage.rot_speed}",
        f"степень гниения: {foliage.rot_amount}",
        f"слой: {foliage.layer}",
    ]