"""Console script for mfc_scraper."""
import sys
import click

from mfc_scraper import dumper


@click.command()
@click.option("-u", "--username", required=True)
@click.option("-o", "--output-folder", default="output")
@click.option("--new-only/--all", default=True)
@click.option("--images/--no-images", default=True)
def main(username, output_folder, new_only, images):
    dumper.dump_collection(username, output_folder, new_only, images)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
