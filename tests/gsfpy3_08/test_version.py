from pathlib import Path
from unittest import TestCase

import toml
from assertpy import assert_that

from gsfpy3_08 import __version__ as module_version


class TestVersion(TestCase):
    def test_version(self):
        pyproject_file = Path(__file__).parents[2] / "pyproject.toml"
        pyproject = toml.load(pyproject_file)
        pyproject_version = pyproject["tool"]["poetry"]["version"]

        assert_that(module_version).is_equal_to(pyproject_version)
