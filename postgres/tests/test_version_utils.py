# (C) Datadog, Inc. 2018-present
# All rights reserved
# Licensed under Simplified BSD License (see LICENSE)
import pytest
from semver import VersionInfo

from datadog_checks.postgres.version_utils import VersionUtils

pytestmark = pytest.mark.unit


def test_parse_version():
    """
    Test _get_version() to make sure the check is properly parsing Postgres versions
    """
    version = VersionUtils.parse_version('9.5.3')
    assert version == VersionInfo(9, 5, 3)

    # Test #.# style versions
    v10_2 = VersionUtils.parse_version('10.2')
    assert v10_2 == VersionInfo(10, 2, 0)

    v11 = VersionUtils.parse_version('11')
    assert v11 == VersionInfo(11, 0, 0)

    # Test #beta# style versions
    beta11 = VersionUtils.parse_version('11beta3')
    assert beta11 == VersionInfo(11, 0, 0, prerelease='beta.3')

    assert v10_2 < beta11
    assert v11 > beta11

    # Test #rc# style versions
    version = VersionUtils.parse_version('11rc1')
    assert version == VersionInfo(11, 0, 0, prerelease='rc.1')

    # Test #nightly# style versions
    version = VersionUtils.parse_version('11nightly3')
    assert version == VersionInfo(11, 0, 0, 'nightly.3')

    v12_3_tde = VersionUtils.parse_version('12.3_TDE_1.0')
    assert v12_3_tde == VersionInfo(12, 3, 0)


def test_throws_exception_for_unknown_version_format():
    with pytest.raises(Exception) as e:
        VersionUtils.parse_version('dontKnow')
    assert e.value.args[0] == "Cannot determine which version is dontKnow"


def test_transform_version():
    version = VersionUtils.transform_version('11beta4')
    expected = {
        'version.raw': '11beta4',
        'version.major': '11',
        'version.minor': '0',
        'version.patch': '0',
        'version.release': 'beta.4',
        'version.scheme': 'semver',
    }
    assert expected == version

    version = VersionUtils.transform_version('10.0')
    expected = {
        'version.raw': '10.0',
        'version.major': '10',
        'version.minor': '0',
        'version.patch': '0',
        'version.scheme': 'semver',
    }
    assert expected == version

    version = VersionUtils.transform_version('10.5.4')
    expected = {
        'version.raw': '10.5.4',
        'version.major': '10',
        'version.minor': '5',
        'version.patch': '4',
        'version.scheme': 'semver',
    }
    assert expected == version


def test_parse_rds_eol_version():
    version = '11.22-rds.20241121'
    v11_22_rds = VersionUtils.parse_version(version)

    assert v11_22_rds == VersionInfo(11, 22, 20241121)
