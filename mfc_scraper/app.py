"""Console script for mfc_scraper."""
import json
import os
import sys
import click

from mfc_scraper import scraper


@click.command()
def main(args=None):
    figures_data = scraper.get_figures_data(scraper.get_all_figures("Nightzus"))

    figures_filepath = "output/figures.json"
    os.makedirs(os.path.dirname(figures_filepath), exist_ok=True)
    with open(figures_filepath, "w") as data_file:
        json.dump(figures_data, data_file)

    scraper.dump_all_images(figures_data)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
