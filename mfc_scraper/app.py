"""Console script for mfc_scraper."""
import json
import sys
import click
import os
import shutil

from mfc_scraper import scraper


@click.command()
@click.option("-u", "--username", required=True)
@click.option("-o", "--output-folder", default="output")
@click.option("--new-only/--all", default=True)
@click.option("--images/--no-images", default=True)
def dump_collection(username, output_folder, new_only, images):
    output_folder = f"{output_folder}/{username}"
    figures_filepath = f"{output_folder}/figures.json"

    all_figures = scraper.get_all_figures(username)
    already_dumped_figures = []
    if new_only:
        with open(figures_filepath, "r") as data_file:
            already_dumped_figures = json.load(data_file)

    figures_to_load = [f for f in all_figures if f not in [f["id"] for f in already_dumped_figures]]
    new_figures_data = scraper.get_figures_data(figures_to_load)
    figures_data = already_dumped_figures + new_figures_data

    os.makedirs(os.path.dirname(figures_filepath), exist_ok=True)
    with open(figures_filepath, "w") as data_file:
        json.dump(figures_data, data_file, indent=3)

    if images:
        for image_data in scraper.get_all_images(new_figures_data):
            images_filepath = f"{output_folder}/images/{image_data['id']}_{{}}.jpg"
            for i, data in enumerate(image_data["images"]):
                image_filepath = images_filepath.format(i)
                os.makedirs(os.path.dirname(image_filepath), exist_ok=True)
                with open(image_filepath, "wb") as data_file:
                    shutil.copyfileobj(data, data_file)

    return 0


if __name__ == "__main__":
    sys.exit(dump_collection())  # pragma: no cover
