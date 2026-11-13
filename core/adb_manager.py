
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Gestión de operaciones ADB."""

import subprocess


class ADBManager:

    def __init__(self, adb_path):
        self.adb_path = adb_path

    def require_adb(self):
        if not self.adb_path:
            raise RuntimeError(
                "No se encontró ADB. Instálalo con: sudo apt install adb"
            )

        return self.adb_path

    def run(self, arguments, timeout=30):
        """Ejecuta ADB sin utilizar un shell."""

        adb = self.require_adb()
        command = [adb] + list(arguments)

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=False
            )
        except subprocess.TimeoutExpired:
            raise RuntimeError(
                f"ADB superó el tiempo límite de {timeout} segundos."
            )
        except OSError as error:
            raise RuntimeError(f"No se pudo ejecutar ADB: {error}")

        output = result.stdout.strip()
        error = result.stderr.strip()

        if result.returncode != 0:
            raise RuntimeError(
                error or output or "ADB devolvió un error."
            )

        return {
            "stdout": output,
            "stderr": error,
            "returncode": result.returncode
        }

    def pair(self, target, pairing_code):
        """Empareja un dispositivo mediante su puerto de pairing."""

        return self.run(
            ["pair", target, pairing_code],
            timeout=60
        )

    def connect(self, target):
        """Conecta un dispositivo mediante IP y puerto."""

        return self.run(
            ["connect", target],
            timeout=30
        )

    def disconnect(self, target):
        """Desconecta un dispositivo específico."""

        return self.run(
            ["disconnect", target],
            timeout=20
        )

    def devices(self, long_format=False):
        """Devuelve la lista de dispositivos ADB."""

        arguments = ["devices"]

        if long_format:
            arguments.append("-l")

        result = self.run(arguments, timeout=20)
        return result["stdout"]

    def get_connected_devices(self):
        """Devuelve un diccionario serial: estado."""

        output = self.devices()
        connected = {}

        for line in output.splitlines():
            parts = line.split()

            if len(parts) >= 2 and parts[0] != "List":
                connected[parts[0]] = parts[1]

        return connected

    def is_connected(self, target):
        """Comprueba que un dispositivo esté en estado device."""

        devices = self.get_connected_devices()
        return devices.get(target) == "device"

    def connect_and_verify(self, target):
        """Conecta y verifica que ADB reconozca el dispositivo."""

        result = self.connect(target)

        if not self.is_connected(target):
            available = self.get_connected_devices()

            raise RuntimeError(
                f"ADB no reconoce {target} como conectado.\n\n"
                f"Dispositivos disponibles:\n"
                + (
                    "\n".join(
                        f"{serial} [{state}]"
                        for serial, state in available.items()
                    )
                    if available else "Ninguno"
                )
            )

        return result["stdout"]
