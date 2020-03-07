# coding: utf-8
# Copyright 2017

"""Implementing the graphical interface for the module searcher."""

from glob import glob
from os import path
from sys import stderr
from typing import Callable, List

from kivy.app import App
from kivy.core.window import Window
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.utils import escape_markup
from pygments.lexer import RegexLexer, words
from pygments.token import Generic
from widgetskv import WKV_ALL_FILES

from .searcher import Searcher


class Gui(App):

    """Class of the main window and runing of the application."""

    searcher: Searcher = Searcher()
    title: str = "Search ID"
    version: str = "0.1.0"
    create_year: int = 2017
    project_link: str = "https://github.com/Paduct/search_id"
    license_link: str = "https://www.gnu.org/licenses/gpl-3.0"
    description: str = searcher.DESCRIPTION
    marker: int = 1
    results: List[List[str]] = [['']]

    COLORED_STR: str = "colored"
    RESULT_STR: str = "result {0} of {1}"
    INTERVAL_STR: str = "scatter lines interval {0}"
    GREEN_COLORED_STR: str = f"[color=#00ff00]{COLORED_STR}[/color]"
    RED_NOT_COLORED_STR: str = f"[color=#ff0000]not {COLORED_STR}[/color]"

    def build(self):
        """Accumulate of resources and the start of the main window."""
        project_path: str = path.split(path.dirname(__file__))[0]
        kv_files_path: str = path.join(project_path, "uix", "*.kv")
        kv_file_names: List[str] = glob(kv_files_path)
        kv_file_names.extend(WKV_ALL_FILES)

        for file_name in kv_file_names:
            Builder.load_file(file_name)

        Window.clearcolor = (0.2, 0.2, 0.2, 1)
        setattr(RegexLexer, "_tokens", None)
        self.icon = path.join(project_path, "data", "magnify.png")
        self.root = Factory.RootWindow()

    def find(self):
        """Implement find button."""
        self.searcher.log = self.root.ids.log.text
        self.searcher.ident = self.root.ids.ident.text
        self.searcher.catalog = self.root.ids.catalog.text
        self.searcher.inter = int(self.root.ids.inter.value)
        self.results = self.searcher.search_id()

        self.marker = 1
        self.colored()
        self.show_interval()

    def colored(self):
        """Implement switch colored."""
        if self.root.ids.colors.active:
            if self.results[0][0].isdigit():
                result_index: int = int(self.results[self.marker - 1][0])
                RegexLexer.tokens = {"root": [
                    (words({escape_markup(
                        f"{self.results[self.marker - 1][1]}"
                    )}), Generic.Heading),
                    (words({escape_markup(
                        f"{self.results[self.marker - 1][result_index]}"
                    )}), Generic.Inserted)
                ]}
            else:
                RegexLexer.tokens = {"root": [(r"^.+$", Generic.Error)]}
            self.root.ids.s_color.text = self.GREEN_COLORED_STR
        else:
            RegexLexer.tokens = {"root": []}
            self.root.ids.s_color.text = self.RED_NOT_COLORED_STR

        delattr(RegexLexer, "_tokens")
        self.root.ids.view.lexer = RegexLexer()

    def show_interval(self):
        """Implement slider interval."""
        self.root.ids.view.text = self.result_string()
        self.root.ids.s_inter.text = \
            self.INTERVAL_STR.format(int(self.root.ids.inter.value))
        self.root.ids.s_result.text = self.RESULT_STR.format(self.marker,
                                                             len(self.results))

    def change_result(self, trend: bool):
        """Implement of buttons back and forth according to the results."""
        if self.marker > 1 and not trend:
            self.marker -= 1
        elif self.marker < len(self.results) and trend:
            self.marker += 1

        self.colored()
        self.show_interval()

    def result_string(
            self, markup_escape: Callable[[str], str] = escape_markup
    ) -> str:
        """Return the result of generating a string."""
        string_result: str

        if self.results[0][0].isdigit():
            result_index: int = int(self.results[self.marker - 1][0])
            start: int = result_index - int(self.root.ids.inter.value)
            start = 2 if start < 2 else start
            end: int = result_index + int(self.root.ids.inter.value) + 1

            string_result = ''.join((
                markup_escape(self.results[self.marker - 1][1]),
                ''.join(self.results[self.marker - 1][start:result_index]),
                markup_escape(self.results[self.marker - 1][result_index]),
                ''.join(self.results[self.marker - 1][result_index + 1:end]),
            ))
        else:
            string_result = ''.join(self.results[0][1:])

        return string_result

    def impl_path_chooser(self, path_file: str):
        """Implement menu - save the current result to a file."""
        try:
            with open(path_file, 'a') as log:
                log.write(self.result_string(markup_escape=lambda s: s))
                log.write('\n')
                log.flush()
        except OSError as error:
            stderr.write(f"{error}\n")

    def on_pause(self) -> bool:
        """Return the sign of switching to pause mode."""
        return True
