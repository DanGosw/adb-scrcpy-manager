
import tkinter as tk
from tkinter import ttk


class ScrollableFrame(tk.Frame):
    BG = "#10121B"

    _active_canvas = None
    _mousewheel_installed = False

    def __init__(self, parent, root=None):
        super().__init__(
            parent,
            bg=self.BG,
            bd=0,
            relief="flat",
            highlightthickness=0
        )

        self.root = root or self.winfo_toplevel()

        self.canvas = tk.Canvas(
            self,
            bg=self.BG,
            bd=0,
            relief="flat",
            highlightthickness=0
        )

        self.scrollbar = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.canvas.yview,
            style="Dark.Vertical.TScrollbar"
        )

        self.content = tk.Frame(
            self.canvas,
            bg=self.BG,
            bd=0,
            highlightthickness=0
        )

        self.window_id = self.canvas.create_window(
            (0, 0),
            window=self.content,
            anchor="nw"
        )

        self.canvas.configure(
            yscrollcommand=self.scrollbar.set
        )

        self.content.bind(
            "<Configure>",
            self._update_scrollregion
        )

        self.canvas.bind(
            "<Configure>",
            self._resize_content
        )

        self.canvas.bind("<Enter>", self._activate)
        self.canvas.bind("<Leave>", self._deactivate)

        self.content.bind("<Enter>", self._activate)
        self.content.bind("<Leave>", self._deactivate)

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.install_mousewheel_support(self.root)

    @classmethod
    def install_mousewheel_support(cls, root):
        if cls._mousewheel_installed:
            return

        root.bind_all("<MouseWheel>", cls._on_mousewheel)
        root.bind_all("<Button-4>", cls._on_mousewheel)
        root.bind_all("<Button-5>", cls._on_mousewheel)

        cls._mousewheel_installed = True

    def _activate(self, _event=None):
        ScrollableFrame._active_canvas = self.canvas

    def _deactivate(self, event=None):
        if event is None:
            return

        widget = self.winfo_containing(
            event.x_root,
            event.y_root
        )

        while widget is not None:
            if widget == self:
                return

            widget = getattr(widget, "master", None)

        if ScrollableFrame._active_canvas == self.canvas:
            ScrollableFrame._active_canvas = None

    @classmethod
    def _on_mousewheel(cls, event):
        canvas = cls._active_canvas

        if canvas is None:
            return

        try:
            if event.num == 4:
                canvas.yview_scroll(-3, "units")

            elif event.num == 5:
                canvas.yview_scroll(3, "units")

            elif event.delta:
                direction = -1 if event.delta > 0 else 1
                canvas.yview_scroll(direction * 3, "units")

            return "break"

        except tk.TclError:
            cls._active_canvas = None

    def _update_scrollregion(self, _event=None):
        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

        self.after_idle(self._update_scrollbar_visibility)

    def _resize_content(self, event):
        self.canvas.itemconfigure(
            self.window_id,
            width=event.width
        )

        self.after_idle(self._update_scrollbar_visibility)

    def _update_scrollbar_visibility(self):
        try:
            content_height = self.content.winfo_reqheight()
            available_height = self.canvas.winfo_height()

            if available_height <= 1:
                return

            needs_scroll = content_height > available_height + 2

            if needs_scroll:
                if not self.scrollbar.winfo_manager():
                    self.scrollbar.pack(
                        side="right",
                        fill="y"
                    )
            else:
                if self.scrollbar.winfo_manager():
                    self.scrollbar.pack_forget()

                self.canvas.yview_moveto(0)

        except tk.TclError:
            pass
