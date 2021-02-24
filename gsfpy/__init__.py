__author__ = """UK Hydrographic Office"""
__email__ = "datascienceandengineering@ukho.gov.uk"
__version__ = "2.0.0"

import os

# Get GSF version to use from environment. Default to GSF v3.08 for backwards
# compatibility with older versions of gsfpy.
if "DEFAULT_GSF_VERSION" in os.environ and os.environ["DEFAULT_GSF_VERSION"] == "3.09":
    from gsfpy3_09 import *  # noqa
else:
    from gsfpy3_08 import *  # type: ignore
