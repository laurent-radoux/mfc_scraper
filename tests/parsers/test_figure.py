from collections import namedtuple

import pytest
from bs4 import BeautifulSoup

from mfc_scraper.parsers.figure import FigureParser


Params = namedtuple("Params", ("id",))
ExpectedValues = namedtuple("ExpectedValues", ("id", "name",))
FixtureParams = namedtuple("FixtureParams", ("params", "expected_values"))


def param_name(param: FixtureParams) -> str:
    return str(param.params)


@pytest.fixture(params=[
    FixtureParams(
        Params(2303),
        ExpectedValues(2303, "Dragon Ball Z - Cooler - Action Pose Figure (Banpresto)")
    )
], ids=param_name)
def figure_params(request) -> FixtureParams:
    return request.param


@pytest.fixture
def figure_parser(figure_params) -> FigureParser:
    with open(f"tests/resources/figure_{figure_params.params.id}_in_collection_page.html", "r") as input_file:
        yield FigureParser(BeautifulSoup(input_file.read(), "html.parser"))


def test_figure_parser(figure_parser, figure_params):
    assert figure_parser.id == figure_params.expected_values.id
    assert figure_parser.name == figure_params.expected_values.name
