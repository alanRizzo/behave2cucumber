import json
import logging
import pathlib
import sys
from pprint import pprint

import click

from pepyno.constants import NAME, VERSION
from pepyno.logger import setup_logging
from pepyno.tools import process_file


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(version=f"v{VERSION} 🥒", package_name=NAME)
@click.option(
    "--debug",
    "-d",
    type=click.IntRange(0, 5),
    default=0,
    help="Set debug level (0-5, where 5 is most verbose)",
)
@click.option(
    "--infile",
    "-i",
    type=click.Path(exists=True, path_type=pathlib.Path),
    required=True,
    help="Specify the input JSON file",
)
@click.option(
    "--outfile",
    "-o",
    type=click.Path(path_type=pathlib.Path),
    help="Specify the output JSON file, otherwise use stdout",
)
@click.option(
    "--remove-background",
    "-r",
    is_flag=True,
    help="Remove background steps from output",
)
@click.option("--format-duration", "-f", is_flag=True, help="Format the duration values")
@click.option(
    "--deduplicate",
    "-D",
    is_flag=True,
    help="Remove duplicate scenarios caused by @autoretry",
)
@click.option("--pretty", is_flag=True, help="Pretty-print the JSON output")
@click.option(
    "--log-dir",
    type=click.Path(file_okay=False, path_type=pathlib.Path),
    default="./",
    help="Directory to store log files",
)
def main(
    debug,
    infile,
    outfile,
    remove_background,
    format_duration,
    deduplicate,
    pretty,
    log_dir,
):
    log_level = 50 - (debug * 10)
    log = setup_logging(log_level, log_dir)

    log.info("Log level set to: %s", logging.getLevelName(log_level))
    log.debug("Arguments received: %s", locals())

    try:
        result = process_file(
            log,
            infile,
            outfile,
            remove_background,
            format_duration,
            deduplicate,
            pretty,
        )

        if not outfile:
            if pretty:
                print(json.dumps(result, indent=4, ensure_ascii=False))
            else:
                pprint(result)

    except KeyboardInterrupt:
        log.warning("Operation interrupted by user")
        sys.exit(130)
    except Exception as e:
        log.critical("Unhandled error: %s", e, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
