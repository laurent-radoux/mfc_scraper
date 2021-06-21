"""Console script for mfc_scraper."""
import json
import os
import sys
import click
import os
import shutil

from mfc_scraper import scraper


@click.command()
def dump_collection(args=None):
    figures_data = scraper.get_figures_data(scraper.get_all_figures("Nightzus")[:4])

    figures_filepath = "output/figures.json"
    os.makedirs(os.path.dirname(figures_filepath), exist_ok=True)
    with open(figures_filepath, "w") as data_file:
        json.dump(figures_data, data_file, indent=3)

    for image_data in scraper.get_all_images(figures_data):
        images_filepath = "output/images/{}_{{}}.jpg".format(image_data['id'])
        for i, data in enumerate(image_data["images"]):
            image_filepath = images_filepath.format(i)
            os.makedirs(os.path.dirname(image_filepath), exist_ok=True)
            with open(image_filepath, "wb") as data_file:
                shutil.copyfileobj(data, data_file)

    return 0


if __name__ == "__main__":
    sys.exit(dump_collection())  # pragma: no cover
