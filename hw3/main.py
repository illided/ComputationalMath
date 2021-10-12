import numpy as np
import pandas as pd
import streamlit as st
import sympy
import matplotlib.pyplot as plt
from hw2.layout import *
from task1 import SimpleReverseInterpolation, RootSearchReverseInterpolation
from hw2.launcher import create_table

def task_3_1():
    function = 'exp(x) + sin(x)'
    function_as_lambda = sympy.lambdify('x', sympy.parse_expr(function))

    a, b = get_region()
    t_s = get_table_size()
    y, n = get_interpolation_parameters(t_s, variable='y')

    X_t, Y_t = create_table(t_s, (a,b), function)
    st.write(pd.DataFrame([X_t, Y_t], index=['x', 'f(x)']))

    X = np.linspace(a, b)
    Y_target = np.full_like(X, y)
    Y_function = [function_as_lambda(x) for x in X]
    col1, col2 = st.columns(2)

    def plot_prediction(predictions: list, column):
        Y_p = [function_as_lambda(pr) for pr in predictions]
        fig, ax = plt.subplots()
        ax.plot(X, Y_target, "--")
        ax.plot(X, Y_function)
        ax.plot(predictions, Y_p, 'ro')
        column.pyplot(fig)

    col1.write('Отражение таблицы')
    col2.write('Интерполирование и поиск корней')

    sr = SimpleReverseInterpolation(X_t, Y_t)
    sr_pred = [sr.interpolate(y, n)(y)]

    plot_prediction(sr_pred, col1)
    col1.write(f'Ошибка: {abs(function_as_lambda(sr_pred[0]) - y)}')

    rs = RootSearchReverseInterpolation(X_t, Y_t)
    rs_pred = rs.interpolate(y, n)

    plot_prediction(rs_pred, col2)
    errors = [abs(function_as_lambda(pr) - y) for pr in rs_pred]
    col2.write(f'Ошибки: {errors}')
    col2.write(f'Средняя ошибка: {np.mean(np.array(errors))}')





def task3_2():
    ...


def main():
    st.header("Лабораторная работа №3")
    task = st.sidebar.selectbox("Выберите подзадачу",
                                ["1. Обратное интерполирование",
                                 "2. Нахождение производных по формулам численного дифференцирования"])
    if task == '1. Обратное интерполирование':
        task_3_1()
    elif task == '2. Нахождение производных по формулам численного дифференцирования':
        task3_2()


if __name__ == '__main__':
    main()
