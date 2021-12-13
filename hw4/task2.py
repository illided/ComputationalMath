import scipy.integrate as integrate
import streamlit as st
from sympy import diff
from sympy import lambdify, parse_expr
import numpy as np

from quadro_complex import *

st.header("Лабораторная работа #4.2")


def get_float(s):
    try:
        return float(s)
    except TypeError:
        st.error(f"Ожидалось число с плавающей запятой, но было получено {s}")


def get_int(s):
    try:
        return int(s)
    except TypeError:
        st.error(f'Ожидалось целое число но было получено: {s}')


with st.form("Введите параметры задачи"):
    f_string = st.text_input("f - функция, для которой считается интеграл")
    col1, col2 = st.columns(2)
    a = col1.text_input("a - левая граница")
    b = col2.text_input("b - правая граница")
    m = st.text_input('m - количество разбиений')
    if st.form_submit_button("Решить задачу"):
        a = get_float(a)
        b = get_float(b)
        if b < a:
            st.error("Левая граница должна быть меньше правой")
        m = get_int(m)
        if m < 1:
            st.error("Количество разбиений должно быть больше одного")
        f = lambdify("x", parse_expr(f_string))
    else:
        st.stop()

st.subheader("Реальное значение")

try:
    real_value = integrate.quad(f, a, b)[0]
except ZeroDivisionError:
    st.error("Функция не интегрируема на данном промежутке")
    st.stop()
st.latex(fr'\int_{{{a}}}^{{{b}}} {f_string} = J = {real_value}')


def print_abs_fact_error(real):
    err = abs(real_value - real)
    st.latex(f"ActualAbsoluteError = {err}")


def print_relative_abs_error(real):
    err = abs(real_value - real)
    st.latex(fr'PercentError = {round(abs(err / real_value) * 100, 4)} \%')


def theoretical_error(AST, Const):
    f_expr = parse_expr(f_string)
    f_der = lambdify('x', diff(f_expr, 'x', AST + 1))
    X = np.linspace(a, b, 100_000)
    Y = abs(f_der(X))
    M = np.amax(Y)
    h = (b - a) / m
    error = Const * M * (b - a) * h ** (AST + 1)
    st.latex(fr'TheoreticalAbsoluteError = {error}')


st.subheader("CКФ левых прямоугольников")
left_rect = QuadroFormulas(f, 'left_rect').compute(m, a, b)
st.latex(fr'J_{{leftRect}}(h) = {left_rect}')
theoretical_error(0, 1 / 2)
print_abs_fact_error(left_rect)
print_relative_abs_error(left_rect)

st.subheader("СКФ правых прямоугольников")
right_rect = QuadroFormulas(f, 'right_rect').compute(m, a, b)
st.latex(fr'J_{{rightRect}}(h) = {right_rect}')
theoretical_error(0, 1 / 2)
print_abs_fact_error(right_rect)
print_relative_abs_error(right_rect)

st.subheader("СКФ средних прямоугольников")
middle_rect = QuadroFormulas(f, 'middle_rect').compute(m, a, b)
st.latex(fr'J_{{middleRect}}(h) = {middle_rect}')
theoretical_error(1, 1 / 24)
print_abs_fact_error(middle_rect)
print_relative_abs_error(middle_rect)

st.subheader('СКФ трапеций')
trap = QuadroFormulas(f, 'trapezoid').compute(m, a, b)
st.latex(fr'J_{{trap}}(h) = {trap}')
theoretical_error(1, 1 / 12)
print_abs_fact_error(trap)
print_relative_abs_error(trap)

st.subheader('СКФ Симпсона')
simp = QuadroFormulas(f, 'simpson').compute(m, a, b)
st.latex(fr'J_{{Simpson}}(h) = {simp}')
theoretical_error(3, 1 / 2880)
print_abs_fact_error(simp)
print_relative_abs_error(simp)
