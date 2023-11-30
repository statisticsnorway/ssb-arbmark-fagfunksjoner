"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """SSB Arbeidsmarked og lønn Fag-fellesfunksjoner."""


if __name__ == "__main__":
    main(prog_name="ssb-arbmark-fagfunksjoner")  # pragma: no cover
