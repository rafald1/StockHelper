import customtkinter as ctk


class IndicatorsFrame(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.analysis = None

        self.macd_lbl = ctk.CTkLabel(self, text="MACD", anchor="w")
        self.macd_lbl.grid(row=0, column=0, sticky="ew", padx=20, pady=(10, 5))

        self.macd_pct_distance_lbl = ctk.CTkLabel(self, text="Percentage Distance")
        self.macd_pct_distance_lbl.grid(row=1, column=0, padx=20, pady=5)
        self.macd_pct_distance_combo = ctk.CTkComboBox(
            self,
            values=["0.5%", "1%", "1.5%", "2%", "3%", "4%", "5%"]
        )
        self.macd_pct_distance_combo.set("1%")
        self.macd_pct_distance_combo.grid(row=2, column=0, padx=20, pady=5)

        self.macd_session_shift_lbl = ctk.CTkLabel(self, text="Shift Sessions by")
        self.macd_session_shift_lbl.grid(row=1, column=1, padx=20, pady=5)
        self.macd_session_shift_combo = ctk.CTkComboBox(self, values=["0", "1", "2", "3", "4", "5", "10", "20"])
        self.macd_session_shift_combo.grid(row=2, column=1, padx=20, pady=5)

        self.macd_btn = ctk.CTkButton(self, width=150, border_width=1, fg_color="transparent",
                                      text_color=("gray10", "gray90"), text="Find", command=self.macd_btn_event)
        self.macd_btn.grid(row=2, column=3, padx=20, pady=5)

        self.separator_1 = ctk.CTkProgressBar(self, height=2, progress_color="gray30")
        self.separator_1.grid(row=3, column=0, columnspan=4, padx=20, pady=(20, 5), sticky="ew")
        self.separator_1.set(100)

        self.rsi_lbl = ctk.CTkLabel(self, text="RSI", anchor="w")
        self.rsi_lbl.grid(row=4, column=0, sticky="ew", padx=20, pady=(10, 5))

        self.rsi_low_lbl = ctk.CTkLabel(self, text="Low")
        self.rsi_low_lbl.grid(row=5, column=0, padx=20, pady=5)
        self.rsi_low_combo = ctk.CTkComboBox(
            self,
            values=["25", "30", "35", "40", "45", "50"]
        )
        self.rsi_low_combo.set("40")
        self.rsi_low_combo.grid(row=6, column=0, padx=20, pady=5)

        self.rsi_high_lbl = ctk.CTkLabel(self, text="High")
        self.rsi_high_lbl.grid(row=5, column=1, padx=20, pady=5)
        self.rsi_high_combo = ctk.CTkComboBox(
            self,
            values=["65", "70", "75", "80", "85"]
        )
        self.rsi_high_combo.set("70")
        self.rsi_high_combo.grid(row=6, column=1, padx=20, pady=5)

        self.rsi_session_shift_lbl = ctk.CTkLabel(self, text="Shift Sessions by")
        self.rsi_session_shift_lbl.grid(row=5, column=2, padx=20, pady=5)
        self.rsi_session_shift_combo = ctk.CTkComboBox(self, values=["0", "1", "2", "3", "4", "5", "10", "20"])
        self.rsi_session_shift_combo.grid(row=6, column=2, padx=20, pady=5)

        self.rsi_btn = ctk.CTkButton(self, width=150, border_width=1, fg_color="transparent",
                                     text_color=("gray10", "gray90"), text="Find", command=self.rsi_btn_event)
        self.rsi_btn.grid(row=6, column=3, padx=20, pady=5)

        self.separator_2 = ctk.CTkProgressBar(self, height=2, progress_color="gray30")
        self.separator_2.grid(row=7, column=0, columnspan=4, padx=20, pady=(20, 5), sticky="ew")
        self.separator_2.set(100)

        self.adx_lbl = ctk.CTkLabel(self, text="ADX", anchor="w")
        self.adx_lbl.grid(row=8, column=0, sticky="ew", padx=20, pady=(10, 5))

        self.adx_session_shift_lbl = ctk.CTkLabel(self, text="Shift Sessions by")
        self.adx_session_shift_lbl.grid(row=9, column=0, padx=20, pady=5)
        self.adx_session_shift_combo = ctk.CTkComboBox(self, values=["0", "1", "2", "3", "4", "5", "10", "20"])
        self.adx_session_shift_combo.grid(row=10, column=0, padx=20, pady=5)

        self.adx_btn = ctk.CTkButton(self, width=150, border_width=1, fg_color="transparent",
                                     text_color=("gray10", "gray90"), text="Find", command=self.adx_btn_event)
        self.adx_btn.grid(row=10, column=3, padx=20, pady=5)

    def macd_btn_event(self):
        pct_distance = float(self.macd_pct_distance_combo.get().replace("%", ""))
        session_shift = int(self.macd_session_shift_combo.get())
        print(self.analysis.calculate_macd(pct_distance=pct_distance, session_shift=session_shift))

    def rsi_btn_event(self):
        low = int(self.rsi_low_combo.get())
        high = int(self.rsi_high_combo.get())
        session_shift = int(self.rsi_session_shift_combo.get())
        print(self.analysis.calculate_rsi(low_rsi=low, high_rsi=high, session_shift=session_shift))

    def adx_btn_event(self):
        session_shift = int(self.adx_session_shift_combo.get())
        print(self.analysis.calculate_adx(session_shift=session_shift))

    def import_analysis_object(self, analysis):
        self.analysis = analysis
