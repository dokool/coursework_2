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
            "Дракон Хартера-Хейтуэя": HarterHatewayDragon,
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


class SliderFrame(ctk.CTkFrame):

    def __init__(self, master, start=1, end=9, text='Итераций:'):
        super().__init__(master)
        self.columnconfigure(0, weight=4)
        self.columnconfigure(1, weight=1)
        self.variable = ctk.IntVar(self, start)
        self.iterations_label = ctk.CTkLabel(
            self,
            text=text,
            font=ctk.CTkFont(size=20)
        ).grid(column=0, row=0, columnspan=2, pady=20)
        self.slider = ctk.CTkSlider(
            self,
            from_=start,
            to=end,
            variable=self.variable,
            number_of_steps=end-start+1,
        ).grid(column=0, row=1, ipadx=20, pady=20)
        self.label = ctk.CTkEntry(
            self,
            textvariable=self.variable,
            font=ctk.CTkFont(size=20),
            state=ctk.DISABLED,
            width=40
        ).grid(column=1, row=1)


class Switch(ctk.CTkFrame):

    def __init__(self, master, text):
        super().__init__(master)
        self.variable = ctk.BooleanVar(self, value=False)
        self.switch = ctk.CTkSwitch(
            self,
            text=text,
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


class LSystem2DMainClass(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)
        self.columnconfigure(0, weight=6)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.canvas = tk.Canvas(self, width=900, height=600)
        self.canvas.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
        self.turtle = turtle.RawTurtle(self.canvas)
        self.turtle.ht()
        self.config = ctk.CTkFrame(self)
        self.animation_switch = Switch(self.config, "Анимация")
        self.button = DrawButton(self.config, self.draw_curve)

    def draw_curve(self):
        raise NotImplementedError


class KochCurve(LSystem2DMainClass):

    def __init__(self, master):
        super().__init__(master)
        self.iterations = SliderFrame(self.config)
        self.snowflake_switch = Switch(self.config, "Снежинка Коха")
        self.angle = SliderFrame(self.config, start=60, end=90, text='Угол')
        self.iterations.pack(fill=ctk.BOTH)
        self.angle.pack(fill=ctk.BOTH, pady=20)
        self.animation_switch.pack(fill=ctk.BOTH, pady=20)
        self.snowflake_switch.pack(fill=ctk.BOTH, pady=20)
        self.button.pack(fill=ctk.BOTH)
        self.config.pack(fill=tk.BOTH, side=tk.LEFT)

    def draw_curve(self):
        screen = self.turtle.getscreen()
        screen.setworldcoordinates(0, 0, screen.window_width() - 1,
                                   screen.window_height() - 1)
        self.turtle.clear()
        pen_width = 2
        n_iter = self.iterations.variable.get()
        if self.snowflake_switch.variable.get():
            axiom = 'F--F--F'
            start_pos = (250, 380)
            f_len = 420 / (3 ** n_iter)
            angle = 60
            self.angle.variable.set(60)
        else:
            axiom = "F"
            start_pos = (70, 20)
            angle = self.angle.variable.get()
            n = np.sqrt(2 - 2 * np.cos(np.deg2rad(2 * (90 - angle))))
            f_len = 750 / ((2 + n) ** n_iter)
        if self.animation_switch.variable.get():
            screen.tracer(5, 0)
        else:
            if n_iter <= 4:
                screen.tracer(10, 10)
            else:
                screen.tracer(0, 0)
                #self.turtle._tracer(0, 0)
        self.turtle.ht()
        l_sys = LSystem2D(
            t=self.turtle,
            axiom=axiom,
            width=pen_width,
            length=f_len,
            angle=angle
        )
        l_sys.add_rules(('F', "F+F--F+F"))
        l_sys.generate_path(n_iter)
        l_sys.draw_turtle(start_pos, 0)
        screen.update()


class HarterHatewayDragon(LSystem2DMainClass):

    def __init__(self, master):
        super().__init__(master)
        self.iterations = SliderFrame(self.config, end=15)
        self.iterations.pack(fill=ctk.BOTH)
        self.animation_switch.pack(fill=ctk.BOTH, pady=20)
        self.button.pack(fill=ctk.BOTH)
        self.config.pack(fill=tk.BOTH, side=tk.LEFT)

    def draw_curve(self):
        screen = self.turtle.getscreen()
        screen.setworldcoordinates(0, 0, screen.window_width() - 1,
                                   screen.window_height() - 1)
        self.turtle.clear()
        pen_width = 2
        angle = 90
        axiom = 'FX'
        n_iter = self.iterations.variable.get()
        #ls = [0, 0.125, 0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        f_len = 10
        start_pos = (700, 100)
        if self.animation_switch.variable.get():
            screen.tracer(5, 5)
        else:
            if n_iter <= 4:
                screen.tracer(10, 0)
            else:
                self.turtle._tracer(0, 0)
        self.turtle.ht()
        l_sys = LSystem2D(
            t=self.turtle,
            axiom=axiom,
            width=pen_width,
            length=f_len,
            angle=angle
        )
        l_sys.add_rules(('FX', "FX+FY+"),
                        ('FY', "-FX-FY"))
        l_sys.generate_path(n_iter)
        l_sys.draw_turtle(start_pos, 0)
        screen.update()


if __name__ == "__main__":
    app = App()
    app.start()
