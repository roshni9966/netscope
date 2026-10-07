import ipaddress
import threading
import tkinter as tk

import customtkinter as ctk

from network_info import get_network_info
from scanner import scan_network
from ui.dashboard import create_dashboard_page
from ui.scan_page import create_scan_page
from ui.sidebar import create_sidebar

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class NetScopeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("NetScope")
        self.geometry("1150x720")
        self.minsize(950, 620)

        self.network_info = get_network_info()
        self.discovered_devices = []

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.setup_sidebar()
        self.create_page_container()
        self.setup_dashboard()
        self.setup_scan_page()
        self.show_dashboard()

    # ---------------------------------------------------------
    # Sidebar
    # ---------------------------------------------------------

    def setup_sidebar(self):
        sidebar_widgets = create_sidebar(
            parent=self,
            dashboard_command=self.show_dashboard,
            network_scan_command=self.show_scan_page,
        )

        self.sidebar = sidebar_widgets["frame"]

        self.dashboard_button = sidebar_widgets[
            "dashboard_button"
        ]

        self.network_scan_button = sidebar_widgets[
            "network_scan_button"
        ]

        self.port_scanner_button = sidebar_widgets[
            "port_scanner_button"
        ]

        self.about_button = sidebar_widgets[
            "about_button"
        ]

    # ---------------------------------------------------------
    # Main page container
    # ---------------------------------------------------------

    def create_page_container(self):
        self.page_container = ctk.CTkFrame(
            self,
            fg_color="transparent",
            corner_radius=0,
        )

        self.page_container.grid(
            row=0,
            column=1,
            sticky="nsew",
        )

        self.page_container.grid_columnconfigure(
            0,
            weight=1,
        )

        self.page_container.grid_rowconfigure(
            0,
            weight=1,
        )

    # ---------------------------------------------------------
    # Dashboard
    # ---------------------------------------------------------

    def setup_dashboard(self):
        dashboard_widgets = create_dashboard_page(
            parent=self.page_container,
            network_info=self.network_info,
        )

        self.dashboard_page = dashboard_widgets["page"]

        self.devices_value_label = dashboard_widgets[
            "devices_value_label"
        ]

        self.network_value_label = dashboard_widgets[
            "network_value_label"
        ]

        self.gateway_value_label = dashboard_widgets[
            "gateway_value_label"
        ]

        self.dashboard_empty_message = dashboard_widgets[
            "empty_message"
        ]

        self.dashboard_table = dashboard_widgets["table"]

    # ---------------------------------------------------------
    # Network Scan page
    # ---------------------------------------------------------

    def setup_scan_page(self):
            scan_widgets = create_scan_page(
                parent=self.page_container,
                network_info=self.network_info,
                start_scan_command=self.start_network_scan,
            )

            self.scan_page = scan_widgets["page"]

            self.network_range_entry = scan_widgets[
                "network_range_entry"
            ]

            self.start_scan_button = scan_widgets[
                "start_scan_button"
            ]

            self.scan_status_label = scan_widgets[
                "status_label"
            ]

            self.scan_progress = scan_widgets[
                "progress"
            ]

            self.scan_table = scan_widgets["table"]
                

    # ---------------------------------------------------------
    # Page navigation
    # ---------------------------------------------------------

    def show_dashboard(self):
        self.scan_page.grid_remove()
        self.dashboard_page.grid()

        self.dashboard_button.configure(
            fg_color="#1f6aa5",
            border_width=0,
        )

        self.network_scan_button.configure(
            fg_color="transparent",
            border_width=1,
        )

    def show_scan_page(self):
        self.dashboard_page.grid_remove()
        self.scan_page.grid()

        self.network_scan_button.configure(
            fg_color="#1f6aa5",
            border_width=0,
        )

        self.dashboard_button.configure(
            fg_color="transparent",
            border_width=1,
        )

    # ---------------------------------------------------------
    # Network scanning
    # ---------------------------------------------------------

    def validate_network_range(self, network_range):
        try:
            network = ipaddress.ip_network(
                network_range,
                strict=False,
            )

        except ValueError:
            return (
                None,
                "Please enter a valid network range.",
            )

        if network.version != 4:
            return (
                None,
                "Only IPv4 networks are currently supported.",
            )

        if not network.is_private:
            return (
                None,
                "Please use a private local network range.",
            )

        if network.num_addresses > 256:
            return (
                None,
                "For safety, NetScope currently scans "
                "a maximum of 256 addresses.",
            )

        return network, None

    def start_network_scan(self):
        network_range = (
            self.network_range_entry.get().strip()
        )

        _, error_message = self.validate_network_range(
            network_range
        )

        if error_message:
            self.scan_status_label.configure(
                text=error_message,
                text_color="#ff6b6b",
            )
            return

        self.clear_table(self.scan_table)

        self.start_scan_button.configure(
            state="disabled",
            text="Scanning...",
        )

        self.network_range_entry.configure(
            state="disabled"
        )

        self.scan_status_label.configure(
            text=f"Scanning {network_range}...",
            text_color="gray",
        )

        self.scan_progress.grid()
        self.scan_progress.start()

        scan_thread = threading.Thread(
            target=self.run_network_scan,
            args=(network_range,),
            daemon=True,
        )

        scan_thread.start()

    def run_network_scan(self, network_range):
        try:
            devices = scan_network(network_range)

            self.after(
                0,
                lambda: self.finish_network_scan(
                    devices,
                    network_range,
                ),
            )

        except Exception as error:
            self.after(
                0,
                lambda: self.handle_scan_error(
                    str(error)
                ),
            )

    def finish_network_scan(
        self,
        devices,
        network_range,
    ):
        self.discovered_devices = devices

        self.scan_progress.stop()
        self.scan_progress.grid_remove()

        self.start_scan_button.configure(
            state="normal",
            text="Start Scan",
        )

        self.network_range_entry.configure(
            state="normal"
        )

        self.devices_value_label.configure(
            text=str(len(devices))
        )

        self.network_value_label.configure(
            text=network_range
        )

        self.populate_table(
            self.scan_table,
            devices,
        )

        self.populate_table(
            self.dashboard_table,
            devices,
        )

        if devices:
            self.scan_status_label.configure(
                text=(
                    f"Scan complete — found "
                    f"{len(devices)} online device(s)."
                ),
                text_color="#4caf50",
            )

            self.dashboard_empty_message.grid_remove()
            self.dashboard_table.grid()

        else:
            self.scan_status_label.configure(
                text=(
                    "Scan complete — no online "
                    "devices were found."
                ),
                text_color="gray",
            )

            self.dashboard_table.grid_remove()

            self.dashboard_empty_message.configure(
                text=(
                    "The latest scan found "
                    "no online devices."
                )
            )

            self.dashboard_empty_message.grid()

    def handle_scan_error(self, error_message):
        self.scan_progress.stop()
        self.scan_progress.grid_remove()

        self.start_scan_button.configure(
            state="normal",
            text="Start Scan",
        )

        self.network_range_entry.configure(
            state="normal"
        )

        self.scan_status_label.configure(
            text=f"Scan failed: {error_message}",
            text_color="#ff6b6b",
        )

    # ---------------------------------------------------------
    # Table data
    # ---------------------------------------------------------

    def populate_table(self, table, devices):
        self.clear_table(table)

        for device in devices:
            table.insert(
                "",
                tk.END,
                values=(
                    device.get(
                        "status",
                        "Unknown",
                    ),
                    device.get(
                        "ip_address",
                        "Unknown",
                    ),
                    device.get(
                        "mac_address",
                        "Not available",
                    ),
                    device.get(
                        "hostname",
                        "Unknown",
                    ),
                ),
            )

    @staticmethod
    def clear_table(table):
        for row in table.get_children():
            table.delete(row)


if __name__ == "__main__":
    app = NetScopeApp()
    app.mainloop()