# coding: utf-8
# Copyright 2017

"""Module for testing search algorithm."""

from os import path
from unittest import TestCase, TestLoader, TestSuite

from searcher import Searcher


class TestSearcher(TestCase):

    """Search algorithm testing."""

    def test_search_id(self):
        """Testing list of results or errors."""
        Searcher.log = "__i*.py"
        Searcher.inter = 10
        Searcher.ident = "800"
        Searcher.catalog = '.'

        self.assertEqual(Searcher().search_results_form(), (
            "{0} (line 8)\n"
            "# coding: utf-8\n"
            "# Copyright 2017\n\n"
            "\"\"\"Initialization.\"\"\"\n\n"
            "from kivy.config import Config\n\n"
            "Config.set(\"graphics\", \"width\", \"{1}\")\n"
            "Config.set(\"graphics\", \"height\", \"{1}\")\n"

            "{0} (line 9)\n"
            "# coding: utf-8\n"
            "# Copyright 2017\n\n"
            "\"\"\"Initialization.\"\"\"\n\n"
            "from kivy.config import Config\n\n"
            "Config.set(\"graphics\", \"width\", \"{1}\")\n"
            "Config.set(\"graphics\", \"height\", \"{1}\")\n"
        ).format(path.join(Searcher.catalog, "__init__.py"), Searcher.ident))


def suite() -> TestSuite:
    """Return a test suite for execution."""
    tests: TestSuite = TestSuite()
    loader: TestLoader = TestLoader()
    tests.addTest(loader.loadTestsFromTestCase(TestSearcher))
    return tests
