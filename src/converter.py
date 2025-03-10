def convert(json_file, remove_background=False, duration_format=False, deduplicate=False):
    """
    Convert Behave JSON format to Cucumber JSON format.

    Args:
        json_file: The JSON data from Behave to be converted
        remove_background: Whether to remove background elements
        duration_format: Whether to format duration values
        deduplicate: Whether to remove duplicate scenarios

    Returns:
        The converted JSON data in Cucumber format
    """
    # json_nodes are the scopes available in behave/cucumber json:
    # Feature -> elements(Scenarios) -> Steps
    json_nodes = ["feature", "elements", "steps"]
    # These fields don't exist in cucumber report, therefore when
    # converting from behave, we need to delete them
    fields_not_exist_in_cucumber_json = ["status", "step_type"]

    def format_level(tree, index=0, id_counter=0):
        for item in tree:
            # Location in behave json translates to uri and line in cucumber json
            uri, line_number = item.pop("location").split(":")
            item["line"] = int(line_number)

            # Remove fields that don't exist in cucumber json
            for field in fields_not_exist_in_cucumber_json:
                item.pop(field, None)  # Using pop with default to avoid KeyError

            if "tags" in item:
                print(f"Before: {item['tags']}")
                item["tags"] = [
                    {"name": "@" + tag if tag.startswith("auto") else tag, "line": item["line"] - 1}
                    for tag in item["tags"]
                ]
                print(f"After: {item['tags']}")

            if json_nodes[index] == "steps":
                if "result" in item:
                    # Truncate long error messages to maximum 2000 chars
                    if "error_message" in item["result"]:
                        error_msg = item["result"].pop("error_message")
                        item["result"]["error_message"] = str(
                            str(error_msg).replace('"', "").replace("\\'", "")
                        )[:2000]

                    # Format duration if needed
                    if "duration" in item["result"] and duration_format:
                        item["result"]["duration"] = int(item["result"]["duration"] * 1_000_000_000)
                else:
                    # In behave, skipped tests don't have result object in their json
                    # For every skipped test we need to generate a new result with status skipped
                    item["result"] = {"status": "skipped", "duration": 0}

                # Convert table format
                if "table" in item:
                    item["rows"] = []
                    t_line = 1
                    item["rows"].append(
                        {"cells": item["table"]["headings"], "line": item["line"] + t_line}
                    )
                    for table_row in item["table"]["rows"]:
                        t_line += 1
                        item["rows"].append({"cells": table_row, "line": item["line"] + t_line})
            else:
                # uri is the name of the feature file the current item is located in
                item["uri"] = uri
                item["description"] = ""
                item["id"] = id_counter
                id_counter += 1

            # If the scope is not "steps" proceed with the recursion
            if index != 2 and json_nodes[index + 1] in item:
                item[json_nodes[index + 1]] = format_level(
                    item[json_nodes[index + 1]], index + 1, id_counter=id_counter
                )
        return tree

    # Option to remove background element because behave pushes its steps to all scenarios already
    if remove_background:
        for feature in json_file:
            if feature["elements"] and feature["elements"][0].get("type") == "background":
                feature["elements"].pop(0)

    if deduplicate:

        def check_dupe(current_feature, current_scenario, previous_scenario):
            """Check if the current scenario is a duplicate of the previous one."""
            # Skip deduplication if not marked with autoretry tag
            if not any(
                "autoretry" in (tag.get("name", "") if isinstance(tag, dict) else tag)
                for tags in [current_feature.get("tags", []), current_scenario.get("tags", [])]
                for tag in tags
            ):
                return False

            # Compare scenario attributes
            for attr in ["keyword", "location", "name", "tags", "type"]:
                if previous_scenario.get(attr) != current_scenario.get(attr):
                    return False

            return True

        for feature in json_file:
            # Create a working list
            scenarios = []

            # For each scenario in the feature
            for scenario in feature.get("elements", []):
                # Append the scenario to the working list
                scenarios.append(scenario)

                # Check if this is a duplicate of the previous scenario
                if len(scenarios) >= 2:
                    previous_scenario = scenarios[-2]
                    if check_dupe(feature, scenario, previous_scenario):
                        # Remove the earlier scenario from the working list
                        scenarios.pop(-2)

            # Replace the existing list with the working list
            feature["elements"] = scenarios

    # Begin the recursion
    return format_level(json_file)
