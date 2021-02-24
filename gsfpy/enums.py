from gsfpy import GSF_V03_09, get_default_gsf_version

if get_default_gsf_version() == GSF_V03_09:
    from gsfpy3_09.enums import *  # noqa
else:
    from gsfpy3_08.enums import *  # type: ignore
