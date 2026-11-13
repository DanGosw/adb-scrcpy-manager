
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Gestión del proceso scrcpy."""

import subprocess
import time

from pathlib import Path


class ScrcpyManager:

    def __init__(self, scrcpy_path, log_path):
        self.scrcpy_path = scrcpy_path
        self.log_path = Path(log_path)

    def require_scrcpy(self):
        if not self.scrcpy_path:
            raise RuntimeError(
                "No se encontró scrcpy. Instálalo con: "
                "sudo apt install scrcpy"
            )

        return self.scrcpy_path

    def launch(self, target):
        """Inicia scrcpy en un proceso independiente."""

        executable = self.require_scrcpy()

        self.log_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with self.log_path.open("a", encoding="utf-8") as logfile:
            logfile.write(
                f"\n\n--- Inicio scrcpy: {target} ---\n"
            )
            logfile.flush()

            try:
                process = subprocess.Popen(
                    [
                        executable,
                        "-s",
                        target
                    ],
                    stdin=subprocess.DEVNULL,
                    stdout=logfile,
                    stderr=subprocess.STDOUT,
                    start_new_session=True
                )
            except OSError as error:
                raise RuntimeError(
                    f"No se pudo iniciar scrcpy: {error}"
                )

        # Da tiempo a scrcpy para informar de errores de inicio.
        time.sleep(1.5)

        if process.poll() is not None:
            try:
                error_log = self.log_path.read_text(
                    encoding="utf-8"
                )[-4000:]
            except OSError:
                error_log = "No se pudo leer el registro de scrcpy."

            raise RuntimeError(
                "scrcpy se cerró durante el inicio.\n\n"
                f"Registro:\n{error_log}"
            )

        return {
            "target": target,
            "pid": process.pid
        }
