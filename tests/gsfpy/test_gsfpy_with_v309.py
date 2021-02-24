import os
import tempfile
from ctypes import c_int, create_string_buffer, string_at
from importlib import reload
from os import path

from assertpy import assert_that
from pytest import fail


def test_correct_gsf_version_when_set_via_env(mocker, gsf_test_data_03_09):
    try:
        # Arrange
        mocker.patch.dict(
            os.environ,
            {
                "DEFAULT_GSF_VERSION": "3.09"
            },
        )

        # Act
        import gsfpy

        reload(gsfpy)

        # Check that we can open a v3.09 file successfully
        with gsfpy.open_gsf(gsf_test_data_03_09.path) as _:
            pass

        # Assert that trying to open a non-existent file gives us a GSF v3.09-specific
        # error message (note the different wording from the v3.08 error message).
        assert_that(gsfpy.open_gsf).raises(gsfpy.GsfException).when_called_with(
            "non-existent.gsf"
        ).is_equal_to("[-1] GSF Error: Unable to open requested file")

    except Exception:
        # Assert
        fail("Exception raised unexpectedly when importing gsfpy: {ex}")
