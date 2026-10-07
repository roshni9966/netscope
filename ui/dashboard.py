import customtkinter as ctk

from ui.widgets import create_card, create_results_table


def create_dashboard_page(parent, network_info):
    """
    Create the NetScope dashboard page.
    """

    dashboard_page = ctk.CTkFrame(
        parent,
        fg_color="transparent",
        corner_radius=0,
    )

    dashboard_page.grid(
        row=0,
        column=0,
        sticky="nsew",
        padx=28,
        pady=25,
    )

    dashboard_page.grid_columnconfigure(
        (0, 1, 2),
        weight=1,
    )

    dashboard_page.grid_rowconfigure(
        4,
        weight=1,
    )

    heading = ctk.CTkLabel(
        dashboard_page,
        text="Network Dashboard",
        font=ctk.CTkFont(
            size=30,
            weight="bold",
        ),
    )

    heading.grid(
        row=0,
        column=0,
        columnspan=3,
        sticky="w",
    )

    subtitle = ctk.CTkLabel(
        dashboard_page,
        text="Monitor and explore devices on your local network.",
        font=ctk.CTkFont(size=15),
        text_color="gray",
    )

    subtitle.grid(
        row=1,
        column=0,
        columnspan=3,
        sticky="w",
        pady=(4, 24),
    )

    _, devices_value_label = create_card(
        parent=dashboard_page,
        row=2,
        column=0,
        title="Online Devices",
        value="0",
    )

    _, network_value_label = create_card(
        parent=dashboard_page,
        row=2,
        column=1,
        title="Network Range",
        value=network_info["network_range"],
    )

    _, gateway_value_label = create_card(
        parent=dashboard_page,
        row=2,
        column=2,
        title="Default Gateway",
        value=network_info["gateway"],
    )

    dashboard_results_frame = ctk.CTkFrame(
        dashboard_page,
    )

    dashboard_results_frame.grid(
        row=4,
        column=0,
        columnspan=3,
        sticky="nsew",
        pady=(24, 0),
    )

    dashboard_results_frame.grid_columnconfigure(
        0,
        weight=1,
    )

    dashboard_results_frame.grid_rowconfigure(
        1,
        weight=1,
    )

    results_heading = ctk.CTkLabel(
        dashboard_results_frame,
        text="Recent Scan Results",
        font=ctk.CTkFont(
            size=20,
            weight="bold",
        ),
    )

    results_heading.grid(
        row=0,
        column=0,
        sticky="w",
        padx=20,
        pady=(18, 10),
    )

    dashboard_empty_message = ctk.CTkLabel(
        dashboard_results_frame,
        text=(
            "No scan results yet.\n"
            "Open Network Scan to discover devices."
        ),
        font=ctk.CTkFont(size=15),
        text_color="gray",
    )

    dashboard_empty_message.grid(
        row=1,
        column=0,
        pady=90,
    )

    dashboard_table = create_results_table(
        dashboard_results_frame
    )

    dashboard_table.grid(
        row=1,
        column=0,
        sticky="nsew",
        padx=20,
        pady=(5, 20),
    )

    dashboard_table.grid_remove()

    return {
        "page": dashboard_page,
        "devices_value_label": devices_value_label,
        "network_value_label": network_value_label,
        "gateway_value_label": gateway_value_label,
        "empty_message": dashboard_empty_message,
        "table": dashboard_table,
    }