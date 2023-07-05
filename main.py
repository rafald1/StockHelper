import customtkinter as ctk

from gui_navigation_frame import NavigationFrame
from gui_data_frame import DataFrame
from gui_analysis_frame import AnalysisFrame
from gui_indicators_frame import IndicatorsFrame
from gui_strategy_frame import StrategyFrame
from manage_data import Stock


class App(ctk.CTk):
    def __init__(self, stock_data):
        super().__init__()

        self.title("Stock Helper")
        self.geometry("1440x810")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.data_frame = DataFrame(master=self, controller=self, stock_data=stock_data, corner_radius=0,
                                    fg_color="transparent")
        self.analysis_frame = AnalysisFrame(master=self, corner_radius=0, fg_color="transparent")
        self.indicators_frame = IndicatorsFrame(master=self, corner_radius=0, fg_color="transparent")
        self.strategy_frame = StrategyFrame(master=self, corner_radius=0, fg_color="transparent")

        self.nav_frame = NavigationFrame(master=self, controller=self, corner_radius=0)
        self.nav_frame.grid(row=0, column=0, sticky="nsew")
        self.nav_frame.grid_rowconfigure(5, weight=1)

    def show_frame(self, frame_name):
        if frame_name == "data":
            self.data_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.data_frame.grid_forget()
        if frame_name == "analysis":
            self.analysis_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.analysis_frame.grid_forget()
        if frame_name == "indicators":
            self.indicators_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.indicators_frame.grid_forget()
        if frame_name == "strategy":
            self.strategy_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.strategy_frame.grid_forget()

    def pass_analyse_class_object_created_from_prepared_data(self):
        analysis = self.data_frame.export_analysis_object()
        self.analysis_frame.import_analysis_object(analysis)
        self.indicators_frame.import_analysis_object(analysis)
        self.strategy_frame.import_analysis_object(analysis)


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    ctk.set_widget_scaling(1.25)

    stock = Stock()
    stock.read_stock_data_from_file()

    app = App(stock)
    app.mainloop()
