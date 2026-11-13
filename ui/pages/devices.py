
import tkinter as tk
from tkinter import ttk

from ui.theme import COLORS


class DevicesPage:

    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.build_ui()

    def build_ui(self):

        page = self.parent
        app = self.app

        # --------------------------------------------------
        # Configuración de la tabla
        # --------------------------------------------------

        style = ttk.Style()

        style.configure(
            "Devices.Treeview",
            background=COLORS["surface"],
            foreground=COLORS["text"],
            fieldbackground=COLORS["surface"],
            borderwidth=0,
            relief="flat",
            rowheight=38,
            font=("Poppins", 9)
        )

        style.map(
            "Devices.Treeview",
            background=[
                ("selected", COLORS["selection"])
            ],
            foreground=[
                ("selected", COLORS["text"])
            ]
        )

        style.configure(
            "Devices.Treeview.Heading",
            background=COLORS["surface_alt"],
            foreground=COLORS["text_secondary"],
            relief="flat",
            borderwidth=0,
            font=("Poppins", 9, "bold"),
            padding=(12, 11)
        )

        style.map(
            "Devices.Treeview.Heading",
            background=[
                ("active", COLORS["surface_hover"])
            ],
            foreground=[
                ("active", COLORS["text"])
            ]
        )

        # --------------------------------------------------
        # Contenedor general
        # --------------------------------------------------

        content = tk.Frame(
            page,
            bg=COLORS["background"]
        )

        content.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # --------------------------------------------------
        # Encabezado
        # --------------------------------------------------

        tk.Label(
            content,
            text="Dispositivos",
            font=("Poppins", 17, "bold"),
            fg=COLORS["text"],
            bg=COLORS["background"]
        ).pack(
            anchor="w",
            pady=(0, 5)
        )

        tk.Label(
            content,
            text="Administra tus dispositivos guardados y controla sus conexiones ADB.",
            font=("Poppins", 9),
            fg=COLORS["text_secondary"],
            bg=COLORS["background"]
        ).pack(
            anchor="w",
            pady=(0, 22)
        )

        # --------------------------------------------------
        # Helper para tarjetas
        # --------------------------------------------------

        def create_card(parent, title, description=None):

            card = tk.Frame(
                parent,
                bg=COLORS["surface"],
                highlightbackground=COLORS["border"],
                highlightthickness=1,
                bd=0
            )

            header = tk.Frame(
                card,
                bg=COLORS["surface"]
            )

            header.pack(
                fill="x",
                padx=20,
                pady=(17, 0)
            )

            title_row = tk.Frame(
                header,
                bg=COLORS["surface"]
            )

            title_row.pack(fill="x")

            indicator = tk.Frame(
                title_row,
                bg=COLORS["accent"],
                width=3,
                height=17
            )

            indicator.pack(
                side="left",
                padx=(0, 10)
            )

            indicator.pack_propagate(False)

            tk.Label(
                title_row,
                text=title,
                font=("Poppins", 10, "bold"),
                fg=COLORS["text"],
                bg=COLORS["surface"]
            ).pack(side="left")

            if description:

                tk.Label(
                    header,
                    text=description,
                    font=("Poppins", 8),
                    fg=COLORS["text_secondary"],
                    bg=COLORS["surface"],
                    justify="left"
                ).pack(
                    anchor="w",
                    pady=(5, 0)
                )

            body = tk.Frame(
                card,
                bg=COLORS["surface"]
            )

            body.pack(
                fill="both",
                expand=True,
                padx=20,
                pady=(15, 18)
            )

            return card, body

        # --------------------------------------------------
        # Dispositivos guardados
        # --------------------------------------------------

        saved_card, saved_body = create_card(
            content,
            "Dispositivos guardados",
            "Selecciona un dispositivo para administrar su conexión."
        )

        saved_card.pack(
            fill="both",
            expand=True,
            pady=(0, 16)
        )

        table_container = tk.Frame(
            saved_body,
            bg=COLORS["surface"],
            bd=0,
            highlightthickness=0
        )

        table_container.pack(
            fill="both",
            expand=True
        )

        columns = (
            "name",
            "address",
            "port"
        )

        app.saved_tree = ttk.Treeview(
            table_container,
            columns=columns,
            show="headings",
            height=7,
            style="Devices.Treeview"
        )

        app.saved_tree.heading(
            "name",
            text="DISPOSITIVO"
        )

        app.saved_tree.heading(
            "address",
            text="DIRECCIÓN IP"
        )

        app.saved_tree.heading(
            "port",
            text="PUERTO"
        )

        app.saved_tree.column(
            "name",
            width=240,
            minwidth=140,
            anchor="w"
        )

        app.saved_tree.column(
            "address",
            width=190,
            minwidth=130,
            anchor="w"
        )

        app.saved_tree.column(
            "port",
            width=110,
            minwidth=80,
            anchor="center"
        )

        saved_scroll = ttk.Scrollbar(
            table_container,
            orient="vertical",
            command=app.saved_tree.yview,
            style="Dark.Vertical.TScrollbar"
        )

        app.saved_tree.configure(
            yscrollcommand=saved_scroll.set
        )

        app.saved_tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        saved_scroll.pack(
            side="right",
            fill="y"
        )

        tk.Label(
            saved_body,
            text="Selecciona una fila para utilizar las acciones de administración.",
            font=("Poppins", 8),
            fg=COLORS["text_disabled"],
            bg=COLORS["surface"],
            anchor="w"
        ).pack(
            fill="x",
            pady=(12, 0)
        )

        # --------------------------------------------------
        # Administración
        # --------------------------------------------------

        admin_card, admin_body = create_card(
            content,
            "Administración",
            "Gestiona los dispositivos almacenados en tu colección."
        )

        admin_card.pack(
            fill="x",
            pady=(0, 16)
        )

        admin_buttons = tk.Frame(
            admin_body,
            bg=COLORS["surface"]
        )

        admin_buttons.pack(
            fill="x"
        )

        ttk.Button(
            admin_buttons,
            text="Reconectar",
            style="Accent.TButton",
            command=app.reconnect_saved
        ).pack(
            side="left",
            padx=(0, 10)
        )

        ttk.Button(
            admin_buttons,
            text="Renombrar",
            style="Dark.TButton",
            command=app.rename_saved
        ).pack(
            side="left",
            padx=(0, 10)
        )

        ttk.Button(
            admin_buttons,
            text="Eliminar",
            style="Danger.TButton",
            command=app.delete_saved
        ).pack(side="left")

        # --------------------------------------------------
        # Herramientas ADB
        # --------------------------------------------------

        tools_card, tools_body = create_card(
            content,
            "Herramientas ADB",
            "Accede a las operaciones adicionales de Android Debug Bridge."
        )

        tools_card.pack(
            fill="x",
            pady=(0, 16)
        )

        tools_buttons = tk.Frame(
            tools_body,
            bg=COLORS["surface"]
        )

        tools_buttons.pack(
            fill="x"
        )

        ttk.Button(
            tools_buttons,
            text="Listar dispositivos ADB",
            style="Dark.TButton",
            command=app.refresh_adb
        ).pack(
            side="left",
            padx=(0, 10)
        )

        ttk.Button(
            tools_buttons,
            text="Iniciar scrcpy",
            style="Dark.TButton",
            command=app.launch_scrcpy
        ).pack(
            side="left",
            padx=(0, 10)
        )

        ttk.Button(
            tools_buttons,
            text="Desconectar",
            style="Dark.TButton",
            command=app.disconnect_device
        ).pack(side="left")

        # --------------------------------------------------
        # Información
        # --------------------------------------------------

        info = tk.Frame(
            content,
            bg=COLORS["surface"],
            highlightbackground=COLORS["border"],
            highlightthickness=1,
            bd=0
        )

        info.pack(
            fill="x",
            pady=(0, 5)
        )

        tk.Label(
            info,
            text="INFORMACIÓN",
            font=("Poppins", 8, "bold"),
            fg=COLORS["accent"],
            bg=COLORS["surface"]
        ).pack(
            anchor="w",
            padx=16,
            pady=(12, 4)
        )

        tk.Label(
            info,
            text=(
                "Para utilizar estas herramientas, selecciona un dispositivo "
                "guardado o introduce su dirección IP y puerto desde la "
                "sección de escaneo."
            ),
            font=("Poppins", 8),
            fg=COLORS["text_secondary"],
            bg=COLORS["surface"],
            wraplength=700,
            justify="left"
        ).pack(
            anchor="w",
            padx=16,
            pady=(0, 12)
        )
