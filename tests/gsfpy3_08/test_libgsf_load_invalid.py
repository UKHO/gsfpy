import os
from importlib import reload

from assertpy import assert_that
from pytest import raises


def test_libgsf_load_fails_with_incorrect_path(mocker):
    # Arrange
    with raises(Exception) as context:
        mocker.patch.dict(os.environ, {"GSFPY3_08_LIBGSF_PATH": "/does/not/exist"})
        expected_errmsg_start = "Cannot load shared library"

        # Act
        import gsfpy3_08  # noqa

        reload(gsfpy3_08)

    # Assert
    assert_that(str(context.value)).starts_with(expected_errmsg_start)
