from tkinter import ttk
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

def create_results_table(parent):
    """
    Create a reusable NetScope device results table.
    """

    style = ttk.Style()
    style.theme_use("clam")

    style.configure(
        "NetScope.Treeview",
        background="#2b2b2b",
        foreground="#f2f2f2",
        fieldbackground="#2b2b2b",
        rowheight=36,
        borderwidth=0,
        font=("Arial", 11),
    )

    style.configure(
        "NetScope.Treeview.Heading",
        background="#1f6aa5",
        foreground="white",
        relief="flat",
        font=("Arial", 11, "bold"),
    )

    style.map(
        "NetScope.Treeview",
        background=[("selected", "#1f6aa5")],
    )

    table = ttk.Treeview(
        parent,
        columns=(
            "status",
            "ip_address",
            "mac_address",
            "hostname",
        ),
        show="headings",
        style="NetScope.Treeview",
    )

    table.heading("status", text="Status")
    table.heading("ip_address", text="IP Address")
    table.heading("mac_address", text="MAC Address")
    table.heading("hostname", text="Hostname")

    table.column(
        "status",
        width=120,
        anchor="center",
    )

    table.column(
        "ip_address",
        width=210,
        anchor="center",
    )

    table.column(
        "mac_address",
        width=220,
        anchor="center",
    )

    table.column(
        "hostname",
        width=400,
        anchor="w",
    )

    return table