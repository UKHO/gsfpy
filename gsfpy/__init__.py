__author__ = """UK Hydrographic Office"""
__email__ = "datascienceandengineering@ukho.gov.uk"
__version__ = "2.0.0"

import os


def get_default_gsf_version() -> str:
    """
    get_default_gsf_version() retrieves the default GSF version to use from the
    environment, defaulting to v3.08 for backwards compatibility with older versions
    of gsfpy.

        Returns: str - The default GSF version in the form "X_XX" e.g. "3_09"
    """
    return os.environ.get("DEFAULT_GSF_VERSION", "3.08").replace(".", "_")


def mirror_default_gsf_version_submodule(
    globals_dict: dict, submodule_name: str = None
):
    """
    mirror_default_gsf_version_submodule() mirrors (via import) the version-specific
    module (from the appropriate gsfpyX_XX namespace) corresponding to the module from
    where it is called.

    E.g. when run from a module located at gsfpy/enums.py, it will mirror the
    gsfpyX_XX.enums module, to allow all members of that module to be accessed via
    gsfpy.enums.

    Params:
        globals_dict: the dictionary of globals pertaining to the calling module. This
                      can be obtained with a call to globals(). This is required as the
                      globals dictionary is updated by the call to the function.
        submodule_name: The name of the submodule to mirror from the gsfpyX_XX
                        namespace. If left empty, the top level gsfpyX_XX module will be
                        mirrored.
    """

    # Get the submodule name in the form gsfpyX_XX.submodule_name
    gsf_submodule_name = ".".join(
        filter(None, [f"gsfpy{get_default_gsf_version()}", submodule_name])
    )

    gsf_submodule = __import__(gsf_submodule_name, globals_dict, None, ["*"], 0)

    # The special attribute __all__ is a list of public members of the module, as
    # interpreted by import *. The globals collection must be updated with these
    # names to correctly mirror the submodule.
    if hasattr(gsf_submodule, "__all__"):
        globals_dict.update(
            (name, getattr(gsf_submodule, name)) for name in gsf_submodule.__all__
        )
    else:
        # In cases where there is no "__all__" perform the equivalent by importing
        # all non-private members (i.e. those that do not start with an underscore).
        globals_dict.update(
            (name, getattr(gsf_submodule, name))
            for name in dir(gsf_submodule)
            if not name.startswith("_")
        )


mirror_default_gsf_version_submodule(globals())
