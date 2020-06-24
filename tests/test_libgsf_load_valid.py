import os
from importlib import reload

from pytest import fail


def test_libgsf_load_succeeds_with_valid_path(mocker):
    try:
        # Arrange
        mocker.patch.dict(
            os.environ,
            {
                "GSFPY_LIBGSF_PATH": os.path.join(
                    os.path.abspath(os.path.dirname(__file__)), "libgsf/libgsf03-09.so"
                )
            },
        )

        # Act
        import gsfpy  # noqa

        reload(gsfpy)

    except Exception:
        # Assert
        fail("Exception raised unexpectedly when importing gsfpy: {ex}")
