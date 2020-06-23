import os
from importlib import reload

import mock
from assertpy import assert_that
from pytest import fail, raises


@mock.patch.dict(os.environ, {"GSFPY_LIBGSF_PATH": "/does/not/exist"})
def test_libgsf_load_fails_with_incorrect_path():
    # Arrange test data
    with raises(Exception) as context:
        expected_errmsg_start = "Cannot load shared library"

        # Act
        import gsfpy  # noqa

        reload(gsfpy)

    # Assert
    assert_that(str(context.value)).starts_with(expected_errmsg_start)


@mock.patch.dict(os.environ, {})
def test_libgsf_load_succeeds_with_no_path():
    try:
        # Act
        import gsfpy  # noqa

        reload(gsfpy)

    except Exception:
        # Assert
        fail("Exception raised unexpectedly when importing gsfpy: {ex}")


@mock.patch.dict(
    os.environ,
    {
        "GSFPY_LIBGSF_PATH": os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "libgsf/libgsf03-09.so"
        )
    },
)
def test_libgsf_load_succeeds_with_valid_path():
    try:
        # Act
        import gsfpy  # noqa

        reload(gsfpy)

    except Exception:
        # Assert
        fail("Exception raised unexpectedly when importing gsfpy: {ex}")
