
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Configuración central multiplataforma de ADB Wireless Manager."""

import os
import shutil
import sys
from pathlib import Path


APP_NAME = "ADB Wireless Manager"
APP_ID = "adb-wireless-manager"


# ============================================================
# SISTEMA OPERATIVO
# ============================================================

IS_WINDOWS = os.name == "nt"
IS_LINUX = sys.platform.startswith("linux")


# ============================================================
# DIRECTORIOS
# ============================================================

if IS_WINDOWS:
    CONFIG_DIR = (
        Path(os.environ.get("APPDATA", Path.home()))
        / "ADBWirelessManager"
    )
else:
    CONFIG_DIR = (
        Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
        / "adb-wireless-pairing"
    )

CONFIG_DIR.mkdir(parents=True, exist_ok=True)

DEVICES_FILE = CONFIG_DIR / "devices.json"
SCRCPY_LOG = CONFIG_DIR / "scrcpy.log"


# ============================================================
# HERRAMIENTAS PORTABLES
# ============================================================

if IS_WINDOWS:
    PORTABLE_TOOLS_DIR = Path(__file__).resolve().parent.parent / "tools"

    TOOL_EXTENSIONS = (".exe", ".cmd", ".bat", "")
else:
    PORTABLE_TOOLS_DIR = (
        Path.home()
        / "Documents"
        / "scrcpy-linux-x86_64-v5.0.1"
    )

    TOOL_EXTENSIONS = ("",)


# ============================================================
# DETECCIÓN DE EJECUTABLES
# ============================================================

def find_binary(name, alternatives=None):
    """
    Busca primero en rutas portables y después en PATH.

    En Windows contempla ejecutables .exe y otras extensiones
    habituales de herramientas de consola.
    """

    candidates = []

    if alternatives:
        candidates.extend(alternatives)

    portable_dir = PORTABLE_TOOLS_DIR

    for extension in TOOL_EXTENSIONS:
        candidates.append(portable_dir / f"{name}{extension}")

    executable = shutil.which(name)

    if executable:
        candidates.append(Path(executable))

    for candidate in candidates:
        if not candidate:
            continue

        candidate = Path(candidate).expanduser()

        if not candidate.is_file():
            continue

        if IS_WINDOWS or os.access(candidate, os.X_OK):
            return str(candidate)

    return None


# ============================================================
# ADB
# ============================================================

def get_adb_path():
    """Obtiene ADB portable o instalado en el sistema."""

    return find_binary(
        "adb",
        [PORTABLE_TOOLS_DIR / ("adb.exe" if IS_WINDOWS else "adb")]
    )


# ============================================================
# SCRCPY
# ============================================================

def get_scrcpy_path():
    """Obtiene scrcpy portable o instalado en el sistema."""

    return find_binary(
        "scrcpy",
        [PORTABLE_TOOLS_DIR / ("scrcpy.exe" if IS_WINDOWS else "scrcpy")]
    )


# ============================================================
# NMAP
# ============================================================

def get_nmap_path():
    """Obtiene Nmap portable o instalado en el sistema."""

    return find_binary(
        "nmap",
        [PORTABLE_TOOLS_DIR / ("nmap.exe" if IS_WINDOWS else "nmap")]
    )
