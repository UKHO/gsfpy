import shutil
from dataclasses import dataclass
from enum import Enum, auto
from pathlib import Path

import pytest
from pytest_cases import fixture_union


class GsfVersion(Enum):
    V03_06 = auto()
    V03_07 = auto()


@dataclass(frozen=True)
class GsfDatafile:
    gsf_version: GsfVersion
    path: Path
    num_beams: int


GSF_03_06_DATAFILE = GsfDatafile(
    GsfVersion.V03_06,
    Path(__file__).parent / "0029_20160323_185603_EX1604_MB.gsf.mb121",
    num_beams=432,
)

GSF_03_07_DATAFILE = GsfDatafile(
    GsfVersion.V03_07,
    Path(__file__).parent / "0059_20181102_212138_EX1811_MB_EM302.gsf.mb121",
    num_beams=432,
)


def _setup_gsf_test_data(src_datafile: GsfDatafile, tmp_path: Path):
    tmp_path.mkdir(parents=True, exist_ok=True)
    tmp_datafile_path = tmp_path / src_datafile.path.name
    shutil.copyfile(src_datafile.path, tmp_datafile_path)
    yield GsfDatafile(
        src_datafile.gsf_version, tmp_datafile_path, src_datafile.num_beams
    )
    shutil.rmtree(tmp_path, ignore_errors=True)


@pytest.fixture
def gsf_test_data_03_06(tmp_path):
    yield from _setup_gsf_test_data(GSF_03_06_DATAFILE, tmp_path)


@pytest.fixture
def gsf_test_data_03_07(tmp_path):
    yield from _setup_gsf_test_data(GSF_03_07_DATAFILE, tmp_path)


fixture_union("gsf_test_data", [gsf_test_data_03_06, gsf_test_data_03_07])


@pytest.fixture(params=[GSF_03_06_DATAFILE, GSF_03_07_DATAFILE])
def gsf_test_data(request, tmp_path):
    src_datafile: GsfDatafile = request.param
    yield from _setup_gsf_test_data(src_datafile, tmp_path)
