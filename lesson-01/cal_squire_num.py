# -*- coding: UTF-8 -*-
"""
    梯度下降求解y=x**2的最小值
"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D

# 设置字符集，防止中文乱码
mpl.rcParams['font.sans-serif'] = [u'simHei']
mpl.rcParams['axes.unicode_minus'] = False

# 原函数
def f(x, y):
    return x**2 + y**2

# 偏导
def h(t):
    return 2 * t

# 画图
def draw(X, Y, Z, x, y, f_current):
    figure = plt.figure()
    axes = Axes3D(figure)
    X2 = np.arange(-2, 2, 0.2)
    Y2 = np.arange(-2, 2, 0.2)
    X2, Y2 = np.meshgrid(X2, Y2)
    Z2 = f(X2, Y2)

    axes.plot_surface(X2, Y2, Z2, rstride=1, cstride=1, cmap='rainbow')
    axes.plot(X, Y, Z, 'ro--')
    axes.set_title(u'z=x^2+y^2函数求解最小值，最终解为：x=%.2f,y=%.2f,z=%.2f'
        % (x, y, f_current))
    plt.show()

# 梯度下降求解z=x**2+y**2的最小值
def gd():
    X = []
    Y = []
    Z = []

    x = 2
    y = 2
    step = 0.1
    f_change = f(x, y)
    f_current = f(x, y)
    X.append(x)
    Y.append(y)
    Z.append(f_current)
    while f_change > 1e-10:
        x = x - step * h(x)
        y = y - step * h(y)
        f_change = np.abs(f_current - f(x, y))
        f_current = f(x, y)

        X.append(x)
        Y.append(y)
        Z.append(f_current)
    print("result: ", (x, y, f_current))
    draw(X, Y, Z, x, y, f_current)

if __name__ == '__main__':
    gd()