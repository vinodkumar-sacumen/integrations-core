# (C) Datadog, Inc. 2018-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
from . import AgentCheck


class Status:
    DOWN = "DOWN"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"
    UP = "UP"


class NetworkCheck(AgentCheck):
    """
    This class should never be directly instantiated.
    This class is deprecated, please make your checks inherit from the
    `AgentCheck` class directly.
    """

    STATUS_TO_SERVICE_CHECK = {
        Status.UP: AgentCheck.OK,
        Status.WARNING: AgentCheck.WARNING,
        Status.CRITICAL: AgentCheck.CRITICAL,
        Status.DOWN: AgentCheck.CRITICAL,
    }

    def __init__(self, *args, **kwargs):
        super(NetworkCheck, self).__init__(*args, **kwargs)
        self.warning("NetworkCheck is deprecated. Please inherit from AgentCheck instead")

    def check(self, instance):
        try:
            statuses = self._check(instance)
        except Exception:
            self.log.exception("Failed to run instance '%s'.", instance.get('name', ""))
        else:
            if isinstance(statuses, tuple):
                # Assume the check only returns one service check
                status, msg = statuses
                self.report_as_service_check(None, status, instance, msg)

            elif isinstance(statuses, list):
                for status in statuses:
                    sc_name, status, msg = status
                    self.report_as_service_check(sc_name, status, instance, msg)

    def _check(self, instance):
        """This function should be implemented by inherited classes"""
        raise NotImplementedError

    def report_as_service_check(self, sc_name, status, instance, msg=None):
        """This function should be implemented by inherited classes"""
        raise NotImplementedError


# Deprecated since we aren't reporting statuses as events anymore
# Keep the class here so that imports don't fail
class EventType:
    pass
