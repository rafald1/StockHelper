import customtkinter as ctk


class StrategyFrame(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.analysis = None

        self.data_frame_lbl = ctk.CTkLabel(self, text="STRATEGY")
        self.data_frame_lbl.grid(row=0, column=0, padx=20, pady=10)

    def import_analysis_object(self, analysis):
        self.analysis = analysis
