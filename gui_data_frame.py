import datetime as dt
import pandas as pd
import customtkinter as ctk

from data_analysis import Analysis


class DataFrame(ctk.CTkFrame):
    def __init__(self, master, controller, stock_data, **kwargs):
        super().__init__(master, **kwargs)

        self.controller = controller
        self.stock_data = stock_data
        self.analysis = None

        df_shape = self.stock_data.df_original.shape
        last_session_date = self.stock_data.df_original.index[-1].date()
        self.data_frame_lbl_1 = ctk.CTkLabel(self, text=f"Stock data contains {df_shape[1]} columns and {df_shape[0]}"
                                                        f" rows.", anchor="w")
        self.data_frame_lbl_1.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=(10, 5))

        self.data_frame_lbl_2 = ctk.CTkLabel(self, text=f"Last session data is from "
                                                        f"{last_session_date}.", anchor="w")
        self.data_frame_lbl_2.grid(row=1, column=0, columnspan=2, sticky="ew", padx=20, pady=5)

        self.separator_1 = ctk.CTkProgressBar(self, height=2, progress_color="gray30")
        self.separator_1.grid(row=2, column=0, columnspan=4, padx=20, pady=(20, 5), sticky="ew")
        self.separator_1.set(100)

        self.data_frame_lbl_3 = ctk.CTkLabel(self, text="Fetch new data", anchor="w")
        self.data_frame_lbl_3.grid(row=3, column=0, columnspan=2, sticky="ew", padx=20, pady=(10, 5))

        self.data_frame_start_date_lbl = ctk.CTkLabel(self, text="Start Date", anchor="w")
        self.data_frame_start_date_lbl.grid(row=4, column=0, sticky="ew", padx=20, pady=5)
        self.data_frame_entry_1 = ctk.CTkEntry(self)
        self.data_frame_entry_1.grid(row=5, column=0, padx=20, pady=5)
        self.data_frame_entry_1.insert(0, last_session_date + dt.timedelta(days=1))

        self.data_frame_end_date_lbl = ctk.CTkLabel(self, text="End Date", anchor="w")
        self.data_frame_end_date_lbl.grid(row=4, column=1, sticky="ew", padx=20, pady=5)
        self.data_frame_entry_2 = ctk.CTkEntry(self)
        self.data_frame_entry_2.grid(row=5, column=1, padx=20, pady=5)
        self.data_frame_entry_2.insert(0, dt.date.today())

        self.data_frame_btn_fetch_data = ctk.CTkButton(self, width=150, border_width=1,
                                                       fg_color="transparent", text_color=("gray10", "gray90"),
                                                       text="Fetch New Data", command=self.fetch_data_btn_event)
        self.data_frame_btn_fetch_data.grid(row=5, column=3, padx=20, pady=5)

        self.separator_2 = ctk.CTkProgressBar(self, height=2, progress_color="gray30")
        self.separator_2.grid(row=6, column=0, columnspan=4, padx=20, pady=(20, 5), sticky="ew")
        self.separator_2.set(100)

        self.data_frame_prepare_lbl = ctk.CTkLabel(self, text="Prepare Data for Analysis", anchor="w")
        self.data_frame_prepare_lbl.grid(row=7, column=0, columnspan=2, sticky="ew", padx=20, pady=(10, 5))

        self.data_frame_prepare_start_date_lbl = ctk.CTkLabel(self, text="Start Date", anchor="w")
        self.data_frame_prepare_start_date_lbl.grid(row=8, column=0, sticky="ew", padx=20, pady=5)
        self.data_frame_prepare_start_date_entry = ctk.CTkEntry(self)
        self.data_frame_prepare_start_date_entry.grid(row=9, column=0, padx=20, pady=5)
        self.data_frame_prepare_start_date_entry.insert(0, (dt.date.today() - pd.DateOffset(months=3)).date())

        self.data_frame_prepare_end_date_lbl = ctk.CTkLabel(self, text="End Date", anchor="w")
        self.data_frame_prepare_end_date_lbl.grid(row=8, column=1, sticky="ew", padx=20, pady=5)
        self.data_frame_prepare_end_date_entry = ctk.CTkEntry(self)
        self.data_frame_prepare_end_date_entry.grid(row=9, column=1, padx=20, pady=5)
        self.data_frame_prepare_end_date_entry.insert(0, dt.date.today())

        self.data_frame_prepare_pct_missing_lbl = ctk.CTkLabel(self, text="Percentage of Missing Data")
        self.data_frame_prepare_pct_missing_lbl.grid(row=8, column=2, padx=20, pady=5)
        self.data_frame_prepare_pct_missing_combo = ctk.CTkComboBox(
            self,
            values=["0%", "1%", "2%", "3%", "4%", "5%", "7%", "10%", "15%", "25%", "50%"]
        )
        self.data_frame_prepare_pct_missing_combo.set("5%")
        self.data_frame_prepare_pct_missing_combo.grid(row=9, column=2, padx=20, pady=5)

        self.data_frame_btn_fetch_data = ctk.CTkButton(self, width=150, border_width=1,
                                                       fg_color="transparent", text_color=("gray10", "gray90"),
                                                       text="Prepare Data", command=self.prepare_data_btn_event)
        self.data_frame_btn_fetch_data.grid(row=9, column=3, padx=20, pady=5)

    def fetch_data_btn_event(self):
        start_date = self.validate_if_date(self.data_frame_entry_1.get())
        end_date = self.validate_if_date(self.data_frame_entry_2.get())

        if start_date is not None and end_date is not None:
            if start_date <= end_date:
                # TODO: Warning popup
                self.stock_data.fetch_new_data_and_update(start_date=start_date, end_date=end_date)
                self.stock_data.write_stock_date_to_file()

    def prepare_data_btn_event(self):
        start_date = self.validate_if_date(self.data_frame_prepare_start_date_entry.get())
        end_date = self.validate_if_date(self.data_frame_prepare_end_date_entry.get())
        missing_data_pct = self.validate_if_float(self.data_frame_prepare_pct_missing_combo.get().replace("%", ""))

        if start_date is not None and end_date is not None and missing_data_pct is not None:
            self.stock_data.prepare_data(start_date=start_date, end_date=end_date,
                                         missing_data_percentage_cutoff=missing_data_pct)

            self.analysis = Analysis(self.stock_data.df)
            self.controller.pass_analyse_class_object_created_from_prepared_data()

    def export_analysis_object(self):
        return self.analysis

    @staticmethod
    def validate_if_date(value):
        try:
            value = pd.Timestamp(value).date()
        except ValueError:
            print("ValueError: Entered value could not be converted to Timestamp object")
            return None
        else:
            if pd.isnull(value):
                return None
            return value

    @staticmethod
    def validate_if_float(value):
        try:
            value = float(value)
        except ValueError:
            print("ValueError: Entered value could not be converted to Float")
            return None
        else:
            return value
