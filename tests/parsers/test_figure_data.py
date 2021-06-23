from collections import namedtuple
from datetime import date

import pytest
from bs4 import BeautifulSoup

from mfc_scraper.parsers.figure_data import FigureDataParser

Params = namedtuple("Params", ("id",))
ExpectedValues = namedtuple("ExpectedValues",
                            ("id", "origin", "characters", "companies", "classifications",
                             "version", "release_date", "image_urls"))
FixtureParams = namedtuple("FixtureParams", ("params", "expected_values"))


def param_name(param: FixtureParams) -> str:
    return str(param.params)


@pytest.fixture(params=[
    FixtureParams(
        Params(688720),
        ExpectedValues(
                    688720,
                    "Dragon Ball Super",
                    ["Son Goku Migatte no Goku'i"],
                    ['Banpresto'],
                    ['Grandista', 'Grandista -Resolution of Soldiers-'],
                    "Overseas Version",
                    date(2018, 7, 1),
                    ['https://static.myfigurecollection.net/pics/figure/big/688720.jpg?rev=1537555368'],
        )
    )
], ids=param_name)
def figure_params(request) -> FixtureParams:
    return request.param


@pytest.fixture
def figure_data_parser(figure_params) -> FigureDataParser:
    with open(f"tests/resources/figure_{figure_params.params.id}_page.html", "rb") as input_file:
        yield FigureDataParser(figure_params.params.id, BeautifulSoup(input_file.read(), "html.parser"))


def test_figure_data_parser(figure_data_parser, figure_params):
    assert figure_data_parser.id == figure_params.expected_values.id
    assert figure_data_parser.origin == figure_params.expected_values.origin
    assert figure_data_parser.characters == figure_params.expected_values.characters
    assert figure_data_parser.companies == figure_params.expected_values.companies
    assert figure_data_parser.classifications == figure_params.expected_values.classifications
    assert figure_data_parser.version == figure_params.expected_values.version
    assert figure_data_parser.release_date == figure_params.expected_values.release_date
    assert figure_data_parser.image_urls == figure_params.expected_values.image_urls
