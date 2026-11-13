
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Persistencia local de dispositivos ADB."""

import json
import os

from datetime import datetime

from config.settings import CONFIG_DIR, DEVICES_FILE


class DeviceStore:

    def __init__(self):
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        self.devices = self.load()

    def load(self):
        """Carga los dispositivos guardados."""

        if not DEVICES_FILE.exists():
            return []

        try:
            with DEVICES_FILE.open("r", encoding="utf-8") as file:
                data = json.load(file)

            return data if isinstance(data, list) else []

        except (OSError, json.JSONDecodeError):
            return []

    def save(self):
        """Guarda los dispositivos mediante un archivo temporal."""

        CONFIG_DIR.mkdir(parents=True, exist_ok=True)

        temporary = DEVICES_FILE.with_suffix(".tmp")

        with temporary.open("w", encoding="utf-8") as file:
            json.dump(
                self.devices,
                file,
                indent=4,
                ensure_ascii=False
            )

        os.chmod(temporary, 0o600)
        temporary.replace(DEVICES_FILE)

    def add(self, name, ip, port):
        """Añade un dispositivo o actualiza uno con la misma IP."""

        for device in self.devices:
            if device["ip"] == ip:
                device["name"] = name
                device["port"] = int(port)
                device["updated"] = datetime.now().isoformat()
                self.save()
                return

        self.devices.append({
            "name": name,
            "ip": ip,
            "port": int(port),
            "created": datetime.now().isoformat()
        })

        self.save()

    def delete(self, index):
        """Elimina un dispositivo por su índice."""

        if 0 <= index < len(self.devices):
            del self.devices[index]
            self.save()

    def rename(self, index, name):
        """Cambia el nombre de un dispositivo."""

        if 0 <= index < len(self.devices):
            self.devices[index]["name"] = name
            self.save()
