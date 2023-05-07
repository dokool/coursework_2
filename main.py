import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt


class App(tk.Tk):
    """_summary_

    :param _type_ tk: _description_
    """
    def __init__(self):
        super().__init__()

        self.title("Фракталы")
        self.geometry("1200x600")
        self.resizable(True, True)

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
