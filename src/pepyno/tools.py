import json
import time
from datetime import datetime
from logging import Logger
from pathlib import Path

from pepyno.constants import NAME, VERSION
from pepyno.converter import convert


def process_file(
    log: Logger,
    infile: Path,
    outfile: Path | None = None,
    remove_background: bool = False,
    duration_format: bool = False,
    deduplicate: bool = False,
    pretty: bool = False,
) -> list:
    """Process the input file and generate Cucumber-compatible output.

    Args:
        log: a Logger instance
        infile: Input JSON file path
        outfile: Output JSON file path (optional)
        remove_background: Whether to remove background steps
        duration_format: Whether to format duration values
        deduplicate: Whether to remove duplicate scenarios
        pretty: Whether to pretty-print the JSON output

    Returns:
        Processed JSON data
    """
    log.info(f"Processing file: {infile}")

    try:
        with open(infile, encoding="utf-8") as f:
            try:
                input_data = json.load(f)
            except json.JSONDecodeError as e:
                raise json.JSONDecodeError(f"Invalid JSON in {infile}: {str(e)}", e.doc, e.pos)

        # Process the data
        start_time = time.time()
        cucumber_output = convert(
            input_data,
            remove_background=remove_background,
            duration_format=duration_format,
            deduplicate=deduplicate,
        )
        log.info(f"Conversion completed in {time.time() - start_time:.2f} seconds")

        # Add metadata to the output
        if isinstance(cucumber_output, list) and cucumber_output:
            metadata = {
                "generated_by": f"{NAME} v{VERSION}",
                "timestamp": datetime.now().isoformat(),
                "source_file": str(infile),
            }
            for feature in cucumber_output:
                feature["metadata"] = metadata

        # Output the result
        if outfile:
            outfile.parent.mkdir(parents=True, exist_ok=True)
            with open(outfile, "w", encoding="utf-8") as f:
                indent = 4 if pretty else None
                json.dump(cucumber_output, f, indent=indent, ensure_ascii=False)
            log.info(f"Output written to: {outfile}")

        return cucumber_output

    except Exception as e:
        log.exception(f"Error processing file: {str(e)}")
        raise
