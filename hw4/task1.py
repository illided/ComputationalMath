import streamlit as st
from sympy import lambdify, parse_expr
import scipy.integrate as integrate
from quadro import *

st.header("Лабораторная работа #4.1")


def get_float(s):
    try:
        return float(s)
    except TypeError:
        st.error(f"Ожидалось число с плавающей запятой, но было получено {s}")


with st.form("Введите параметры задачи"):
    f_string = st.text_input("f - функция, для которой считается интеграл")
    col1, col2 = st.columns(2)
    a = col1.text_input("a - левая граница")
    b = col2.text_input("b - левая граница")
    if st.form_submit_button("Решить задачу"):
        a = get_float(a)
        b = get_float(b)
        if b < a:
            st.error("Левая граница должна быть меньше правой")
        f = lambdify("x", parse_expr(f_string))
    else:
        st.stop()

st.subheader("Реальное значение")

try:
    real_value = integrate.quad(f, a, b)[0]
except ZeroDivisionError:
    st.error("Функция не интегрируема на данном промежутке")
    st.stop()
st.latex(fr'\int_{{{a}}}^{{{b}}} {f_string} = {real_value}')


def print_error(real):
    err = abs(real_value - real)
    real_string = str(real)
    if real < 0:
        real_string = '(' + real_string + ')'
    st.latex(f"Error = |{real_value} - {real_string}| = {err}")
    st.latex(fr'PercentError = {round(abs(err / real_value), 4) * 100} \%')


st.subheader("КФ левого прямоугольника")
left_rect = left_rectangle(f, a, b)
st.latex(fr'(b - a) f(a) = {left_rect}')
print_error(left_rect)

st.subheader("КФ правого прямоугольника")
right_rect = right_rectangle(f, a, b)
st.latex(fr'(b - a) f(b) = {right_rect}')
print_error(right_rect)

st.subheader("КФ среднего прямоугольника")
middle_rec = middle_rectangle(f, a, b)
st.latex(fr'(b - a) f(\frac{{b - a}}{{2}}) = {middle_rec}')
print_error(middle_rec)

st.subheader("КФ трапеции")
trap = trapezoid(f, a, b)
st.latex(fr'\frac{{b - a}}{{2}} (f(b) - f(a)) = {trap}')
print_error(trap)

st.subheader("КФ Симпсона")
simp = simpson(f, a, b)
st.latex(fr'(\frac{{b - a}}{{6}}) * (f(a) + 4 * f(\frac{{a + b}}{{2}}) + f(b)) = {simp}')
print_error(simp)

st.subheader("КФ 3/8")
te = three_eight(f, a, b)
st.latex("h = (b - a) / 3")
st.latex(fr"(b - a) (\frac{1}{8} f(a) + \frac{3}{8} f(a + h) + \frac{3}{8} f(a + 2h) + \frac{1}{8} f(b)) = {te}")
print_error(te)