
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Detección de interfaces y redes IPv4."""

import ipaddress
import subprocess


def get_default_interface():
    """Detecta la interfaz asociada a la ruta predeterminada."""

    try:
        result = subprocess.run(
            ["ip", "-4", "route", "show", "default"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False
        )

        for line in result.stdout.splitlines():
            parts = line.split()

            if "dev" in parts:
                index = parts.index("dev")

                if index + 1 < len(parts):
                    return parts[index + 1]

    except (OSError, subprocess.TimeoutExpired):
        pass

    return None


def get_interfaces():
    """Obtiene interfaces con IPv4 y sus respectivas subredes."""

    interfaces = []

    try:
        result = subprocess.run(
            ["ip", "-o", "-4", "addr", "show"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False
        )

        if result.returncode != 0:
            return interfaces

        for line in result.stdout.splitlines():
            parts = line.split()

            if len(parts) < 4:
                continue

            interface = parts[1]
            address = parts[3]

            if interface == "lo":
                continue

            try:
                network = ipaddress.ip_interface(address).network

                interfaces.append({
                    "name": interface,
                    "address": str(network),
                    "ip": address.split("/")[0]
                })

            except ValueError:
                continue

    except (OSError, subprocess.TimeoutExpired):
        pass

    return interfaces
