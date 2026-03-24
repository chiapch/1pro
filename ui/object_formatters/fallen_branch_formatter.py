from objects.fallen_branch import FallenBranch


def format_fallen_branch_info(branch: FallenBranch) -> list[str]:
    return [
        "объект: ветка",
        f"id: {branch.id}",
        f"родитель: {branch.origin_object_id}",
        f"скорость гниения: {branch.rot_speed}",
        f"степень гниения: {branch.rot_amount}",
        f"слой: {branch.layer}",
    ]