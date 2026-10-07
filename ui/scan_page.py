import customtkinter as ctk

from ui.widgets import create_results_table


def create_scan_page(
    parent,
    network_info,
    start_scan_command,
):
    """
    Create the NetScope Network Scan page.

    Returns references to widgets that app.py needs
    during and after a network scan.
    """

    scan_page = ctk.CTkFrame(
        parent,
        fg_color="transparent",
        corner_radius=0,
    )

    scan_page.grid(
        row=0,
        column=0,
        sticky="nsew",
        padx=28,
        pady=25,
    )

    scan_page.grid_columnconfigure(
        0,
        weight=1,
    )

    scan_page.grid_rowconfigure(
        4,
        weight=1,
    )

    # ---------------------------------------------------------
    # Heading
    # ---------------------------------------------------------

    heading = ctk.CTkLabel(
        scan_page,
        text="Network Scanner",
        font=ctk.CTkFont(
            size=30,
            weight="bold",
        ),
    )

    heading.grid(
        row=0,
        column=0,
        sticky="w",
    )

    subtitle = ctk.CTkLabel(
        scan_page,
        text=(
            "Discover active devices on a local network "
            "you own or have permission to inspect."
        ),
        font=ctk.CTkFont(size=15),
        text_color="gray",
    )

    subtitle.grid(
        row=1,
        column=0,
        sticky="w",
        pady=(4, 22),
    )

    # ---------------------------------------------------------
    # Scan controls
    # ---------------------------------------------------------

    controls_frame = ctk.CTkFrame(
        scan_page,
    )

    controls_frame.grid(
        row=2,
        column=0,
        sticky="ew",
    )

    controls_frame.grid_columnconfigure(
        0,
        weight=1,
    )

    range_label = ctk.CTkLabel(
        controls_frame,
        text="Network range",
        font=ctk.CTkFont(
            size=14,
            weight="bold",
        ),
    )

    range_label.grid(
        row=0,
        column=0,
        sticky="w",
        padx=20,
        pady=(16, 5),
    )

    network_range_entry = ctk.CTkEntry(
        controls_frame,
        height=42,
        placeholder_text="Example: 192.168.1.0/24",
    )

    network_range_entry.grid(
        row=1,
        column=0,
        sticky="ew",
        padx=(20, 10),
        pady=(0, 18),
    )

    network_range_entry.insert(
        0,
        network_info["network_range"],
    )

    start_scan_button = ctk.CTkButton(
        controls_frame,
        text="Start Scan",
        width=140,
        height=42,
        command=start_scan_command,
    )

    start_scan_button.grid(
        row=1,
        column=1,
        padx=(0, 20),
        pady=(0, 18),
    )

    # ---------------------------------------------------------
    # Scan status
    # ---------------------------------------------------------

    status_frame = ctk.CTkFrame(
        scan_page,
        fg_color="transparent",
    )

    status_frame.grid(
        row=3,
        column=0,
        sticky="ew",
        pady=(14, 8),
    )

    status_frame.grid_columnconfigure(
        0,
        weight=1,
    )

    scan_status_label = ctk.CTkLabel(
        status_frame,
        text="Ready to scan",
        text_color="gray",
    )

    scan_status_label.grid(
        row=0,
        column=0,
        sticky="w",
    )

    scan_progress = ctk.CTkProgressBar(
        status_frame,
        width=200,
        mode="indeterminate",
    )

    scan_progress.grid(
        row=0,
        column=1,
        sticky="e",
    )

    scan_progress.stop()
    scan_progress.grid_remove()

    # ---------------------------------------------------------
    # Results
    # ---------------------------------------------------------

    results_frame = ctk.CTkFrame(
        scan_page,
    )

    results_frame.grid(
        row=4,
        column=0,
        sticky="nsew",
    )

    results_frame.grid_columnconfigure(
        0,
        weight=1,
    )

    results_frame.grid_rowconfigure(
        1,
        weight=1,
    )

    results_title = ctk.CTkLabel(
        results_frame,
        text="Discovered Devices",
        font=ctk.CTkFont(
            size=20,
            weight="bold",
        ),
    )

    results_title.grid(
        row=0,
        column=0,
        sticky="w",
        padx=20,
        pady=(18, 10),
    )

    scan_table = create_results_table(
        results_frame
    )

    scan_table.grid(
        row=1,
        column=0,
        sticky="nsew",
        padx=20,
        pady=(5, 20),
    )

    # ---------------------------------------------------------
    # Return widgets app.py needs
    # ---------------------------------------------------------

    return {
        "page": scan_page,
        "network_range_entry": network_range_entry,
        "start_scan_button": start_scan_button,
        "status_label": scan_status_label,
        "progress": scan_progress,
        "table": scan_table,
    }