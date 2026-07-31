import ipaddress
import threading
import tkinter as tk
from tkinter import ttk

import customtkinter as ctk

from network_info import get_network_info
from scanner import scan_network


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

        self.create_sidebar()
        self.create_page_container()
        self.create_dashboard_page()
        self.create_scan_page()

        self.show_dashboard()

    # ---------------------------------------------------------
    # Sidebar
    # ---------------------------------------------------------

    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self,
            width=210,
            corner_radius=0,
        )
        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsew",
        )
        self.sidebar.grid_propagate(False)

        self.logo_label = ctk.CTkLabel(
            self.sidebar,
            text="NetScope",
            font=ctk.CTkFont(
                size=27,
                weight="bold",
            ),
        )
        self.logo_label.pack(
            padx=20,
            pady=(35, 38),
        )

        self.dashboard_button = ctk.CTkButton(
            self.sidebar,
            text="Dashboard",
            height=42,
            command=self.show_dashboard,
        )
        self.dashboard_button.pack(
            padx=20,
            pady=8,
            fill="x",
        )

        self.network_scan_button = ctk.CTkButton(
            self.sidebar,
            text="Network Scan",
            height=42,
            command=self.show_scan_page,
        )
        self.network_scan_button.pack(
            padx=20,
            pady=8,
            fill="x",
        )

        self.port_scanner_button = ctk.CTkButton(
            self.sidebar,
            text="Port Scanner",
            height=42,
            fg_color="transparent",
            border_width=1,
            state="disabled",
        )
        self.port_scanner_button.pack(
            padx=20,
            pady=8,
            fill="x",
        )

        self.about_button = ctk.CTkButton(
            self.sidebar,
            text="About",
            height=42,
            fg_color="transparent",
            border_width=1,
            state="disabled",
        )
        self.about_button.pack(
            padx=20,
            pady=8,
            fill="x",
        )

        self.version_label = ctk.CTkLabel(
            self.sidebar,
            text="Version 1.0",
            text_color="gray",
        )
        self.version_label.pack(
            side="bottom",
            pady=20,
        )

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

        self.page_container.grid_columnconfigure(0, weight=1)
        self.page_container.grid_rowconfigure(0, weight=1)

    # ---------------------------------------------------------
    # Dashboard page
    # ---------------------------------------------------------

    def create_dashboard_page(self):
        self.dashboard_page = ctk.CTkFrame(
            self.page_container,
            fg_color="transparent",
            corner_radius=0,
        )
        self.dashboard_page.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=28,
            pady=25,
        )

        self.dashboard_page.grid_columnconfigure(
            (0, 1, 2),
            weight=1,
        )
        self.dashboard_page.grid_rowconfigure(4, weight=1)

        heading = ctk.CTkLabel(
            self.dashboard_page,
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
            self.dashboard_page,
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

        _, self.devices_value_label = self.create_card(
            parent=self.dashboard_page,
            row=2,
            column=0,
            title="Online Devices",
            value="0",
        )

        _, self.network_value_label = self.create_card(
            parent=self.dashboard_page,
            row=2,
            column=1,
            title="Network Range",
            value=self.network_info["network_range"],
        )

        _, self.gateway_value_label = self.create_card(
            parent=self.dashboard_page,
            row=2,
            column=2,
            title="Default Gateway",
            value=self.network_info["gateway"],
        )

        self.dashboard_results_frame = ctk.CTkFrame(
            self.dashboard_page,
        )
        self.dashboard_results_frame.grid(
            row=4,
            column=0,
            columnspan=3,
            sticky="nsew",
            pady=(24, 0),
        )

        self.dashboard_results_frame.grid_columnconfigure(
            0,
            weight=1,
        )
        self.dashboard_results_frame.grid_rowconfigure(
            1,
            weight=1,
        )

        results_heading = ctk.CTkLabel(
            self.dashboard_results_frame,
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

        self.dashboard_empty_message = ctk.CTkLabel(
            self.dashboard_results_frame,
            text=(
                "No scan results yet.\n"
                "Open Network Scan to discover devices."
            ),
            font=ctk.CTkFont(size=15),
            text_color="gray",
        )
        self.dashboard_empty_message.grid(
            row=1,
            column=0,
            pady=90,
        )

        self.dashboard_table = self.create_results_table(
            self.dashboard_results_frame
        )
        self.dashboard_table.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=20,
            pady=(5, 20),
        )
        self.dashboard_table.grid_remove()

    # ---------------------------------------------------------
    # Network Scan page
    # ---------------------------------------------------------

    def create_scan_page(self):
        self.scan_page = ctk.CTkFrame(
            self.page_container,
            fg_color="transparent",
            corner_radius=0,
        )
        self.scan_page.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=28,
            pady=25,
        )

        self.scan_page.grid_columnconfigure(0, weight=1)
        self.scan_page.grid_rowconfigure(4, weight=1)

        heading = ctk.CTkLabel(
            self.scan_page,
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
            self.scan_page,
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

        controls_frame = ctk.CTkFrame(
            self.scan_page,
        )
        controls_frame.grid(
            row=2,
            column=0,
            sticky="ew",
        )
        controls_frame.grid_columnconfigure(0, weight=1)

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

        self.network_range_entry = ctk.CTkEntry(
            controls_frame,
            height=42,
            placeholder_text="Example: 192.168.1.0/24",
        )
        self.network_range_entry.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(20, 10),
            pady=(0, 18),
        )

        self.network_range_entry.insert(
            0,
            self.network_info["network_range"],
        )

        self.start_scan_button = ctk.CTkButton(
            controls_frame,
            text="Start Scan",
            width=140,
            height=42,
            command=self.start_network_scan,
        )
        self.start_scan_button.grid(
            row=1,
            column=1,
            padx=(0, 20),
            pady=(0, 18),
        )

        status_frame = ctk.CTkFrame(
            self.scan_page,
            fg_color="transparent",
        )
        status_frame.grid(
            row=3,
            column=0,
            sticky="ew",
            pady=(14, 8),
        )
        status_frame.grid_columnconfigure(0, weight=1)

        self.scan_status_label = ctk.CTkLabel(
            status_frame,
            text="Ready to scan",
            text_color="gray",
        )
        self.scan_status_label.grid(
            row=0,
            column=0,
            sticky="w",
        )

        self.scan_progress = ctk.CTkProgressBar(
            status_frame,
            width=200,
            mode="indeterminate",
        )
        self.scan_progress.grid(
            row=0,
            column=1,
            sticky="e",
        )
        self.scan_progress.stop()
        self.scan_progress.grid_remove()

        results_frame = ctk.CTkFrame(
            self.scan_page,
        )
        results_frame.grid(
            row=4,
            column=0,
            sticky="nsew",
        )
        results_frame.grid_columnconfigure(0, weight=1)
        results_frame.grid_rowconfigure(1, weight=1)

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

        self.scan_table = self.create_results_table(results_frame)
        self.scan_table.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=20,
            pady=(5, 20),
        )

    # ---------------------------------------------------------
    # Reusable widgets
    # ---------------------------------------------------------

    def create_card(self, parent, row, column, title, value):
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

    def create_results_table(self, parent):
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

        table.heading(
            "status",
            text="Status",
        )
        table.heading(
            "ip_address",
            text="IP Address",
        )
        table.heading(
           "mac_address",
            text="MAC Address",
        )
        table.heading(
            "hostname",
            text="Hostname",
        )

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
    # Scanning
    # ---------------------------------------------------------

    def validate_network_range(self, network_range):
        try:
            network = ipaddress.ip_network(
                network_range,
                strict=False,
            )

        except ValueError:
            return None, "Please enter a valid network range."

        if network.version != 4:
            return None, "Only IPv4 networks are currently supported."

        if not network.is_private:
            return None, "Please use a private local network range."

        if network.num_addresses > 256:
            return (
                None,
                "For safety, NetScope currently scans a maximum "
                "of 256 addresses.",
            )

        return network, None

    def start_network_scan(self):
        network_range = self.network_range_entry.get().strip()

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
        self.network_range_entry.configure(state="disabled")

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
                lambda: self.handle_scan_error(str(error)),
            )

    def finish_network_scan(self, devices, network_range):
        self.discovered_devices = devices

        self.scan_progress.stop()
        self.scan_progress.grid_remove()

        self.start_scan_button.configure(
            state="normal",
            text="Start Scan",
        )
        self.network_range_entry.configure(state="normal")

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
                text="Scan complete — no online devices were found.",
                text_color="gray",
            )

            self.dashboard_table.grid_remove()
            self.dashboard_empty_message.configure(
                text="The latest scan found no online devices."
            )
            self.dashboard_empty_message.grid()

    def handle_scan_error(self, error_message):
        self.scan_progress.stop()
        self.scan_progress.grid_remove()

        self.start_scan_button.configure(
            state="normal",
            text="Start Scan",
        )
        self.network_range_entry.configure(state="normal")

        self.scan_status_label.configure(
            text=f"Scan failed: {error_message}",
            text_color="#ff6b6b",
        )

    def populate_table(self, table, devices):
        self.clear_table(table)

        for device in devices:
            table.insert(
                "",
                tk.END,
                values=(
                    device["status"],
                    device["ip_address"],
                    device["hostname"],
                ),
            )

    @staticmethod
    def clear_table(table):
        for row in table.get_children():
            table.delete(row)


if __name__ == "__main__":
    app = NetScopeApp()
    app.mainloop()