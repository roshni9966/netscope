import customtkinter as ctk


class NetScopeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window settings
        self.title("NetScope")
        self.geometry("1100x700")
        self.minsize(900, 600)

        # Theme settings
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Configure main window layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_sidebar()
        self.create_dashboard()

    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self,
            width=220,
            corner_radius=0
        )
        self.sidebar.grid(
            row=0,
            column=0,
            sticky="nsew"
        )
        self.sidebar.grid_propagate(False)

        self.logo_label = ctk.CTkLabel(
            self.sidebar,
            text="NetScope",
            font=ctk.CTkFont(
                size=26,
                weight="bold"
            )
        )
        self.logo_label.pack(
            padx=20,
            pady=(35, 40)
        )

        self.dashboard_button = ctk.CTkButton(
            self.sidebar,
            text="Dashboard",
            height=42
        )
        self.dashboard_button.pack(
            padx=20,
            pady=8,
            fill="x"
        )

        self.scan_button = ctk.CTkButton(
            self.sidebar,
            text="Network Scan",
            height=42,
            fg_color="transparent",
            border_width=1
        )
        self.scan_button.pack(
            padx=20,
            pady=8,
            fill="x"
        )

        self.port_button = ctk.CTkButton(
            self.sidebar,
            text="Port Scanner",
            height=42,
            fg_color="transparent",
            border_width=1
        )
        self.port_button.pack(
            padx=20,
            pady=8,
            fill="x"
        )

        self.about_button = ctk.CTkButton(
            self.sidebar,
            text="About",
            height=42,
            fg_color="transparent",
            border_width=1
        )
        self.about_button.pack(
            padx=20,
            pady=8,
            fill="x"
        )

        self.version_label = ctk.CTkLabel(
            self.sidebar,
            text="Version 1.0",
            text_color="gray"
        )
        self.version_label.pack(
            side="bottom",
            pady=20
        )

    def create_dashboard(self):
        self.main_frame = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color="transparent"
        )
        self.main_frame.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=30,
            pady=30
        )

        self.main_frame.grid_columnconfigure(
            (0, 1, 2),
            weight=1
        )
        self.main_frame.grid_rowconfigure(
            2,
            weight=1
        )

        self.heading_label = ctk.CTkLabel(
            self.main_frame,
            text="Network Dashboard",
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        )
        self.heading_label.grid(
            row=0,
            column=0,
            columnspan=3,
            sticky="w",
            pady=(0, 5)
        )

        self.subtitle_label = ctk.CTkLabel(
            self.main_frame,
            text="Monitor and explore devices on your local network.",
            font=ctk.CTkFont(size=15),
            text_color="gray"
        )
        self.subtitle_label.grid(
            row=1,
            column=0,
            columnspan=3,
            sticky="w",
            pady=(0, 25)
        )

        self.devices_card = self.create_card(
            column=0,
            title="Online Devices",
            value="0"
        )

        self.network_card = self.create_card(
            column=1,
            title="Network Range",
            value="Not detected"
        )

        self.gateway_card = self.create_card(
            column=2,
            title="Default Gateway",
            value="Not detected"
        )

        self.results_frame = ctk.CTkFrame(
            self.main_frame
        )
        self.results_frame.grid(
            row=3,
            column=0,
            columnspan=3,
            sticky="nsew",
            pady=(25, 0)
        )

        self.results_frame.grid_columnconfigure(
            0,
            weight=1
        )
        self.results_frame.grid_rowconfigure(
            1,
            weight=1
        )

        self.results_title = ctk.CTkLabel(
            self.results_frame,
            text="Recent Scan Results",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        )
        self.results_title.grid(
            row=0,
            column=0,
            sticky="w",
            padx=20,
            pady=(20, 10)
        )

        self.empty_message = ctk.CTkLabel(
            self.results_frame,
            text="No scan results yet.\nStart a network scan to discover devices.",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        self.empty_message.grid(
            row=1,
            column=0,
            pady=100
        )

    def create_card(self, column, title, value):
        card = ctk.CTkFrame(
            self.main_frame,
            height=130
        )
        card.grid(
            row=2,
            column=column,
            sticky="nsew",
            padx=8
        )
        card.grid_propagate(False)

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        title_label.pack(
            anchor="w",
            padx=20,
            pady=(20, 8)
        )

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        )
        value_label.pack(
            anchor="w",
            padx=20
        )

        return card


if __name__ == "__main__":
    app = NetScopeApp()
    app.mainloop()