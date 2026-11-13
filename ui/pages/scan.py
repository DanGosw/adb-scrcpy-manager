
import tkinter as tk
from tkinter import ttk

from ui.theme import COLORS


class ScanPage:

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
            "Scan.Treeview",
            background=COLORS["surface"],
            foreground=COLORS["text"],
            fieldbackground=COLORS["surface"],
            borderwidth=0,
            relief="flat",
            rowheight=34,
            font=("Poppins", 9)
        )

        style.map(
            "Scan.Treeview",
            background=[
                ("selected", COLORS["selection"])
            ],
            foreground=[
                ("selected", COLORS["text"])
            ]
        )

        style.configure(
            "Scan.Treeview.Heading",
            background=COLORS["surface_alt"],
            foreground=COLORS["text_secondary"],
            relief="flat",
            borderwidth=0,
            font=("Poppins", 8, "bold"),
            padding=(12, 10)
        )

        style.map(
            "Scan.Treeview.Heading",
            background=[
                ("active", COLORS["surface_hover"])
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
            text="Escaneo de red",
            font=("Poppins", 17, "bold"),
            fg=COLORS["text"],
            bg=COLORS["background"]
        ).pack(
            anchor="w",
            pady=(0, 5)
        )

        tk.Label(
            content,
            text="Descubre dispositivos disponibles en tu red local y establece conexiones ADB.",
            font=("Poppins", 9),
            fg=COLORS["text_secondary"],
            bg=COLORS["background"]
        ).pack(
            anchor="w",
            pady=(0, 22)
        )

        # --------------------------------------------------
        # Helpers visuales
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

            tk.Label(
                header,
                text=title,
                font=("Poppins", 10, "bold"),
                fg=COLORS["text"],
                bg=COLORS["surface"]
            ).pack(anchor="w")

            if description:

                tk.Label(
                    card,
                    text=description,
                    font=("Poppins", 8),
                    fg=COLORS["text_secondary"],
                    bg=COLORS["surface"],
                    justify="left"
                ).pack(
                    anchor="w",
                    padx=20,
                    pady=(4, 0)
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
        # Red local
        # --------------------------------------------------

        network_card, network_body = create_card(
            content,
            "Red local",
            "Selecciona la interfaz de red que deseas utilizar para descubrir dispositivos."
        )

        network_card.pack(
            fill="x",
            pady=(0, 16)
        )

        network_row = tk.Frame(
            network_body,
            bg=COLORS["surface"]
        )

        network_row.pack(fill="x")

        network_row.columnconfigure(1, weight=1)

        ttk.Label(
            network_row,
            text="Interfaz de red",
            style="Surface.TLabel"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 16)
        )

        app.interface_combo = ttk.Combobox(
            network_row,
            textvariable=app.interface_var,
            state="readonly",
            width=30,
            style="Dark.TCombobox",
            font=("Poppins", 9)
        )

        app.interface_combo.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(0, 12)
        )

        ttk.Button(
            network_row,
            text="Actualizar",
            style="Dark.TButton",
            command=app.refresh_interfaces
        ).grid(
            row=0,
            column=2,
            padx=(0, 10)
        )

        app.scan_button = ttk.Button(
            network_row,
            text="Escanear red",
            style="Accent.TButton",
            command=app.scan_network
        )

        app.scan_button.grid(
            row=0,
            column=3
        )

        app.scan_status_label = tk.Label(
            network_body,
            text="Selecciona una interfaz para comenzar.",
            font=("Poppins", 8),
            fg=COLORS["text_secondary"],
            bg=COLORS["surface"],
            anchor="w"
        )

        app.scan_status_label.pack(
            fill="x",
            pady=(15, 0)
        )

        app.network_info = tk.Label(
            network_body,
            text="",
            font=("Poppins", 8),
            fg=COLORS["text_secondary"],
            bg=COLORS["surface"],
            anchor="w"
        )

        # --------------------------------------------------
        # Dispositivos encontrados
        # --------------------------------------------------

        scan_card, scan_body = create_card(
            content,
            "Dispositivos encontrados",
            "Selecciona un dispositivo para utilizar su dirección IP en las operaciones siguientes."
        )

        scan_card.pack(
            fill="both",
            expand=True,
            pady=(0, 16)
        )

        scan_table = tk.Frame(
            scan_body,
            bg=COLORS["surface"],
            bd=0,
            highlightthickness=0
        )

        scan_table.pack(
            fill="both",
            expand=True
        )

        columns = (
            "ip",
            "hostname",
            "status"
        )

        app.scan_tree = ttk.Treeview(
            scan_table,
            columns=columns,
            show="headings",
            height=6,
            style="Scan.Treeview"
        )

        app.scan_tree.heading(
            "ip",
            text="DIRECCIÓN IP"
        )

        app.scan_tree.heading(
            "hostname",
            text="NOMBRE"
        )

        app.scan_tree.heading(
            "status",
            text="ESTADO"
        )

        app.scan_tree.column(
            "ip",
            width=170,
            minwidth=120,
            anchor="w"
        )

        app.scan_tree.column(
            "hostname",
            width=240,
            minwidth=130,
            anchor="w"
        )

        app.scan_tree.column(
            "status",
            width=130,
            minwidth=90,
            anchor="center"
        )

        scan_scroll = ttk.Scrollbar(
            scan_table,
            orient="vertical",
            command=app.scan_tree.yview,
            style="Dark.Vertical.TScrollbar"
        )

        app.scan_tree.configure(
            yscrollcommand=scan_scroll.set
        )

        app.scan_tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scan_scroll.pack(
            side="right",
            fill="y"
        )

        app.scan_tree.bind(
            "<<TreeviewSelect>>",
            app.on_scan_selection
        )

        # --------------------------------------------------
        # Emparejamiento ADB
        # --------------------------------------------------

        pair_card, pair_body = create_card(
            content,
            "01  ·  Emparejamiento ADB",
            "Introduce los datos proporcionados por la función de depuración inalámbrica de Android."
        )

        pair_card.pack(
            fill="x",
            pady=(0, 16)
        )

        pair_body.columnconfigure(1, weight=1)

        def add_field(parent, label, row, variable, show=None):

            ttk.Label(
                parent,
                text=label,
                style="Surface.TLabel"
            ).grid(
                row=row,
                column=0,
                sticky="w",
                padx=(0, 20),
                pady=9
            )

            entry = ttk.Entry(
                parent,
                textvariable=variable,
                show=show,
                style="Dark.TEntry"
            )

            entry.grid(
                row=row,
                column=1,
                sticky="ew",
                pady=9
            )

            return entry

        add_field(
            pair_body,
            "Dirección IP",
            0,
            app.ip_var
        )

        add_field(
            pair_body,
            "Puerto de emparejamiento",
            1,
            app.pair_port_var
        )

        add_field(
            pair_body,
            "Código de emparejamiento",
            2,
            app.pair_code_var,
            show="*"
        )

        ttk.Button(
            pair_body,
            text="Emparejar dispositivo",
            style="Accent.TButton",
            command=app.pair_device
        ).grid(
            row=3,
            column=1,
            sticky="w",
            pady=(12, 0)
        )

        # --------------------------------------------------
        # Conexión ADB
        # --------------------------------------------------

        connect_card, connect_body = create_card(
            content,
            "02  ·  Conexión ADB",
            "Establece la conexión inalámbrica con un dispositivo previamente emparejado."
        )

        connect_card.pack(
            fill="x",
            pady=(0, 16)
        )

        connect_body.columnconfigure(1, weight=1)

        ttk.Label(
            connect_body,
            text="Dirección IP",
            style="Surface.TLabel"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 20),
            pady=9
        )

        tk.Label(
            connect_body,
            textvariable=app.ip_var,
            font=("Poppins", 9, "bold"),
            fg=COLORS["accent"],
            bg=COLORS["surface"],
            anchor="w"
        ).grid(
            row=0,
            column=1,
            sticky="w",
            pady=9
        )

        add_field(
            connect_body,
            "Puerto de conexión",
            1,
            app.connect_port_var
        )

        ttk.Button(
            connect_body,
            text="Conectar + scrcpy",
            style="Accent.TButton",
            command=app.connect_device
        ).grid(
            row=2,
            column=1,
            sticky="w",
            pady=(12, 0)
        )

        # --------------------------------------------------
        # Guardar dispositivo
        # --------------------------------------------------

        save_card, save_body = create_card(
            content,
            "Guardar dispositivo",
            "Almacena los datos de conexión para reutilizarlos posteriormente."
        )

        save_card.pack(
            fill="x",
            pady=(0, 10)
        )

        save_body.columnconfigure(1, weight=1)

        app.device_name_entry = add_field(
            save_body,
            "Nombre del dispositivo",
            0,
            app.device_name_var
        )

        ttk.Button(
            save_body,
            text="Guardar dispositivo",
            style="Dark.TButton",
            command=app.save_device
        ).grid(
            row=0,
            column=2,
            padx=(15, 0)
        )

        tk.Label(
            save_body,
            text="Se guarda la IP y el puerto. El código de emparejamiento nunca se almacena.",
            font=("Poppins", 8),
            fg=COLORS["text_disabled"],
            bg=COLORS["surface"],
            anchor="w"
        ).grid(
            row=1,
            column=0,
            columnspan=3,
            sticky="w",
            pady=(10, 0)
        )
