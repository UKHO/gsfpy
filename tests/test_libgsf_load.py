from os import environ, path
from unittest import TestCase


class test_libgsf_load(TestCase):
    def test_libgsf_load_fails_with_incorrect_path(self):
        # Arrange
        environ["GSFPY_GSFLIB_PATH"] = "/does/not/exist"
        expected_errmsg = f"""Cannot load shared library from
            {environ["GSFPY_GSFLIB_PATH"]}. Set the $GSFPY_GSFLIB_PATH
            environment variable to the correct path, or remove
            it from the environment to use the default version."""

        # Act
        with self.assertRaises(Exception) as context:
            import_gsfpy()

            # Assert
            self.assertTrue(expected_errmsg in context.exception)

    def test_libgsf_load_succeeds_with_valid_path(self):
        # Arrange
        environ["GSFPY_GSFLIB_PATH"] = path.join(
            path.abspath(path.dirname(__file__)), "libgsf/libgsf03-09.so"
        )

        # Act
        try:
            import_gsfpy()
        except Exception:
            # Assert
            self.fail("Exception raised unexpectedly when importing gsfpy")

    def test_libgsf_load_succeeds_with_no_path(self):
        # Arrange
        del environ["GSFPY_GSFLIB_PATH"]

        # Act
        try:
            import_gsfpy()
        except Exception:
            # Assert
            self.fail("Exception raised unexpectedly when importing gsfpy")


def import_gsfpy():
    import gsfpy  # noqa
