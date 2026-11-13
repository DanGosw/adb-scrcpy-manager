
import tkinter as tk
from tkinter import ttk


COLORS = {
    "background": "#0B0D14",
    "sidebar": "#10131E",
    "surface": "#171B29",
    "surface_alt": "#202638",
    "surface_hover": "#293149",
    "border": "#2B3348",

    "accent": "#9B8CFF",
    "accent_hover": "#B0A5FF",
    "blue": "#6EA8FE",
    "cyan": "#55D6E8",
    "green": "#55D6A0",
    "yellow": "#FFD479",
    "red": "#FF7185",

    "text": "#EDF0FA",
    "text_secondary": "#929BB2",
    "text_disabled": "#606A80",

    "selection": "#38365F",
    "scrollbar": "#353D55",
    "scrollbar_hover": "#515D7D",
}


FONT = "Poppins"


def apply_theme(root):

    root.configure(
        bg=COLORS["background"]
    )

    style = ttk.Style(root)
    style.theme_use("clam")

    # Frames

    style.configure(
        "Dark.TFrame",
        background=COLORS["background"]
    )

    style.configure(
        "Surface.TFrame",
        background=COLORS["surface"]
    )

    # Labels

    style.configure(
        "Dark.TLabel",
        background=COLORS["background"],
        foreground=COLORS["text"],
        font=(FONT, 10)
    )

    style.configure(
        "Muted.TLabel",
        background=COLORS["background"],
        foreground=COLORS["text_secondary"],
        font=(FONT, 9)
    )

    style.configure(
        "Surface.TLabel",
        background=COLORS["surface"],
        foreground=COLORS["text"],
        font=(FONT, 10)
    )

    # LabelFrame

    style.configure(
        "Dark.TLabelframe",
        background=COLORS["surface"],
        bordercolor=COLORS["border"],
        relief="flat"
    )

    style.configure(
        "Dark.TLabelframe.Label",
        background=COLORS["surface"],
        foreground=COLORS["accent"],
        font=(FONT, 10, "bold")
    )

    # Entries

    style.configure(
        "Dark.TEntry",
        fieldbackground=COLORS["surface_alt"],
        foreground=COLORS["text"],
        insertcolor=COLORS["text"],
        bordercolor=COLORS["border"],
        lightcolor=COLORS["border"],
        darkcolor=COLORS["border"],
        padding=(12, 10),
        relief="flat",
        borderwidth=1,
        font=(FONT, 9)
    )

    style.map(
        "Dark.TEntry",
        bordercolor=[
            ("focus", COLORS["accent"]),
            ("disabled", COLORS["border"])
        ],
        lightcolor=[
            ("focus", COLORS["accent"])
        ],
        darkcolor=[
            ("focus", COLORS["accent"])
        ],
        fieldbackground=[
            ("disabled", COLORS["background"])
        ]
    )
   
    # Combobox

    style.configure(
        "Dark.TCombobox",
        fieldbackground=COLORS["surface_alt"],
        background=COLORS["surface_alt"],
        foreground=COLORS["text"],
        arrowcolor=COLORS["accent"],
        bordercolor=COLORS["border"],
        lightcolor=COLORS["border"],
        darkcolor=COLORS["border"],
        padding=(12, 10),
        relief="flat",
        arrowsize=14,
        font=(FONT, 9)
    )

    style.map(
        "Dark.TCombobox",
        fieldbackground=[
            ("readonly", COLORS["surface_alt"]),
            ("focus", COLORS["surface_alt"]),
            ("disabled", COLORS["background"])
        ],
        background=[
            ("readonly", COLORS["surface_alt"]),
            ("active", COLORS["surface_hover"])
        ],
        foreground=[
            ("readonly", COLORS["text"]),
            ("disabled", COLORS["text_disabled"])
        ],
        selectbackground=[
            ("readonly", COLORS["selection"])
        ],
        selectforeground=[
            ("readonly", COLORS["text"])
        ],
        bordercolor=[
            ("focus", COLORS["accent"])
        ],
        lightcolor=[
            ("focus", COLORS["accent"])
        ],
        darkcolor=[
            ("focus", COLORS["accent"])
        ]
    )

    # Lista desplegable del Combobox
    style.configure(
        "Dark.TCombobox",
        postoffset=(0, 0, 0, 0)
    )

    # Buttons

    style.configure(
        "Dark.TButton",
        background=COLORS["surface_alt"],
        foreground=COLORS["text"],
        borderwidth=1,
        bordercolor=COLORS["border"],
        lightcolor=COLORS["surface_alt"],
        darkcolor=COLORS["surface_alt"],
        padding=(16, 11),
        font=(FONT, 9, "bold"),
        relief="flat",
        focusthickness=0
    )

    style.map(
        "Dark.TButton",
        background=[
            ("disabled", COLORS["surface"]),
            ("pressed", COLORS["selection"]),
            ("active", COLORS["surface_hover"])
        ],
        foreground=[
            ("disabled", COLORS["text_disabled"]),
            ("active", COLORS["text"])
        ],
        bordercolor=[
            ("active", COLORS["accent"])
        ]
    )

    style.configure(
        "Accent.TButton",
        background=COLORS["accent"],
        foreground="#111322",
        borderwidth=0,
        padding=(18, 11),
        font=(FONT, 9, "bold"),
        relief="flat",
        focusthickness=0
    )

    style.map(
        "Accent.TButton",
        background=[
            ("disabled", COLORS["surface_alt"]),
            ("pressed", COLORS["accent"]),
            ("active", COLORS["accent_hover"])
        ],
        foreground=[
            ("disabled", COLORS["text_disabled"]),
            ("active", "#111322")
        ]
    )

    style.configure(
        "Danger.TButton",
        background=COLORS["red"],
        foreground="#1B1018",
        borderwidth=0,
        padding=(16, 11),
        font=(FONT, 9, "bold"),
        relief="flat",
        focusthickness=0
    )

    style.map(
        "Danger.TButton",
        background=[
            ("active", "#FF91A0"),
            ("pressed", "#E85D75")
        ]
    )

    # Treeview

    style.configure(
        "Treeview",
        background=COLORS["surface"],
        foreground=COLORS["text"],
        fieldbackground=COLORS["surface"],
        borderwidth=0,
        relief="flat",
        rowheight=38,
        font=(FONT, 9)
    )

    style.configure(
        "Treeview.Heading",
        background=COLORS["surface_alt"],
        foreground=COLORS["text_secondary"],
        relief="flat",
        borderwidth=0,
        font=(FONT, 9, "bold"),
        padding=10
    )

    style.map(
        "Treeview",
        background=[
            ("selected", COLORS["selection"])
        ],
        foreground=[
            ("selected", COLORS["text"])
        ]
    )

    style.map(
        "Treeview.Heading",
        background=[
            ("active", COLORS["surface_hover"])
        ],
        foreground=[
            ("active", COLORS["text"])
        ]
    )

    # Scrollbar

    style.configure(
        "Dark.Vertical.TScrollbar",
        background=COLORS["scrollbar"],
        troughcolor=COLORS["background"],
        bordercolor=COLORS["background"],
        lightcolor=COLORS["scrollbar"],
        darkcolor=COLORS["scrollbar"],
        arrowcolor=COLORS["text_secondary"],
        relief="flat",
        borderwidth=0,
        width=7
    )

    style.map(
        "Dark.Vertical.TScrollbar",
        background=[
            ("active", COLORS["scrollbar_hover"]),
            ("pressed", COLORS["accent"])
        ]
    )

    return style
