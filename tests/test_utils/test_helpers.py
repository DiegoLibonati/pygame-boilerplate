import os
import sys
from unittest.mock import patch

import pytest

from src.utils.helpers import resource_path


class TestResourcePath:
    @pytest.mark.unit
    def test_returns_string(self) -> None:
        result: str = resource_path("some/path.png")
        assert isinstance(result, str)

    @pytest.mark.unit
    def test_path_contains_relative_path(self) -> None:
        result: str = resource_path("assets/image.png")
        assert "assets" in result and "image.png" in result

    @pytest.mark.unit
    def test_unbundled_uses_abspath(self) -> None:
        expected: str = os.path.join(os.path.abspath("."), "assets/image.png")
        result: str = resource_path("assets/image.png")
        assert result == expected

    @pytest.mark.unit
    def test_bundled_uses_meipass(self) -> None:
        meipass: str = "/tmp/bundle"
        with patch.object(sys, "_MEIPASS", meipass, create=True):
            result: str = resource_path("assets/image.png")
        expected: str = os.path.join(meipass, "assets/image.png")
        assert result == expected

    @pytest.mark.unit
    def test_empty_relative_path_returns_base(self) -> None:
        result: str = resource_path("")
        assert os.path.normpath(result) == os.path.abspath(".")

    @pytest.mark.unit
    def test_nested_path_segments(self) -> None:
        result: str = resource_path("a/b/c/d.txt")
        assert os.path.normpath(result).endswith(os.path.join("a", "b", "c", "d.txt"))

    @pytest.mark.unit
    def test_bundled_path_does_not_include_cwd(self) -> None:
        meipass: str = "/bundle/path"
        with patch.object(sys, "_MEIPASS", meipass, create=True):
            result: str = resource_path("data/file.json")
        assert result.startswith(meipass)
        assert os.path.abspath(".") not in result
