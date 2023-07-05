import customtkinter as ctk


class NavigationFrame(ctk.CTkFrame):
    def __init__(self, master, controller, **kwargs):
        ctk.CTkFrame.__init__(self, master, **kwargs)

        self.controller = controller

        self.nav_frame_lbl = ctk.CTkLabel(self, text="(ノ-_-)ノ ミ ┴┴", font=ctk.CTkFont(size=15, weight="bold"))
        self.nav_frame_lbl.grid(row=0, column=0, padx=20, pady=20)

        self.data_button = ctk.CTkButton(self, corner_radius=0, height=40, border_spacing=10,
                                         text="Data", fg_color="transparent",
                                         text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                         anchor="w", command=self.data_button_event)
        self.data_button.grid(row=1, column=0, sticky="ew")

        self.analysis_button = ctk.CTkButton(self, corner_radius=0, height=40, border_spacing=10,
                                             text="Analysis", fg_color="transparent",
                                             text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                             anchor="w", command=self.analysis_button_event)
        self.analysis_button.grid(row=2, column=0, sticky="ew")

        self.indicators_button = ctk.CTkButton(self, corner_radius=0, height=40, border_spacing=10,
                                               text="Indicators", fg_color="transparent",
                                               text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                               anchor="w", command=self.indicators_button_event)
        self.indicators_button.grid(row=3, column=0, sticky="ew")

        self.strategy_button = ctk.CTkButton(self, corner_radius=0, height=40, border_spacing=10,
                                             text="Strategy", fg_color="transparent",
                                             text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                             anchor="w", command=self.strategy_button_event)
        self.strategy_button.grid(row=4, column=0, sticky="ew")

        self.appearance_mode_menu = ctk.CTkOptionMenu(self, values=["Dark", "Light"],
                                                      command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=5, column=0, padx=10, pady=10, sticky="s")

        self.scaling_menu = ctk.CTkOptionMenu(self, values=["75%", "100%", "125%", "150%", "200%"],
                                              command=self.change_scaling_event)
        self.scaling_menu.grid(row=6, column=0, padx=10, pady=(10, 20))
        self.scaling_menu.set("125%")

        self.select_frame_by_name("data")

    def select_frame_by_name(self, frame_name):
        # set button color for selected button
        self.data_button.configure(fg_color=("gray75", "gray25") if frame_name == "data" else "transparent")
        self.analysis_button.configure(fg_color=("gray75", "gray25") if frame_name == "analysis" else "transparent")
        self.indicators_button.configure(fg_color=("gray75", "gray25") if frame_name == "indicators" else "transparent")
        self.strategy_button.configure(fg_color=("gray75", "gray25") if frame_name == "strategy" else "transparent")

        self.controller.show_frame(frame_name)

    def data_button_event(self):
        self.select_frame_by_name("data")

    def analysis_button_event(self):
        self.select_frame_by_name("analysis")

    def indicators_button_event(self):
        self.select_frame_by_name("indicators")

    def strategy_button_event(self):
        self.select_frame_by_name("strategy")

    @staticmethod
    def change_appearance_mode_event(new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)

    @staticmethod
    def change_scaling_event(new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)
