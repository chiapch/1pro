def group_objects(objects: list) -> list[dict]:
    groups: dict[str, dict] = {}

    for obj in objects:
        key = obj.object_type

        if key not in groups:
            groups[key] = {
                "group_key": key,
                "display_name": obj.display_name,
                "count": 0,
                "objects": [],
            }

        groups[key]["count"] += 1
        groups[key]["objects"].append(obj)

    return list(groups.values())