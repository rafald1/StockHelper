import customtkinter as ctk


class AnalysisFrame(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.analysis = None

        # Percentage change
        self.anlys_frame_lbl_pct_change = ctk.CTkLabel(self, text="Percentage Change")
        self.anlys_frame_lbl_pct_change.grid(row=0, column=0, padx=20, pady=10)

        self.anlys_frame_lbl_session = ctk.CTkLabel(self, text="No. of Sessions")
        self.anlys_frame_lbl_session.grid(row=1, column=0, padx=20, pady=5)
        self.anlys_frame_combo_session = ctk.CTkComboBox(self, values=["1", "2", "3", "4", "5", "10", "20"])
        self.anlys_frame_combo_session.grid(row=2, column=0, padx=20, pady=5)
        self.anlys_frame_combo_session.set("2")

        self.anlys_frame_lbl_pct_decrease = ctk.CTkLabel(self, text="Percentage Decrease")
        self.anlys_frame_lbl_pct_decrease.grid(row=1, column=1, padx=20, pady=5)
        self.anlys_frame_combo_pct_decrease = ctk.CTkComboBox(
            self,
            values=["-4%", "-5%", "-6%", "-8%", "-10%", "-12%", "-15%", "-20%", "-25%"]
        )
        self.anlys_frame_combo_pct_decrease.set("-10%")
        self.anlys_frame_combo_pct_decrease.grid(row=2, column=1, padx=20, pady=5)

        self.anlys_frame_lbl_pct_increase = ctk.CTkLabel(self, text="Percentage Increase")
        self.anlys_frame_lbl_pct_increase.grid(row=1, column=2, padx=20, pady=5)
        self.anlys_frame_combo_pct_increase = ctk.CTkComboBox(
            self,
            values=["4%", "5%", "6%", "8%", "10%", "12%", "15%", "20%", "25%"]
        )
        self.anlys_frame_combo_pct_increase.set("10%")
        self.anlys_frame_combo_pct_increase.grid(row=2, column=2, padx=20, pady=5)

        self.anlys_frame_btn_pct_change = ctk.CTkButton(self, width=150, border_width=1,
                                                        fg_color="transparent", text_color=("gray10", "gray90"),
                                                        text="Find", command=self.pct_change_btn_event)
        self.anlys_frame_btn_pct_change.grid(row=2, column=3, padx=20, pady=5)

        self.separator = ctk.CTkProgressBar(self, height=2, progress_color="gray30")
        self.separator.grid(row=3, column=0, columnspan=4, padx=20, pady=(20, 5), sticky="ew")
        self.separator.set(100)

        # Gaps
        self.anlys_frame_lbl_gaps = ctk.CTkLabel(self, text="Gaps")
        self.anlys_frame_lbl_gaps.grid(row=4, column=0, padx=20, pady=10)

        self.anlys_frame_lbl_gaps_pct = ctk.CTkLabel(self, text="Percentage Change")
        self.anlys_frame_lbl_gaps_pct.grid(row=5, column=0, padx=20, pady=5)
        self.anlys_frame_combo_gaps_pct = ctk.CTkComboBox(self, values=["3%", "5%", "7%"])
        self.anlys_frame_combo_gaps_pct.grid(row=6, column=0, padx=20, pady=5)

        self.anlys_frame_lbl_gaps_session = ctk.CTkLabel(self, text="Shift Sessions by")
        self.anlys_frame_lbl_gaps_session.grid(row=5, column=1, padx=20, pady=5)
        self.anlys_frame_combo_gaps_session = ctk.CTkComboBox(self,
                                                              values=["0", "1", "2", "3", "4", "5", "10", "20"])
        self.anlys_frame_combo_gaps_session.grid(row=6, column=1, padx=20, pady=5)

        self.anlys_frame_btn_gaps = ctk.CTkButton(self, width=150, border_width=1,
                                                  fg_color="transparent", text_color=("gray10", "gray90"),
                                                  text="Find", command=self.gaps_btn_event)
        self.anlys_frame_btn_gaps.grid(row=6, column=3, padx=20, pady=5)

    def pct_change_btn_event(self):
        no_of_sessions = int(self.anlys_frame_combo_session.get())
        pct_decrease = int(self.anlys_frame_combo_pct_decrease.get().replace("%", ""))
        pct_increase = int(self.anlys_frame_combo_pct_increase.get().replace("%", ""))
        print(f"Change over {no_of_sessions} session(s) by {pct_decrease}% and {pct_increase}%\n"
              f"{self.analysis.stock_price_pct_change(no_of_sessions, pct_decrease, pct_increase)}\n")
        # with open("output.txt", mode="w") as output:
        #     output.write(a.stock_price_pct_change(no_of_sessions, pct_decrease, pct_increase))

    def gaps_btn_event(self):
        pct_change = int(self.anlys_frame_combo_gaps_pct.get().replace("%", ""))
        session_shift = int(self.anlys_frame_combo_gaps_session.get())
        print(f"Gaps over -{pct_change}% and {pct_change}%. Last session shifted by {session_shift} session(s)\n"
              f"{self.analysis.looking_for_gaps(pct_change, session_shift)}\n")

    def import_analysis_object(self, analysis):
        self.analysis = analysis
