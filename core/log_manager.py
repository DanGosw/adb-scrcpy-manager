
import threading
from datetime import datetime


class LogManager:

    def __init__(self, task_manager, text_widget):
        self.task_manager = task_manager
        self.text_widget = text_widget

    def log(self, message):

        if threading.current_thread() is not threading.main_thread():
            self.task_manager.events.put(
                ("log", str(message), None)
            )
            return

        self.append(message)

    def append(self, message):

        timestamp = datetime.now().strftime("%H:%M:%S")

        self.text_widget.configure(state="normal")

        self.text_widget.insert(
            "end",
            f"[{timestamp}] {message}\n"
        )

        self.text_widget.see("end")
        self.text_widget.configure(state="disabled")
