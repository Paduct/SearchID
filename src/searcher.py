# coding: utf-8
# Copyright 2017

"""
Self-contained module.

Is a console application, to search id in the logs of the directory.

"""

from argparse import ArgumentParser, Namespace
from glob import glob
from linecache import getline
from os import path
from sys import stderr, stdout
from typing import List


class Searcher():

    """Search algorithm."""

    DEFAULT_INTERVAL: int = 10
    DESCRIPTION: str = "Search id in logs."
    DIRECTORY_NOT_EXIST_STR: str = "directory doesn't exist"
    INVALID_INT_VALUE_STR: str = "invalid int value"
    LOGS_ARE_MISSING_STR: str = "logs are missing"
    TWO_BLANK_LINES_STR: str = "\t{0}: {1!r}\n"
    NOT_FOUND_STR: str = "Not found\n"
    CATALOG_STR: str = "catalog"
    ERRORS_STR: str = "Errors:\n"
    IDENT_STR: str = "ident"
    LOG_STR: str = "log"

    log: str
    ident: str
    inter: int
    catalog: str
    red: str = '{0}'
    blue: str = '{0}'
    green: str = '{0}'

    def search_id(self) -> List[List[str]]:
        """Return a list of results or errors."""
        logs: List[str] = glob(path.join(self.catalog, self.log))
        results: List[List[str]] = []

        self.check_parameter(logs, results)
        if not results:
            self.search(logs, results)
            if not results:
                results.append(['', self.NOT_FOUND_STR])

        return results

    def check_parameter(self, logs: List[str], results: List[List[str]]):
        """Input parameter check."""
        result: List[str] = ['', self.ERRORS_STR]

        if not path.isdir(self.catalog):
            result.append(self.TWO_BLANK_LINES_STR.format(
                self.DIRECTORY_NOT_EXIST_STR, self.catalog
            ))
        if not logs:
            result.append(self.TWO_BLANK_LINES_STR.format(
                self.LOGS_ARE_MISSING_STR, self.log
            ))
        if not self.ident.isdigit():
            result.append(self.TWO_BLANK_LINES_STR.format(
                self.INVALID_INT_VALUE_STR, self.ident
            ))

        if len(result) > 2:
            results.append(result)

    def search(self, logs: List[str], results: List[List[str]]):
        """Search id in logs."""
        for log in logs:
            if path.isfile(log):
                try:
                    with open(log, 'r') as document:
                        for i, line in enumerate(document):
                            if self.ident in line:
                                results.append(['', f"{log} (line {i+1})\n"])
                                for j in range(i - 99, i + 102):
                                    if j == i + 1:
                                        results[-1][0] = str(len(results[-1]))
                                    results[-1].append(getline(log, j))
                except (OSError, UnicodeDecodeError) as error:
                    stderr.write(f"{error}\n")

    def search_results_form(self) -> str:
        """Return completed print form."""
        string: str = ''
        results: List[List[str]] = self.search_id()

        if results[0][0].isdigit():
            for result in results:
                result_index: int = int(result[0])
                start: int = result_index - self.inter
                start = 2 if start < 2 else start
                end: int = result_index + self.inter + 1

                result[result_index] = self.green.format(result[result_index])
                string = "{0}{1}{2}".format(string,
                                            self.blue.format(result[1]),
                                            ''.join(result[start:end]))
        else:
            string = self.red.format(''.join(results[0][1:]))

        return string


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser(description=Searcher.DESCRIPTION)
    parser.add_argument(Searcher.CATALOG_STR, type=str,
                        help="directory to search")
    parser.add_argument(Searcher.LOG_STR, type=str, help="file mask")
    parser.add_argument(Searcher.IDENT_STR, type=str, help="required number")
    parser.add_argument("-c", dest="colors", help="turn color design",
                        action="store_true")
    parser.add_argument("-i", dest="inter", help="scatter of lines", type=int,
                        const=Searcher.DEFAULT_INTERVAL, nargs='?',
                        metavar='I', default=Searcher.DEFAULT_INTERVAL)

    args: Namespace = parser.parse_args()
    Searcher.log = args.log
    Searcher.inter = args.inter
    Searcher.ident = args.ident
    Searcher.catalog = args.catalog

    if args.colors:
        Searcher.red = "\x1b[31;1m{0}\x1b[0m"
        Searcher.blue = "\x1b[34;1m{0}\x1b[0m"
        Searcher.green = "\x1b[32;1m{0}\x1b[0m"

    stdout.write(Searcher().search_results_form())
