
import queue
import threading


class TaskManager:

    def __init__(self):
        self.events = queue.Queue()
        self.busy = False
        self.closing = False

    def submit(self, function, callback=None):

        if self.busy:
            raise RuntimeError(
                "Hay otra operación en ejecución."
            )

        self.busy = True

        def execute():

            try:
                result = function()
                self.events.put(
                    ("success", result, callback)
                )

            except Exception as error:
                self.events.put(
                    ("error", str(error), None)
                )

        threading.Thread(
            target=execute,
            daemon=True
        ).start()

    def get_events(self):

        events = []

        while True:
            try:
                events.append(
                    self.events.get_nowait()
                )
            except queue.Empty:
                break

        return events
