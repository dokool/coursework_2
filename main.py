import tkinter as tk
import turtle
import random
from l_system_2d import LSystem2D
import numba
import numpy as np
from PIL import Image
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
            "Главная": GreetingFrame(self),
            "Кривая Коха": KochCurve(self),
            "Дракон Хартера-Хейтуэя": DefaultLSystem2DClass(
                self, 90, 0, [('FX', "FX+FY+"), ('FY', "-FX-FY")],
                "FX", "7", "(700, 200)", 12),
            "Треугольник Серпинского": DefaultLSystem2DClass(
                self, 60, 180, [('F', "FF"), ('X', "--FXF++FXF++FXF--")],
                'FXF--FF--FF', "280 / (2 ** self.n_iter)", "(750, 10)", 9),
            "Кривая Гильберта": DefaultLSystem2DClass(
                self, 90, 90, [('X', "-YF+XFX+FY-"), ('Y', "+XF-YFY-FX+")],
                'X', "500 / (2 ** self.n_iter - 1)", "(225, 10)", 7),
            "Трава": DefaultLSystem2DClass(
                self, 10, 90, [('F', "F[+F]F[-F]F")], "F",
                "450 / (3 ** self.n_iter)", "(475, 30)", 6, True, 10, 50),
            "Куст": DefaultLSystem2DClass(
                self, 0, 90, [('F', "FF-[-F+F+F]+[+F-F-F]")], "F",
                "315 / (1.5 * 2.28 ** self.n_iter)", "(475, 10)",
                6, True, 10, 50),
            "Дерево": Tree(self),
            "Квадратичная кривая Коха": DefaultLSystem2DClass(
                self, 90, 0, [("F", "F-F+F+FFF-F-F+F")], 'F+F+F+F',
                "500 / (2 * 4 ** self.n_iter - 1)",
                "(350 + self.n_iter * 30, 80)"),
            "Кристал": DefaultLSystem2DClass(
                self, 90, 0, [("F", "FF+F++F+F")],
                "F+F+F+F", "495 / 3 ** self.n_iter", "(240, 10)", 6),
            "Кольцо": DefaultLSystem2DClass(
                self, 90, 0, [("F", "FF+F+F+F+F+F-F")],
                "F+F+F+F", "350 / 3.2 ** self.n_iter",
                "(330 + self.n_iter * 60, 15 * self.n_iter)", 4),
            "Множество Мандельброта": MandelbrotFractal(self),
            "Множество Жюлиа": JuliaFractal(self),
        }
        self.option_menu = ctk.CTkOptionMenu(
            master=self,
            values=list(self.frames.keys()),
            command=self.select_frame,
            anchor='center',
            font=ctk.CTkFont(size=20),
            dropdown_font=ctk.CTkFont(size=15)
        )
        self.option_menu.pack(side=tk.TOP, fill=tk.X, padx=20, pady=5)
        self.mainframe.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.select_frame('Главная')

    def start(self):
        self.mainloop()

    def select_frame(self, choice):
        self.mainframe.forget()
        self.mainframe = self.frames[choice]
        self.mainframe.tkraise()
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
        ).grid(column=0, row=1, pady=20, padx=20)
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
        )
        self.button.pack()

    def switch(self):
        if self.button._state == ctk.NORMAL:
            self.button._state = ctk.DISABLED
        else:
            self.button._state = ctk.NORMAL


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
        self.button = DrawButton(self.config, self._wrapper)

    def draw_curve(self):
        raise NotImplementedError

    def _wrapper(self):
        # self.button.switch()
        screen = self.turtle.getscreen()
        screen.setworldcoordinates(0, 0, screen.window_width() - 1,
                                   screen.window_height() - 1)
        self.turtle.clear()
        pen_width = 2
        self.n_iter = self.iterations.variable.get()
        self.rules_move = []
        self.draw_curve()
        if self.animation_switch.variable.get():
            screen.tracer(1, 1)
        else:
            screen.tracer(0, 0)
        self.turtle.ht()
        l_sys = LSystem2D(
            t=self.turtle,
            axiom=self.axiom,
            width=pen_width,
            length=self.f_len,
            angle=self.angle
        )
        l_sys.add_rules(*self.rules)
        if self.rules_move:
            l_sys.add_rules_move(*self.rules_move)
        l_sys.generate_path(self.n_iter)
        l_sys.draw_turtle(self.start_pos, self.start_angle)
        screen.update()
        # self.button.switch()


class DefaultLSystem2DClass(LSystem2DMainClass):

    def __init__(self, master, angle, start_angle, rules, axiom, f_len,
                 start_pos, iterations: int = 5, angle_slider: bool = 0,
                 angle_start: int = 0, angle_end: int = 180):
        super().__init__(master)
        self.iterations = SliderFrame(self.config, end=iterations)
        self.iterations.pack(fill=ctk.BOTH)
        if angle_slider:
            self.angle_frame = SliderFrame(self.config, start=10,
                                           end=50, text='Угол')
            self.angle_frame.pack(fill=ctk.BOTH, pady=20)
        self.animation_switch.pack(fill=ctk.BOTH, pady=20)
        self.button.pack(fill=ctk.BOTH)
        self.config.pack(fill=tk.BOTH, side=tk.LEFT)

        self.angle_slider = angle_slider
        self.angle_ = angle
        self.start_angle = start_angle
        self.rules = rules
        self.axiom = axiom
        self.f_len_ = f_len
        self.start_pos_ = start_pos

    def draw_curve(self):
        if self.angle_slider:
            self.angle = self.angle_frame.variable.get()
        else:
            self.angle = self.angle_
        self.f_len = eval(self.f_len_)
        self.start_pos = eval(self.start_pos_)


class KochCurve(LSystem2DMainClass):

    def __init__(self, master):
        super().__init__(master)
        self.iterations = SliderFrame(self.config)
        self.snowflake_switch = Switch(self.config, "Снежинка Коха")
        self.angle_frame = SliderFrame(self.config, start=60,
                                       end=90, text='Угол')
        self.iterations.pack(fill=ctk.BOTH)
        self.angle_frame.pack(fill=ctk.BOTH, pady=20)
        self.animation_switch.pack(fill=ctk.BOTH, pady=20)
        self.snowflake_switch.pack(fill=ctk.BOTH, pady=20)
        self.button.pack(fill=ctk.BOTH)
        self.config.pack(fill=tk.BOTH, side=tk.LEFT)

    def draw_curve(self):
        self.start_angle = 0
        self.rules = [('F', "F+F--F+F")]
        if self.snowflake_switch.variable.get():
            self.axiom = 'F--F--F'
            self.start_pos = (250, 380)
            self.f_len = 420 / (3 ** self.n_iter)
            self.angle = 60
            self.angle_frame.variable.set(60)
        else:
            self.axiom = "F"
            self.start_pos = (70, 20)
            self.angle = self.angle_frame.variable.get()
            n = np.sqrt(2 - 2 * np.cos(np.deg2rad(2 * (90 - self.angle))))
            self.f_len = 750 / ((2 + n) ** self.n_iter)


class Tree(LSystem2DMainClass):

    def __init__(self, master):
        super().__init__(master)
        self.iterations = SliderFrame(self.config, end=10)
        self.leaf_slider = SliderFrame(self.config, start=0,
                                       end=10, text='Листья')
        self.iterations.pack(fill=ctk.BOTH)
        self.leaf_slider.pack(fill=ctk.BOTH, pady=20)
        self.animation_switch.pack(fill=ctk.BOTH, pady=20)
        self.button.pack(fill=ctk.BOTH)
        self.config.pack(fill=tk.BOTH, side=tk.LEFT)

    def draw_curve(self):
        self.start_pos = (450, 10)
        self.start_angle = 90
        self.f_len = 20
        self.angle = 20
        self.axiom = "A"
        self.rules = [
            ("A", f"F(1, 1)[+({self.angle})A][-({self.angle})A]", 0.5),
            ("A", f"F(1, 1)[++({self.angle})A][+({self.angle})A]\
                    [-({self.angle})A][--({self.angle})A]", 0.4),
            ("A", f"F(1, 1)[-({self.angle})A]", 0.05),
            ("A", f"F(1, 1)[+({self.angle})A]", 0.05),
            ("F(x, y)", lambda x, y: f"F({(1.2+random.triangular(-0.5, 0.5, random.gauss(0, 1)))*x}, {1.4*y})"),
            ("+(x)", lambda x: f"+({x + random.triangular(-10, 10, random.gauss(0, 2))})"),
            ("-(x)", lambda x: f"-({x + random.triangular(-10, 10, random.gauss(0, 2))})"),
        ]
        self.rules_move = [
            ("F", self.cmd_turtle_fd),
            ("+", self.cmd_turtle_left),
            ("-", self.cmd_turtle_right),
            ('A', self.cmd_turtle_leaf),
        ]

    def cmd_turtle_fd(self, t, length, *args):
        t.pencolor('#30221A')
        t.pensize(args[1])
        t.fd(length*args[0])

    def cmd_turtle_left(self, t, angle, *args):
        t.left(args[0])

    def cmd_turtle_right(self, t, angle, *args):
        t.right(args[0])

    def cmd_turtle_leaf(self, t, length, *args):
        if random.random() > self.leaf_slider.variable.get() / 10:
            return
        s = t.pensize()
        t.pensize(5)
        p = random.randint(0, 2)
        match p:
            case 0:
                t.pencolor('#009900')
            case 1:
                t.pencolor('#667900')
            case _:
                t.pencolor('#20BB00')
        t.fd(length//2)
        t.pencolor("#000000")
        t.pensize(s)


class BSM2DMainClass(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)
        self.columnconfigure(0, weight=6)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.width, self.height = 920, 600
        self.c = 0
        self.screen_array = np.full((self.width, self.height, 3),
                                    [0, 0, 0], dtype=np.uint8)
        self.canvas_frame = ctk.CTkLabel(self, bg_color="#515151", text='',
                                         width=920, height=600)
        self.canvas_frame.pack(fill=ctk.BOTH, side=tk.LEFT)
        self.config = ctk.CTkFrame(self)
        self.move_left_button = ctk.CTkButton(self.config,
                                              command=self.move_left, text="⬅")
        self.move_right_button = ctk.CTkButton(self.config,
                                               command=self.move_right,
                                               text="➡")
        self.move_up_button = ctk.CTkButton(self.config,
                                            command=self.move_up, text="⬆")
        self.move_down_button = ctk.CTkButton(self.config,
                                              command=self.move_down, text="⬇")
        self.zoom_button = ctk.CTkButton(self.config,
                                         command=self.zoom_in, text="🔍")
        self.zoom_out_button = ctk.CTkButton(self.config,
                                             command=self.zoom_out,
                                             text="🔍out")
        self.move_left_button.pack()
        self.move_right_button.pack()
        self.move_up_button.pack()
        self.move_down_button.pack()
        self.zoom_button.pack()
        self.zoom_out_button.pack()
        self.button = DrawButton(self.config, self.redraw)
        self.button.pack(fill=ctk.BOTH, expand=True)
        self.config.pack(fill=ctk.BOTH, side=tk.LEFT, expand=True)

    def redraw(self):
        self.zoom = 2.2
        self.dx = 0.0
        self.dy = 0.0
        self.draw()

    def draw(self):
        self._draw_fractal()

    def move_left(self):
        self.dx += 0.4 * self.zoom
        self.draw()

    def move_right(self):
        self.dx -= 0.4 * self.zoom
        self.draw()

    def move_up(self):
        self.dy += 0.4 * self.zoom
        self.draw()

    def move_down(self):
        self.dy -= 0.4 * self.zoom
        self.draw()

    def zoom_in(self):
        self.zoom *= 0.5
        self.draw()

    def zoom_out(self):
        self.zoom /= 0.5
        self.draw()

    def _draw_fractal(self):
        image = self.render(self.screen_array, self.width, self.height,
                            self.zoom / self.height, self.dx, self.dy, self.c)
        img = Image.fromarray(image)
        imgtk = ctk.CTkImage(dark_image=img, size=(self.width, self.height))
        self.canvas_frame.configure(image=imgtk)

    @staticmethod
    @numba.njit(fastmath=True, parallel=True)
    def render(screen_array, width, height, zoom,
               dx, dy, C=None, max_iter=500):
        if C:
            bias = 1.0
        else:
            bias = 1.3
        offset = np.array([bias * width, height]) // 2
        for x in numba.prange(width):
            for y in numba.prange(height):
                if C:
                    z = (x - offset[0]) * zoom - dx +\
                        1j * ((y - offset[1]) * zoom - dy)
                    c = C
                else:
                    c = (x - offset[0]) * zoom - dx +\
                        1j * ((y - offset[1]) * zoom - dy)
                    z = 0
                n_iter = 0
                for i in numba.prange(max_iter):
                    z = z ** 2 + c
                    if z.real ** 2 + z.imag ** 2 >= 4:
                        break
                    n_iter += 1
                r = g = b = int(255 * n_iter / max_iter)
                # if n_iter == max_iter-1:
                #     r = g = b = 0
                # else:
                #     r = (n_iter % 2) * 32 + 128
                #     g = (n_iter % 4) * 64
                #     b = (n_iter % 2) * 16 + 128
                screen_array[x, y] = (r, g, b)
        return screen_array.transpose((1, 0, 2))


class MandelbrotFractal(BSM2DMainClass):

    def __init__(self, master):
        super().__init__(master)


class JuliaFractal(BSM2DMainClass):

    def __init__(self, master):
        super().__init__(master)

    def draw(self):
        self.c = complex(-1)
        self._draw_fractal()


if __name__ == "__main__":
    app = App()
    app.start()
