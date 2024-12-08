import subprocess
import traceback
from threading import Thread, Event

from nixos_updatechecker.config import APP_CONFIG
from nixos_updatechecker.core import get_changes
from nixos_updatechecker.indicator import UpdateCheckIndicator


class UpdateCheckController:
    def __init__(self, indicator: UpdateCheckIndicator):
        self.indicator = indicator
        self.recheck_ev = Event()

        self.indicator.recheck_ev = self.recheck_ev

    def mainloop(self):
        while True:
            # Pending
            self.indicator.show_status([], True)

            # Result
            try:
                self.indicator.show_status(get_changes(), False)
            except subprocess.CalledProcessError:
                traceback.print_exc()
                self.indicator.show_status([], False)

            # Delay
            self.recheck_ev.clear()
            self.recheck_ev.wait(timeout=APP_CONFIG["recheck-interval"])

    @staticmethod
    def start(indicator: UpdateCheckIndicator):
        obj = UpdateCheckController(indicator)
        thread = Thread(name="control_mainloop", target=obj.mainloop)
        thread.daemon = True
        thread.start()
        return obj
