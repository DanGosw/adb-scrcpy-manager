
import tkinter as tk

from ui.theme import COLORS


class Card(tk.Frame):

    def __init__(
        self,
        parent,
        title=None,
        description=None,
        accent=None,
        **kwargs
    ):

        self.accent = accent or COLORS["accent"]
        self.card_bg = COLORS["surface"]

        super().__init__(
            parent,
            bg=self.card_bg,
            bd=0,
            highlightbackground=COLORS["border"],
            highlightthickness=1,
            **kwargs
        )

        self.body = self

        if title:

            header = tk.Frame(
                self,
                bg=self.card_bg
            )
            header.pack(
                fill="x",
                padx=18,
                pady=(17, 5)
            )

            indicator = tk.Frame(
                header,
                bg=self.accent,
                width=3,
                height=17
            )
            indicator.pack(
                side="left",
                padx=(0, 10)
            )
            indicator.pack_propagate(False)

            tk.Label(
                header,
                text=title,
                font=("Poppins", 11, "bold"),
                fg=COLORS["text"],
                bg=self.card_bg
            ).pack(
                side="left",
                anchor="center"
            )

        if description:

            tk.Label(
                self,
                text=description,
                font=("Poppins", 9),
                fg=COLORS["text_secondary"],
                bg=self.card_bg,
                justify="left",
                wraplength=700
            ).pack(
                anchor="w",
                padx=18,
                pady=(5, 16)
            )
