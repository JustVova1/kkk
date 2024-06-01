# main_app.py
import tkinter as tk
from tkinter import ttk
from File1 import MyApp as App1
from File2 import MyApp as App2
from ttkthemes import ThemedTk


class MainApplication(ThemedTk):  
    def __init__(self):
        super().__init__()

        self.set_theme("arc")  

        self.title("App")

        self.tab_control = ttk.Notebook(self)
        
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab2 = ttk.Frame(self.tab_control)
        
        self.tab_control.add(self.tab1, text="Регулярна прецесія")
        self.tab_control.add(self.tab2, text="Конічний рух")
        
        self.tab_control.pack(expand=1, fill="both")

        self.init_tabs()

    def init_tabs(self):
        App1(self.tab1).pack(expand=True, fill="both")
        App2(self.tab2).pack(expand=True, fill="both")

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
