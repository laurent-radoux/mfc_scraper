#!/usr/bin/env python

"""Tests for `mfc_scraper` package."""

import pytest

from click.testing import CliRunner

from mfc_scraper import scraper
from mfc_scraper import __main__


@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(__main__.main)
    assert result.exit_code == 0
    assert 'mfc_scraper.cli.main' in result.output
    help_result = runner.invoke(__main__.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
