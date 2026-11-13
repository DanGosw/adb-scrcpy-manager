
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ADB Wireless Manager
Nuevo punto de entrada de la aplicación.
"""

import tkinter as tk
from tkinter import ttk

from ui.main_window import ADBWirelessManager


def main():
    root = tk.Tk()

    try:
        style = ttk.Style(root)
        style.theme_use("clam")
    except tk.TclError:
        pass

    ADBWirelessManager(root)

    root.mainloop()


if __name__ == "__main__":
    main()
