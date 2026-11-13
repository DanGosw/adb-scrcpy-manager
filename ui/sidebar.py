
import tkinter as tk

from ui.theme import COLORS


class Sidebar(tk.Frame):

    def __init__(self, parent, on_navigate):

        super().__init__(
            parent,
            bg=COLORS["sidebar"],
            width=245,
            highlightthickness=0
        )

        self.on_navigate = on_navigate
        self.active_page = None
        self.buttons = {}

        self.pack_propagate(False)

        self.build_ui()

    def build_ui(self):

        # Identidad de la aplicación
        header = tk.Frame(
            self,
            bg=COLORS["sidebar"]
        )
        header.pack(
            fill="x",
            padx=24,
            pady=(30, 30)
        )

        brand = tk.Frame(
            header,
            bg=COLORS["sidebar"]
        )
        brand.pack(anchor="w")

        tk.Label(
            brand,
            text="ADB",
            font=("Poppins", 25, "bold"),
            fg=COLORS["accent"],
            bg=COLORS["sidebar"]
        ).pack(anchor="w")

        tk.Label(
            header,
            text="WIRELESS MANAGER",
            font=("Poppins", 8, "bold"),
            fg=COLORS["text_secondary"],
            bg=COLORS["sidebar"]
        ).pack(anchor="w", pady=(0, 5))

        tk.Label(
            header,
            text="Android device management",
            font=("Poppins", 8),
            fg=COLORS["text_disabled"],
            bg=COLORS["sidebar"]
        ).pack(anchor="w")

        # Separador
        tk.Frame(
            self,
            bg=COLORS["border"],
            height=1
        ).pack(
            fill="x",
            padx=20,
            pady=(0, 25)
        )

        # Navegación principal
        tk.Label(
            self,
            text="WORKSPACE",
            font=("Poppins", 8, "bold"),
            fg=COLORS["text_disabled"],
            bg=COLORS["sidebar"]
        ).pack(
            anchor="w",
            padx=24,
            pady=(0, 12)
        )

        navigation = [
            ("dashboard", "Resumen", "01"),
            ("scan", "Escanear red", "02"),
            ("devices", "Dispositivos", "03"),
            ("logs", "Registro", "04"),
        ]

        for page_id, label, number in navigation:
            self.add_button(page_id, label, number)

        # Preferencias
        tk.Label(
            self,
            text="CONFIGURACIÓN",
            font=("Poppins", 8, "bold"),
            fg=COLORS["text_disabled"],
            bg=COLORS["sidebar"]
        ).pack(
            anchor="w",
            padx=24,
            pady=(32, 12)
        )

        self.add_button(
            "settings",
            "Ajustes",
            "05"
        )

        # Pie del sidebar
        footer = tk.Frame(
            self,
            bg=COLORS["sidebar"]
        )
        footer.pack(
            side="bottom",
            fill="x",
            padx=20,
            pady=22
        )

        tk.Frame(
            footer,
            bg=COLORS["border"],
            height=1
        ).pack(
            fill="x",
            pady=(0, 15)
        )

        tk.Label(
            footer,
            text="ADB Wireless Manager",
            font=("Poppins", 8, "bold"),
            fg=COLORS["text_secondary"],
            bg=COLORS["sidebar"]
        ).pack(anchor="w")

        tk.Label(
            footer,
            text="Version 2.0",
            font=("Poppins", 8),
            fg=COLORS["text_disabled"],
            bg=COLORS["sidebar"]
        ).pack(
            anchor="w",
            pady=(4, 0)
        )

    def add_button(self, page_id, label, number):

        container = tk.Frame(
            self,
            bg=COLORS["sidebar"]
        )
        container.pack(
            fill="x",
            padx=12,
            pady=3
        )

        indicator = tk.Frame(
            container,
            bg=COLORS["sidebar"],
            width=3
        )
        indicator.pack(
            side="left",
            fill="y"
        )

        button = tk.Button(
            container,
            text=f"{number}   {label}",
            font=("Poppins", 9),
            anchor="w",
            relief="flat",
            bd=0,
            padx=15,
            pady=12,
            cursor="hand2",
            bg=COLORS["sidebar"],
            fg=COLORS["text_secondary"],
            activebackground=COLORS["surface_hover"],
            activeforeground=COLORS["text"],
            command=lambda: self.navigate(page_id)
        )

        button.pack(
            side="left",
            fill="x",
            expand=True
        )

        button.bind(
            "<Enter>",
            lambda event: self.on_hover(page_id, True)
        )

        button.bind(
            "<Leave>",
            lambda event: self.on_hover(page_id, False)
        )

        self.buttons[page_id] = {
            "button": button,
            "indicator": indicator,
            "container": container
        }

    def on_hover(self, page_id, hovering):

        if page_id == self.active_page:
            return

        elements = self.buttons[page_id]
        button = elements["button"]

        button.configure(
            bg=COLORS["surface_hover"] if hovering else COLORS["sidebar"],
            fg=COLORS["text"] if hovering else COLORS["text_secondary"]
        )

        elements["container"].configure(
            bg=COLORS["surface_hover"] if hovering else COLORS["sidebar"]
        )

    def navigate(self, page_id):

        self.set_active(page_id)
        self.on_navigate(page_id)

    def set_active(self, page_id):

        self.active_page = page_id

        for key, elements in self.buttons.items():

            button = elements["button"]
            indicator = elements["indicator"]
            container = elements["container"]

            if key == page_id:

                button.configure(
                    bg=COLORS["surface_active"] if "surface_active" in COLORS else COLORS["surface_alt"],
                    fg=COLORS["accent"],
                    font=("Poppins", 9, "bold")
                )

                indicator.configure(
                    bg=COLORS["accent"]
                )

                container.configure(
                    bg=COLORS["surface_alt"]
                )

            else:

                button.configure(
                    bg=COLORS["sidebar"],
                    fg=COLORS["text_secondary"],
                    font=("Poppins", 9)
                )

                indicator.configure(
                    bg=COLORS["sidebar"]
                )

                container.configure(
                    bg=COLORS["sidebar"]
                )
