import pathlib

import click

from tools import _name, _version


def parse_args():
    """Parse command line arguments using click."""

    @click.command(context_settings={"help_option_names": ["-h", "--help"]})
    @click.version_option(version=f"{_name} v{_version}")
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
    @click.option(
        "--format-duration",
        "-f",
        is_flag=True,
        help="Format the duration values",
    )
    @click.option(
        "--deduplicate",
        "-D",
        is_flag=True,
        help="Remove duplicate scenarios caused by @autoretry",
    )
    @click.option(
        "--pretty",
        is_flag=True,
        help="Pretty-print the JSON output",
    )
    @click.option(
        "--log-dir",
        type=click.Path(file_okay=False, path_type=pathlib.Path),
        default="./",
        help="Directory to store log files",
    )
    def main(**kwargs):
        return kwargs

    return main()
