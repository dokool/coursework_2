import tkinter as tk
import turtle
import random
import re
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
            "Фрактал Вичека": DefaultLSystem2DClass(
                self, 90, 90, [("F", "F-F+F+F-F")],
                "F-F-F-F", "480 / (3 ** self.n_iter)", "(225, 10)"),
            "Кривая Леви": DefaultLSystem2DClass(
                self, 45, 0, [("F", "+F--F+")], "F",
                "650 / (1.5 ** self.n_iter)",
                "(130 + 15 * self.n_iter, 60 + 5 * self.n_iter)",
                iterations=14),
            "Кривая Серпинского": DefaultLSystem2DClass(
                self, 90, 0, [("X", "XF-F+F-XF+F+XF-F+F-X")],
                "F+XF+F+XF", "[100, 38.5, 17.26, 8.22, 4.01][self.n_iter-1]",
                "(425, 10)"),
            "Кривая Пеано-Госпера": DefaultLSystem2DClass(
                self, 60, 0,
                [("X", "X+YF++YF-FX--FXFX-YF+"),
                 ("Y", "-FX+YFYF++YF+FX--FX-Y")],
                "FX", "600 / (2.9 ** self.n_iter)",
                "(300 + 30 * self.n_iter, 10)",
                iterations=4),
            "Пентаплекс": DefaultLSystem2DClass(
                self, 36, 0, [("F", "F++F++F+++++F-F++F")],
                "F++F++F++F++F", "325 / (2.6 ** self.n_iter)", "(320, 10)"),
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


class LSystem2D:
    def __init__(self, t, axiom, width, length, angle):
        self.axiom = axiom
        self.state = axiom
        self.width = width
        self.length = length
        self.angle = angle
        self.t = t
        self.rules = {}
        self.t.pensize(self.width)
        self.rules_key = None
        self.key_re_list = []
        self.cmd_functions = {}

    def add_rules(self, *rules):
        for r in rules:
            p = 1
            if len(r) == 3:
                key, value, p = r
            else:
                key, value = r

            key_re = key.replace("(", r"\(")
            key_re = key_re.replace(")", r"\)")
            key_re = key_re.replace("+", r"\+")
            key_re = key_re.replace("-", r"\-")

            if not isinstance(value, str):
                key_re = re.sub(r"([a-z]+)([, ]*)",
                                lambda m: r"([-+]?\b\d+(?:\.\d+)?\b)"
                                + m.group(2), key_re)
                self.key_re_list.append(key_re)

            if not self.rules.get(key):
                self.rules[key] = [(value, key_re, p)]
            else:
                self.rules[key].append((value, key_re, p))

    def get_random_rule(self, rules):
        p = random.random()
        off = 0
        for v in rules:
            if p < (v[2]+off):
                return v
            off += v[2]

        return rules[0]

    def update_param_cmd(self, m):
        if not self.rules_key:
            return ""
        if len(self.rules_key) == 1:
            rule = self.rules_key[0]
        else:
            rule = self.get_random_rule(self.rules_key)

        if isinstance(rule[0], str):
            return rule[0].lower()
        else:
            args = list(map(float, m.groups()))
            return rule[0](*args).lower()

    def generate_path(self, n_iter):
        for n in range(n_iter):
            for key, rules in self.rules.items():
                self.rules_key = rules
                self.state = re.sub(rules[0][1], self.update_param_cmd,
                                    self.state)
                self.rules_key = None

            self.state = self.state.upper()

    def set_turtle(self, my_tuple):
        self.t.up()
        self.t.goto(my_tuple[0], my_tuple[1])
        self.t.seth(my_tuple[2])
        self.t.down()

    def add_rules_move(self, *moves):
        for key, func in moves:
            self.cmd_functions[key] = func

    def draw_turtle(self, start_pos, start_angle):
        self.t.up()
        self.t.setpos(start_pos)
        self.t.seth(start_angle)
        self.t.down()
        turtle_stack = []
        key_list_re = "|".join(self.key_re_list)
        for values in re.finditer(r"(" + key_list_re + r"|.)", self.state):
            cmd = values.group(0)
            args = [float(x) for x in values.groups()[1:] if x]

            if 'F' in cmd:
                if len(args) > 0 and self.cmd_functions.get('F'):
                    self.cmd_functions['F'](self.t, self.length, *args)
                else:
                    self.t.fd(self.length)
            elif 'S' in cmd:
                if len(args) > 0 and self.cmd_functions.get('S'):
                    self.cmd_functions['S'](self.t, self.length, *args)
                else:
                    self.t.up()
                    self.t.forward(self.length)
                    self.t.down()
            elif '+' in cmd:
                if len(args) > 0 and self.cmd_functions.get('+'):
                    self.cmd_functions['+'](self.t, self.angle, *args)
                else:
                    self.t.left(self.angle)
            elif '-' in cmd:
                if len(args) > 0 and self.cmd_functions.get('-'):
                    self.cmd_functions['-'](self.t, self.angle, *args)
                else:
                    self.t.right(self.angle)
            elif 'A' in cmd:
                if self.cmd_functions.get('A'):
                    self.cmd_functions['A'](self.t, self.length, *args)
            elif "[" in cmd:
                turtle_stack.append((self.t.xcor(), self.t.ycor(),
                                     self.t.heading(), self.t.pensize()))
            elif "]" in cmd:
                xcor, ycor, head, w = turtle_stack.pop()
                self.set_turtle((xcor, ycor, head))
                self.width = w
                self.t.pensize(self.width)


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
                                         width=self.width, height=self.height)
        self.config = ctk.CTkFrame(self, bg_color="#434343")
        self.move_pad = ctk.CTkFrame(self.config)
        self.move_left_button = ctk.CTkButton(self.move_pad,
                                              command=self.move_left, text="⬅",
                                              width=93,
                                              font=ctk.CTkFont(size=20))
        self.move_right_button = ctk.CTkButton(self.move_pad,
                                               command=self.move_right,
                                               text="➡",
                                               width=93,
                                               font=ctk.CTkFont(size=20))
        self.move_up_button = ctk.CTkButton(self.move_pad,
                                            command=self.move_up, text="⬆",
                                            width=93,
                                            font=ctk.CTkFont(size=20))
        self.move_down_button = ctk.CTkButton(self.move_pad,
                                              command=self.move_down, text="⬇",
                                              width=93,
                                              font=ctk.CTkFont(size=20))
        self.zoom_button = ctk.CTkButton(self.config,
                                         command=self.zoom_in,
                                         text="Приблизить",
                                         width=140,
                                         font=ctk.CTkFont(size=20))
        self.zoom_out_button = ctk.CTkButton(self.config,
                                             command=self.zoom_out,
                                             text="Отдалить",
                                             width=140,
                                             font=ctk.CTkFont(size=20))
        self.color_switch = Switch(self.config, 'Цвет')
        self.button = DrawButton(self.config, self.redraw)
        self.canvas_frame.pack(fill=ctk.BOTH, side=tk.LEFT)
        self.move_up_button.grid(row=0, column=1, sticky='nsew')
        self.move_left_button.grid(row=1, column=0, sticky='nsew')
        self.move_right_button.grid(row=1, column=2, sticky='nsew')
        self.move_down_button.grid(row=2, column=1, sticky='nsew')
        self.move_pad.pack(ipady=5, fill=ctk.BOTH, side=ctk.TOP)
        self.zoom_button.pack(pady=5)
        self.zoom_out_button.pack(pady=5)
        self.color_switch.pack(pady=5)

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
                            self.zoom / self.height, self.dx, self.dy, self.c,
                            color=self.color_switch.variable.get())
        img = Image.fromarray(image)
        imgtk = ctk.CTkImage(dark_image=img, size=(self.width, self.height))
        self.canvas_frame.configure(image=imgtk)

    @staticmethod
    @numba.njit(fastmath=True, parallel=True)
    def render(screen_array, width, height, zoom,
               dx, dy, C=None, max_iter=500, color=False):
        bias = 1.0 if C else 1.3
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
                if color:
                    if n_iter == max_iter-1:
                        r = g = b = 0
                    else:
                        r = (n_iter % 2) * 32 + 128
                        g = (n_iter % 4) * 64
                        b = (n_iter % 2) * 16 + 128
                else:
                    r = g = b = int(255 * n_iter / max_iter)
                screen_array[x, y] = (r, g, b)
        return screen_array.transpose((1, 0, 2))


class MandelbrotFractal(BSM2DMainClass):

    def __init__(self, master):
        super().__init__(master)
        self.button.pack(fill=ctk.BOTH, expand=True, pady=5)
        self.config.pack(fill=ctk.BOTH, side=tk.LEFT, expand=True)


class JuliaSlider(ctk.CTkFrame):

    def __init__(self, master, text, command, start=-2, end=2):
        super().__init__(master)
        self.columnconfigure(0, weight=4)
        self.columnconfigure(1, weight=1)
        self.variable = ctk.DoubleVar(self, 0)
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
            number_of_steps=400,
            command=command
        ).grid(column=0, row=1, pady=20, padx=20)
        self.label = ctk.CTkEntry(
            self,
            textvariable=self.variable,
            font=ctk.CTkFont(size=20),
            state=ctk.DISABLED,
            width=65
        ).grid(column=1, row=1)


class JuliaFractal(BSM2DMainClass):

    def __init__(self, master):
        super().__init__(master)
        self.real_c_slider = JuliaSlider(
            self.config, 'Реальная', self.slider_event)
        self.imag_c_slider = JuliaSlider(
            self.config, 'Мнимая', self.slider_event)
        self.real_c_slider.pack()
        self.imag_c_slider.pack()
        self.button.pack(fill=ctk.BOTH, expand=True, pady=5)
        self.config.pack(fill=ctk.BOTH, side=tk.LEFT, expand=True)

    def slider_event(self, event):
        self.draw()

    def draw(self):
        self.c = complex(
            self.real_c_slider.variable.get(),
            self.imag_c_slider.variable.get(),
        )
        self._draw_fractal()


if __name__ == "__main__":
    app = App()
    app.start()
