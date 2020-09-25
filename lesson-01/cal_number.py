# -*- coding: UTF-8 -*-
"""
    梯度下降求解y=x**2的最小值
"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# 设置字符集，防止中文乱码
mpl.rcParams['font.sans-serif'] = [u'simHei']
mpl.rcParams['axes.unicode_minus'] = False

# 原函数
def f(x):
    return x ** 2

# 导数
def h(x):
    return 2 * x

# 画图
def draw_gd(X, Y, x, f_current):
    figure = plt.figure()
    X2 = np.arange(-2.1, 2.15, 0.05)
    Y2 = X2 ** 2

    plt.plot(X2, Y2, '-', color='#666666', linewidth=2)
    plt.plot(X, Y, 'ro--')
    plt.title(u'y=x^2函数求解最小值，最终解为：x=%.2f,y=%.2f' % (x, f_current))
    plt.show()

# 梯度下降求解y=x**2的最小值
def gd():
    X = []
    Y = []

    x = 2
    step = 0.8
    f_change = f(x)
    f_current = f(x)
    X.append(x)
    Y.append(f_current)

    while f_change > 1e-10:
        x = x - step * h(x)
        f_change = np.abs(f_current - f(x))
        f_current = f(x)

        X.append(x)
        Y.append(f_current)
    print("result: ", (x, f_current))
    draw_gd(X, Y, x, f_current)

if __name__ == '__main__':
    gd()