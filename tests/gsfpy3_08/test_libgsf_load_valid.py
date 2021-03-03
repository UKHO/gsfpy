import os
from importlib import reload

from pytest import fail


def test_libgsf_load_succeeds_with_valid_path(mocker):
    try:
        # Arrange
        mocker.patch.dict(
            os.environ,
            {
                "GSFPY3_08_LIBGSF_PATH": os.path.join(
                    os.path.abspath(os.path.dirname(__file__)), "libgsf/libgsf03-08.so"
                )
            },
        )

        # Act
        import gsfpy3_08  # noqa

        reload(gsfpy3_08)

    except Exception:
        # Assert
        fail("Exception raised unexpectedly when importing gsfpy3_08: {ex}")
