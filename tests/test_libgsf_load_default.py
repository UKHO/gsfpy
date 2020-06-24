import os
from importlib import reload

from pytest import fail


def test_libgsf_load_succeeds_with_no_path(mocker):
    try:
        # Arrange
        mocker.patch.dict(os.environ, {})

        # Act
        import gsfpy  # noqa

        reload(gsfpy)

    except Exception:
        # Assert
        fail("Exception raised unexpectedly when importing gsfpy: {ex}")
