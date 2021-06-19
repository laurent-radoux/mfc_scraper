"""Main module."""

from typing import List
import os
import shutil
import requests
from tqdm import tqdm
import multiprocessing as mp

from mfc_scraper.pages.figure_collection_page import FigureCollectionPage, NoFiguresFound
from mfc_scraper.pages.figure_page import FigurePage


def get_all_figures() -> List[int]:
    base_url = "https://myfigurecollection.net/users.v4.php"
    url_parameters = {
        "username": "Nightzus",
        "mode": "view",
        "tab": "collection",
        "status": 2,
        "categoryId": -1,
        "sort": "category",
        "order": "asc",
    }
    all_figures = []
    current_page = 1
    with tqdm() as progress_bar:
        while True:
            page_content = requests.get(base_url
                                        + "?"
                                        + "&".join(f"{k}={v}" for k, v in url_parameters.items())
                                        + f"&page={current_page}"
                                        ).text
            try:
                all_figures += (f.id for f in FigureCollectionPage(page_content).figures)
                current_page += 1
                progress_bar.update()
            except NoFiguresFound:
                break

    return all_figures


def get_figure_data(figure_id: int):
    base_url = "https://myfigurecollection.net/item/"
    return FigurePage(figure_id, requests.get(f"{base_url}{figure_id}").text).data.to_dict()


def get_figures_data(figure_ids: List[int]):
    with mp.Pool(mp.cpu_count()) as pool:
        return list(tqdm(pool.imap(get_figure_data, figure_ids), total=len(figure_ids)))


def dump_image(url: str, local_filepath: str):
    response = requests.get(url, stream=True)
    os.makedirs(os.path.dirname(local_filepath), exist_ok=True)
    with open(local_filepath, "wb") as output_file:
        shutil.copyfileobj(response.raw, output_file)


def dump_all_images(figures_data: List):
    for f in figures_data:
        for i, u in enumerate(f["image_urls"]):
            dump_image(u, f"output/images/{f['id']}_{i}.jpg")
