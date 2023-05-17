import tkinter as tk
import turtle
from l_system_2d import LSystem2D
import numpy as np
import matplotlib.pyplot as plt
import customtkinter as ctk


class App(ctk.CTk):
    """_summary_

    :param _type_ tk: _description_
    """
    def __init__(self):
        super().__init__()

        self.title("Фракталы")
        self.geometry("1200x600")
        self.resizable(True, True)

        self.mainframe = ctk.CTkFrame(self)
        self.frames = {
            "Главная": GreetingFrame,
            "Кривая Коха": KochCurve,
            "2": GreetingFrame,
        }
        self.option_menu = ctk.CTkOptionMenu(
            master=self,
            values=list(self.frames.keys()),
            command=self.select_frame,
            anchor='center',
            font=ctk.CTkFont(size=20)
        )
        self.option_menu.pack(side=tk.TOP, fill=tk.X, padx=20, pady=5)
        self.mainframe.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.select_frame('Главная')
        # self.canvas = CanvasFrame(self)
        # self.canvas.pack(side=tk.LEFT)
        # self.config = ConfigurationFrame()
        # self.config.pack(side=tk.RIGHT)

    def start(self):
        self.mainloop()

    def select_frame(self, choice):
        self.mainframe.destroy()
        self.mainframe = self.frames[choice](self)
        self.mainframe.pack(expand=True, fill=tk.BOTH)


class GreetingFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)
        text = """
Курсовая работа
Студента БПИз-21 Муратова Владислава Азаматовича
Тема "Фракталы в науке"
        """
        self.greeteing_label = ctk.CTkLabel(self, text=text)
        self.greeteing_label.pack(fill=tk.BOTH, expand=True)


class CanvasFrame(ctk.CTkCanvas):

    def __init__(self, master):
        super().__init__(master)
        #self.config()
        # self.screen.bgcolor('cyan')
        self.turtle = turtle.RawTurtle(self)
        #self.turtle.ht()


class IterationsFrame(ctk.CTkFrame):

    def __init__(self, master, start=1, end=9):
        super().__init__(master)
        self.columnconfigure(0, weight=4)
        self.columnconfigure(1, weight=1)
        self.n_iters = ctk.IntVar(self, 1)
        self.iterations_label = ctk.CTkLabel(
            self,
            text='Итераций:',
            font=ctk.CTkFont(size=20)
        ).grid(column=0, row=0, columnspan=2, pady=20)
        self.iterations_slider = ctk.CTkSlider(
            self,
            from_=start,
            to=end,
            variable=self.n_iters,
            number_of_steps=end-start+1,
            # command=self.slider_event
        ).grid(column=0, row=1, ipadx=20, pady=20)
        self.slider_label = ctk.CTkEntry(
            self,
            textvariable=self.n_iters,
            font=ctk.CTkFont(size=20),
            state=ctk.DISABLED,
            width=40
        ).grid(column=1, row=1)


class AnimationSwitch(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)
        self.variable = ctk.BooleanVar(self, value=True)
        self.animation = ctk.CTkSwitch(
            self,
            text='Анимация',
            font=ctk.CTkFont(size=20),
            variable=self.variable
        ).pack()


class DrawButton(ctk.CTkFrame):

    def __init__(self, master, command):
        super().__init__(master)
        self.button = ctk.CTkButton(
            self,
            text="Построить",
            font=ctk.CTkFont(size=20),
            command=command
        ).pack()


class KochCurve(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)
        self.columnconfigure(0, weight=6)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        #self.canvas = CanvasFrame(self)
        #self.canvas.grid(column=0, row=0, sticky='wens')
        self.canvas = tk.Canvas(self)
        self.canvas.grid(column=0, row=0, sticky='wens')
        self.turtle = turtle.RawTurtle(self.canvas)
        self.config = ctk.CTkFrame(self)
        self.iterations = IterationsFrame(self.config)
        self.iterations.pack(fill=ctk.BOTH)
        self.animation_switch = AnimationSwitch(self.config)
        self.animation_switch.pack(fill=ctk.BOTH, pady=20)
        self.button = DrawButton(self.config, self.draw_curve)
        self.button.pack(fill=ctk.BOTH)
        self.config.grid(column=1, row=0, sticky="wens")
        

    def draw_curve(self):
        pen_width = 2
        f_len = 10
        angle = 60
        axiom = 'F'
        n_iter = self.iterations.n_iters.get()
        t = self.turtle
        #t._tracer(0, 0)
        t._tracer(0, 0)
        l_sys = LSystem2D(
            t=t,
            axiom=axiom,
            width=pen_width,
            length=f_len,
            angle=angle
        )
        screen = t.getscreen()
        #screen.reset()
        t.ht()
        screen.setworldcoordinates(-1, -1, screen.window_width() - 1, screen.window_height() - 1)
        l_sys.add_rules(('F', "F+F--F+F"))
        l_sys.generate_path(n_iter)
        print(t.pos())
        l_sys.draw_turtle((0, 0), 0)

        #self.turtle.forward(10)


if __name__ == "__main__":
    app = App()
    app.start()
