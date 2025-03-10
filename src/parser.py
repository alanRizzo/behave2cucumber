import itertools

JSON_NODES = ["feature", "elements", "steps"]
FIELDS_TO_REMOVE = ["status", "step_type"]


def convert(json_file, remove_background=False, duration_format=False, deduplicate=False) -> list:
    def format_level(tree, index=0, id_counter=itertools.count()):
        for item in tree:
            uri, line_number = item.pop("location").split(":")
            item["line"] = int(line_number)
            for field in FIELDS_TO_REMOVE:
                item.pop(field, None)

            if "tags" in item:
                item["tags"] = [
                    {"name": f"{tag}", "line": item["line"] - 1} for tag in item["tags"]
                ]

            if JSON_NODES[index] == "steps":
                item.setdefault("result", {"status": "skipped", "duration": 0})
                result = item.get("result", {})
                if "error_message" in result:
                    result["error_message"] = (
                        str(result.pop("error_message")).replace('"', "").replace("\\'", "")[:2000]
                    )
                if "duration" in result and duration_format:
                    result["duration"] = int(result["duration"] * 1_000_000_000)
                if "table" in item:
                    item["rows"] = [
                        {"cells": item["table"]["headings"], "line": item["line"] + 1}
                    ] + [
                        {"cells": row, "line": item["line"] + idx + 2}
                        for idx, row in enumerate(item["table"]["rows"])
                    ]
            else:
                item.update({"uri": uri, "description": "", "id": next(id_counter)})

            if index != 2 and JSON_NODES[index + 1] in item:
                item[JSON_NODES[index + 1]] = format_level(
                    item[JSON_NODES[index + 1]], index + 1, id_counter
                )
        return tree

    if remove_background:
        for feature in json_file:
            if feature["elements"][0].get("type") == "background":
                feature["elements"].pop(0)

    if deduplicate:
        for feature in json_file:
            scenarios = []
            for scenario in feature["elements"]:
                if not (len(scenarios) > 1 and scenarios[-1] == scenario):
                    scenarios.append(scenario)
            feature["elements"] = scenarios

    return format_level(json_file)
