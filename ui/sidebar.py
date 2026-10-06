import customtkinter as ctk


def create_sidebar(
    parent,
    dashboard_command,
    network_scan_command,
):
    """
    Create the NetScope sidebar and return references
    to the navigation buttons.
    """

    sidebar = ctk.CTkFrame(
        parent,
        width=210,
        corner_radius=0,
    )

    sidebar.grid(
        row=0,
        column=0,
        sticky="nsew",
    )

    sidebar.grid_propagate(False)

    logo_label = ctk.CTkLabel(
        sidebar,
        text="NetScope",
        font=ctk.CTkFont(
            size=27,
            weight="bold",
        ),
    )

    logo_label.pack(
        padx=20,
        pady=(35, 38),
    )

    dashboard_button = ctk.CTkButton(
        sidebar,
        text="Dashboard",
        height=42,
        command=dashboard_command,
    )

    dashboard_button.pack(
        padx=20,
        pady=8,
        fill="x",
    )

    network_scan_button = ctk.CTkButton(
        sidebar,
        text="Network Scan",
        height=42,
        command=network_scan_command,
    )

    network_scan_button.pack(
        padx=20,
        pady=8,
        fill="x",
    )

    port_scanner_button = ctk.CTkButton(
        sidebar,
        text="Port Scanner",
        height=42,
        fg_color="transparent",
        border_width=1,
        state="disabled",
    )

    port_scanner_button.pack(
        padx=20,
        pady=8,
        fill="x",
    )

    about_button = ctk.CTkButton(
        sidebar,
        text="About",
        height=42,
        fg_color="transparent",
        border_width=1,
        state="disabled",
    )

    about_button.pack(
        padx=20,
        pady=8,
        fill="x",
    )

    version_label = ctk.CTkLabel(
        sidebar,
        text="Version 1.0",
        text_color="gray",
    )

    version_label.pack(
        side="bottom",
        pady=20,
    )

    return {
        "frame": sidebar,
        "dashboard_button": dashboard_button,
        "network_scan_button": network_scan_button,
        "port_scanner_button": port_scanner_button,
        "about_button": about_button,
    }