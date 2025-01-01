import random
from math import sin, cos, pi, log
from tkinter import *

CANVAS_WIDTH = 640  # 画布的宽
CANVAS_HEIGHT = 480  # 画布的高
CANVAS_CENTER_X = CANVAS_WIDTH / 2  # 画布中心的X轴坐标
CANVAS_CENTER_Y = CANVAS_HEIGHT / 2  # 画布中心的Y轴坐标
IMAGE_ENLARGE = 11  # 放大比例
HEART_COLOR = "#ff2121"  # 心的颜色


def heart_function(t, shrink_ratio: float = IMAGE_ENLARGE):
    """
    爱心函数生成器
    :param t: 参数
    :param shrink_ratio: 放大比例
    :return: 坐标
    """
    x = 16 * (sin(t) ** 3)
    y = -(13 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(4 * t))

    # 放大
    x *= shrink_ratio
    y *= shrink_ratio

    # 移到画布中央
    x += CANVAS_CENTER_X
    y += CANVAS_CENTER_Y

    return int(x), int(y)


def scatter_inside(x, y, beta=0.15):
    """
    随机扩散
    :param x: 原x
    :param y: 原y
    :param beta: 扩散强度
    :return: 新坐标
    """
    ratio_x = -beta * log(random.random())
    ratio_y = -beta * log(random.random())

    dx = ratio_x * (x - CANVAS_CENTER_X)
    dy = ratio_y * (y - CANVAS_CENTER_Y)

    return x - dx, y - dy


def shrink(x, y, ratio):
    """
    粒子抖动效果
    :param x: 原x
    :param y: 原y
    :param ratio: 缩放比例
    :return: 新坐标
    """
    force = -1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.6)
    dx = ratio * force * (x - CANVAS_CENTER_X)
    dy = ratio * force * (y - CANVAS_CENTER_Y)
    return x - dx, y - dy


def curve(p):
    """
    自定义曲线函数
    :param p: 参数
    :return: 正弦值
    """
    return 2 * (2 * sin(4 * p)) / (2 * pi)


class Heart:
    """
    爱心类，用于生成爱心及其动画效果
    """

    def __init__(self, generate_frame=20):
        self._points = set()  # 原始爱心坐标集合
        self._edge_diffusion_points = set()  # 边缘扩散效果点坐标集合
        self._center_diffusion_points = set()  # 中心扩散效果点坐标集合
        self.all_points = {}  # 每帧动态点坐标
        self.build(1000)  # 生成较少的点

        self.generate_frame = generate_frame

        # 预先计算每一帧的动态效果
        for frame in range(generate_frame):
            self.calc(frame)

    def build(self, number):
        """生成爱心的基础点和扩散效果"""
        for _ in range(number):
            t = random.uniform(0, 2 * pi)  # 随机生成
            x, y = heart_function(t)
            self._points.add((x, y))

        self._generate_diffusion(self._points, 3, self._edge_diffusion_points, 0.05)
        self._generate_diffusion(self._edge_diffusion_points, 3, self._center_diffusion_points, 0.17)

    def _generate_diffusion(self, points, num_iterations, diffusion_set, beta):
        """生成扩散效果"""
        for _x, _y in list(points):
            for _ in range(num_iterations):
                x, y = scatter_inside(_x, _y, beta)
                diffusion_set.add((x, y))

    def calc_position(self, x, y, ratio):
        """调整缩放比例，产生效果"""
        force = 1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.520)
        dx = ratio * force * (x - CANVAS_CENTER_X) + random.randint(-1, 1)
        dy = ratio * force * (y - CANVAS_CENTER_Y) + random.randint(-1, 1)
        return x - dx, y - dy

    def calc(self, generate_frame):
        """计算每一帧的动态效果"""
        ratio = 10 * curve(generate_frame / 10 * pi)  # 圆滑的周期的缩放比例
        halo_radius = int(4 + 6 * (1 + curve(generate_frame / 10 * pi)))
        halo_number = int(1000 + 2000 * abs(curve(generate_frame / 10 * pi) ** 2))

        all_points = []

        # 生成光环效果
        self._generate_halo(halo_number, halo_radius, all_points)

        # 生成爱心轮廓、边缘和中心扩散效果
        self._generate_heart_points(ratio, all_points)

        self.all_points[generate_frame] = all_points

    def _generate_halo(self, halo_number, halo_radius, all_points):
        """生成光环效果"""
        heart_halo_point = set()
        for _ in range(halo_number):
            t = random.uniform(0, 2 * pi)
            x, y = heart_function(t, shrink_ratio=11.6)
            x, y = shrink(x, y, halo_radius)
            if (x, y) not in heart_halo_point:
                heart_halo_point.add((x, y))
                x += random.randint(-14, 14)
                y += random.randint(-14, 14)
                size = random.choice((1, 2, 2))
                all_points.append((x, y, size))

    def _generate_heart_points(self, ratio, all_points):
        """生成爱心轮廓、边缘和中心扩散效果的点"""
        for x, y in self._points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 3)
            all_points.append((x, y, size))

        for x, y in self._edge_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))

        for x, y in self._center_diffusion_points:
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))

    def render(self, render_canvas, render_frame):
        """渲染指定帧的爱心图案"""
        for x, y, size in self.all_points[render_frame % self.generate_frame]:
            render_canvas.create_oval(x, y, x + size, y + size, width=0, fill=HEART_COLOR)


def draw(main: Tk, render_canvas: Canvas, render_heart: Heart, render_frame=0):
    """更新并渲染每一帧的爱心效果"""
    render_canvas.delete('all')
    render_heart.render(render_canvas, render_frame)
    main.after(20, draw, main, render_canvas, render_heart, render_frame + 1)  # 提高帧速率


if __name__ == '__main__':
    root = Tk()
    canvas = Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white")
    canvas.pack()

    heart_effect = Heart(generate_frame=20)  # 减少生成帧数
    draw(root, canvas, heart_effect)

    root.mainloop()
