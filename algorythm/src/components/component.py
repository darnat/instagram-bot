import instana
import time


class Component(object):
    """
    Component Parent class
    """
    def __init__(self, instana):
        """
        Initialize Component object
        """
        self._instana = instana
        self._last_action = 0
        self._action_interval = 24 * 60 * 60

    def able_to(self):
        """
        Check if the action is able to be done
        """
        current = time.time()
        if current >= (self._last_action + self._action_interval):
            self._last_action = current
            return True
        return False

    def run(self):
        """
        Run the process
        """
        pass
