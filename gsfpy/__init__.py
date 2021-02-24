__author__ = """UK Hydrographic Office"""
__email__ = "datascienceandengineering@ukho.gov.uk"
__version__ = "2.0.0"

import os

GSF_V03_09 = "3.09"


def get_default_gsf_version() -> str:
    if "DEFAULT_GSF_VERSION" in os.environ:
        return os.environ["DEFAULT_GSF_VERSION"]
    else:
        return ""


# Get GSF version to use from environment. Default to GSF v3.08 for backwards
# compatibility with older versions of gsfpy.
if get_default_gsf_version() == GSF_V03_09:
    from gsfpy3_09 import *  # noqa
else:
    from gsfpy3_08 import *  # type: ignore
