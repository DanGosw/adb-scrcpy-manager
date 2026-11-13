
import tkinter as tk
from tkinter import ttk

from ui.theme import COLORS


class DashboardPage:

    def __init__(self, parent, app):

        self.parent = parent
        self.app = app

        self.build_ui()

    def build_ui(self):

        page = self.parent
        app = self.app

        # Introducción
        tk.Label(
            page,
            text="Bienvenido",
            font=("Poppins", 17, "bold"),
            fg=COLORS["text"],
            bg=COLORS["background"]
        ).pack(
            anchor="w",
            pady=(5, 5)
        )

        tk.Label(
            page,
            text="Gestiona tus conexiones Android desde un solo lugar.",
            font=("Poppins", 9),
            fg=COLORS["text_secondary"],
            bg=COLORS["background"]
        ).pack(
            anchor="w",
            pady=(0, 24)
        )

        # Tarjetas de estado
        cards = tk.Frame(
            page,
            bg=COLORS["background"]
        )
        cards.pack(
            fill="x",
            pady=(0, 22)
        )

        cards.columnconfigure(0, weight=1)
        cards.columnconfigure(1, weight=1)

        def create_status_card(
            parent,
            title,
            initial_text,
            foreground,
            row,
            column
        ):

            card = tk.Frame(
                parent,
                bg=COLORS["surface"],
                highlightbackground=COLORS["border"],
                highlightthickness=1
            )

            card.grid(
                row=row,
                column=column,
                sticky="ew",
                padx=6,
                pady=6
            )

            header = tk.Frame(
                card,
                bg=COLORS["surface"]
            )
            header.pack(
                fill="x",
                padx=17,
                pady=(16, 7)
            )

            tk.Label(
                header,
                text=title.upper(),
                font=("Poppins", 8, "bold"),
                fg=COLORS["text_secondary"],
                bg=COLORS["surface"]
            ).pack(anchor="w")

            status = tk.Label(
                card,
                text=initial_text,
                font=("Poppins", 12, "bold"),
                fg=foreground,
                bg=COLORS["surface"],
                anchor="w"
            )

            status.pack(
                fill="x",
                padx=17,
                pady=(0, 17)
            )

            return status

        # ADB
        app.adb_status_label = create_status_card(
            cards,
            "Android Debug Bridge",
            "Comprobando...",
            COLORS["yellow"],
            0,
            0
        )

        # scrcpy
        app.scrcpy_status_label = create_status_card(
            cards,
            "Scrcpy",
            "Comprobando...",
            COLORS["yellow"],
            0,
            1
        )

        # Nmap
        app.nmap_status_label = create_status_card(
            cards,
            "Nmap",
            "Comprobando...",
            COLORS["yellow"],
            1,
            0
        )

        # Dispositivos guardados
        app.saved_count_label = create_status_card(
            cards,
            "Dispositivos guardados",
            str(len(app.store.devices)),
            COLORS["accent"],
            1,
            1
        )

        # Acceso rápido
        actions = app.create_card(
            page,
            "Acceso rápido",
            "Accede directamente a las funciones principales.",
            accent=COLORS["blue"]
        )

        actions.pack(
            fill="x",
            pady=(0, 18)
        )

        action_row = tk.Frame(
            actions,
            bg=COLORS["surface"]
        )
        action_row.pack(
            fill="x",
            padx=18,
            pady=(5, 17)
        )

        ttk.Button(
            action_row,
            text="Escanear red",
            style="Accent.TButton",
            command=lambda: app.show_page("scan")
        ).pack(
            side="left",
            padx=(0, 8)
        )

        ttk.Button(
            action_row,
            text="Ver dispositivos",
            style="Dark.TButton",
            command=lambda: app.show_page("devices")
        ).pack(
            side="left",
            padx=8
        )

        ttk.Button(
            action_row,
            text="Ver registro",
            style="Dark.TButton",
            command=lambda: app.show_page("logs")
        ).pack(
            side="left",
            padx=8
        )

        # Estado general
        app.dashboard_connection_label = tk.Label(
            page,
            text="Estado: Preparado",
            font=("Poppins", 9),
            fg=COLORS["text_secondary"],
            bg=COLORS["background"]
        )

        app.dashboard_connection_label.pack(
            anchor="w",
            pady=(12, 5)
        )
