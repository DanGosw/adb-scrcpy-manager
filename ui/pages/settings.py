
import tkinter as tk

from config.settings import CONFIG_DIR, DEVICES_FILE
from ui.theme import COLORS


class SettingsPage:

    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.build_ui()

    def create_info_card(self, parent, title, description, accent=None):
        card = tk.Frame(
            parent,
            bg=COLORS["surface"],
            highlightbackground=COLORS["border"],
            highlightthickness=1
        )

        header = tk.Frame(
            card,
            bg=COLORS["surface"]
        )
        header.pack(fill="x", padx=18, pady=(15, 5))

        if accent:
            tk.Frame(
                header,
                bg=accent,
                width=3,
                height=18
            ).pack(side="left", padx=(0, 9))

        tk.Label(
            header,
            text=title,
            font=("Poppins", 11, "bold"),
            fg=COLORS["text"],
            bg=COLORS["surface"]
        ).pack(side="left")

        tk.Label(
            card,
            text=description,
            font=("Poppins", 9),
            fg=COLORS["text_secondary"],
            bg=COLORS["surface"],
            justify="left",
            anchor="w",
            wraplength=850
        ).pack(
            fill="x",
            padx=18,
            pady=(4, 16)
        )

        return card

    def build_ui(self):

        page = self.parent
        app = self.app

        # Encabezado
        tk.Label(
            page,
            text="Configuración",
            font=("Poppins", 19, "bold"),
            fg=COLORS["text"],
            bg=COLORS["background"]
        ).pack(anchor="w", pady=(0, 5))

        tk.Label(
            page,
            text="Información del entorno y almacenamiento de la aplicación.",
            font=("Poppins", 9),
            fg=COLORS["text_secondary"],
            bg=COLORS["background"]
        ).pack(anchor="w", pady=(0, 20))

        # Herramientas detectadas
        tools_card = self.create_info_card(
            page,
            "Herramientas del sistema",
            "Estado de las dependencias necesarias para el funcionamiento."
        )
        tools_card.pack(fill="x", pady=7)

        tools = [
            ("ADB", app.adb_path),
            ("scrcpy", app.scrcpy_path),
            ("Nmap", app.nmap_path)
        ]

        for name, path in tools:

            item = tk.Frame(
                tools_card,
                bg=COLORS["surface"]
            )
            item.pack(
                fill="x",
                padx=18,
                pady=7
            )

            tk.Label(
                item,
                text=name,
                font=("Poppins", 9, "bold"),
                fg=COLORS["text"],
                bg=COLORS["surface"],
                width=12,
                anchor="w"
            ).pack(side="left")

            tk.Label(
                item,
                text=path or "No encontrado",
                font=("JetBrains Mono", 8),
                fg=COLORS["green"] if path else COLORS["red"],
                bg=COLORS["surface"],
                anchor="w",
                justify="left",
                wraplength=700
            ).pack(
                side="left",
                fill="x",
                expand=True
            )

        # Almacenamiento
        config_card = self.create_info_card(
            page,
            "Almacenamiento",
            f"Directorio de configuración:\n{CONFIG_DIR}\n\n"
            f"Archivo de dispositivos guardados:\n{DEVICES_FILE}\n\n"
            "Los códigos de emparejamiento no se almacenan.",
            accent=COLORS["blue"]
        )
        config_card.pack(fill="x", pady=8)

        # Información de la aplicación
        version_card = self.create_info_card(
            page,
            "Información de la aplicación",
            "ADB Wireless Manager 2.0\n"
            "Interfaz desarrollada con Python y Tkinter.",
            accent=COLORS["accent"]
        )
        version_card.pack(fill="x", pady=8)
