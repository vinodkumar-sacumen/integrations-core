# (C) Datadog, Inc. 2025-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from datadog_checks.base.constants import ServiceCheck
from datadog_checks.dev.utils import assert_service_checks


def test_check_falco_e2e(dd_agent_check, instance):
    aggregator = dd_agent_check(instance, rate=True)
    aggregator.assert_service_check('falco.openmetrics.health', ServiceCheck.OK, count=2)
    assert_service_checks(aggregator)
