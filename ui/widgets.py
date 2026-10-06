import customtkinter as ctk


def create_card(parent, row, column, title, value):
    """
    Create a dashboard information card.
    """

    card = ctk.CTkFrame(
        parent,
        height=130,
    )

    card.grid(
        row=row,
        column=column,
        sticky="nsew",
        padx=7,
    )

    card.grid_propagate(False)

    title_label = ctk.CTkLabel(
        card,
        text=title,
        font=ctk.CTkFont(size=14),
        text_color="gray",
    )

    title_label.pack(
        anchor="w",
        padx=20,
        pady=(20, 8),
    )

    value_label = ctk.CTkLabel(
        card,
        text=value,
        font=ctk.CTkFont(
            size=22,
            weight="bold",
        ),
    )

    value_label.pack(
        anchor="w",
        padx=20,
    )

    return card, value_label