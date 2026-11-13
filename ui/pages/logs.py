
import tkinter as tk
from tkinter import ttk

from ui.theme import COLORS


class LogsPage:

    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.build_ui()

    def build_ui(self):

        page = self.parent
        app = self.app

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
            text="Registro de operaciones",
            font=("Poppins", 17, "bold"),
            fg=COLORS["text"],
            bg=COLORS["background"]
        ).pack(
            anchor="w",
            pady=(0, 5)
        )

        tk.Label(
            content,
            text="Consulta las operaciones ejecutadas y los mensajes generados por la aplicación.",
            font=("Poppins", 9),
            fg=COLORS["text_secondary"],
            bg=COLORS["background"]
        ).pack(
            anchor="w",
            pady=(0, 22)
        )

        # --------------------------------------------------
        # Tarjeta de registro
        # --------------------------------------------------

        log_card = tk.Frame(
            content,
            bg=COLORS["surface"],
            highlightbackground=COLORS["border"],
            highlightthickness=1,
            bd=0
        )

        log_card.pack(
            fill="both",
            expand=True
        )

        # Encabezado de tarjeta

        header = tk.Frame(
            log_card,
            bg=COLORS["surface"]
        )

        header.pack(
            fill="x",
            padx=20,
            pady=(17, 14)
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
            text="Consola de actividad",
            font=("Poppins", 10, "bold"),
            fg=COLORS["text"],
            bg=COLORS["surface"]
        ).pack(side="left")

        tk.Label(
            header,
            text="Mensajes del sistema, conexiones y operaciones ADB.",
            font=("Poppins", 8),
            fg=COLORS["text_secondary"],
            bg=COLORS["surface"]
        ).pack(
            anchor="w",
            pady=(5, 0)
        )

        # --------------------------------------------------
        # Área de texto
        # --------------------------------------------------

        log_container = tk.Frame(
            log_card,
            bg=COLORS["surface_alt"],
            highlightbackground=COLORS["border"],
            highlightthickness=1,
            bd=0
        )

        log_container.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 18)
        )

        app.log_text = tk.Text(
            log_container,
            height=16,
            wrap="word",
            state="disabled",
            bg=COLORS["surface_alt"],
            fg=COLORS["text"],
            insertbackground=COLORS["text"],
            selectbackground=COLORS["selection"],
            selectforeground=COLORS["text"],
            relief="flat",
            borderwidth=0,
            padx=15,
            pady=14,
            font=("JetBrains Mono", 9),
            spacing1=3,
            spacing3=3
        )

        log_scroll = ttk.Scrollbar(
            log_container,
            orient="vertical",
            command=app.log_text.yview,
            style="Dark.Vertical.TScrollbar"
        )

        app.log_text.configure(
            yscrollcommand=log_scroll.set
        )

        app.log_text.pack(
            side="left",
            fill="both",
            expand=True
        )

        log_scroll.pack(
            side="right",
            fill="y"
        )

        # --------------------------------------------------
        # Acciones
        # --------------------------------------------------

        actions = tk.Frame(
            content,
            bg=COLORS["background"]
        )

        actions.pack(
            fill="x",
            pady=(15, 0)
        )

        def clear_logs():

            app.log_text.configure(state="normal")
            app.log_text.delete("1.0", "end")
            app.log_text.configure(state="disabled")

            app.log("Registro limpiado.")

        ttk.Button(
            actions,
            text="Limpiar registro",
            style="Dark.TButton",
            command=clear_logs
        ).pack(side="right")
