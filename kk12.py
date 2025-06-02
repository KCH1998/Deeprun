import streamlit as st
import numpy as np
from dezero import Variable
import graphviz
from io import BytesIO

def plot_dot_graph(output):
    dot = graphviz.Digraph(format='png')
    funcs = []
    seen_set = set()

    def add_func(f):
        if f not in seen_set:
            funcs.append(f)
            seen_set.add(f)

    def add_var(var):
        name = str(id(var))
        val = var.data if hasattr(var, 'data') else None
        if hasattr(var, 'name') and var.name:
            label = f'{var.name}={val}\nshape: {var.shape}'
        else:
            label = f'값: {val}\nshape: {var.shape}'
        dot.node(name, label=label, shape='ellipse')
        if var.creator is not None:
            add_func(var.creator)
            dot.edge(str(id(var.creator)), name)

    add_var(output)
    while funcs:
        func = funcs.pop()
        func_name = str(id(func))
        dot.node(func_name, label=func.__class__.__name__, shape='box')
        for x in func.inputs:
            add_var(x)
            dot.edge(str(id(x)), func_name)
        for y in func.outputs:
            dot.edge(func_name, str(id(y())))
    return dot

st.title("Graph-first Dezero: 실시간 연산 그래프 시각화")

x_val = st.number_input("x 값 입력", value=4.0)
operation = st.selectbox(
    "연산 선택",
    [
        "x ** 2 + x",
        "x ** 3 + 2 * x",
        "sin(x) + x",
        "cos(x) + x",
        "exp(x) - x",
        "log(x + 1)"
    ]
)

col1, col2 = st.columns([2, 3])

with col1:
    import math
    from dezero.functions import sin, cos, exp, log

    # Variable 및 중간 결과에 name 지정
    if operation == "x ** 2 + x":
        x = Variable(np.array(x_val), name='x')
        x2 = x ** 2
        x2.name = "x^2"
        y = x2 + x
        y.name = "x^2+x"
    elif operation == "x ** 3 + 2 * x":
        x = Variable(np.array(x_val), name='x')
        x3 = x ** 3
        x3.name = "x^3"
        x2x = 2 * x
        x2x.name = "2x"
        y = x3 + x2x
        y.name = "x^3+2x"
    elif operation == "sin(x) + x":
        x = Variable(np.array(x_val), name='x')
        sx = sin(x)
        sx.name = "sin(x)"
        y = sx + x
        y.name = "sin(x)+x"
    elif operation == "cos(x) + x":
        x = Variable(np.array(x_val), name='x')
        cx = cos(x)
        cx.name = "cos(x)"
        y = cx + x
        y.name = "cos(x)+x"
    elif operation == "exp(x) - x":
        x = Variable(np.array(x_val), name='x')
        ex = exp(x)
        ex.name = "exp(x)"
        y = ex - x
        y.name = "exp(x)-x"
    elif operation == "log(x + 1)":
        x = Variable(np.array(x_val), name='x')
        lx = log(x + 1)
        lx.name = "log(x+1)"
        y = lx
        y.name = "log(x+1)"
    else:
        x = Variable(np.array(x_val), name='x')
        y = x

    y.backward()
    dot = plot_dot_graph(y)
    img_bytes = dot.pipe(format='png')
    if img_bytes:
        st.image(BytesIO(img_bytes), caption="연산 그래프")
    else:
        st.error("그래프 생성 실패")

with col2:
    st.write("## 계산 과정 설명")
    st.markdown(f"- 입력 변수 x: {x_val}")

    if operation == "x ** 2 + x":
        st.markdown("- 계산식: \(x^2 + x\)")
        st.markdown(f"- 계산 과정: \n 1) \(x^2 = {x_val ** 2}\)\n 2) \(x^2 + x = {x_val ** 2 + x_val}\)")
    elif operation == "x ** 3 + 2 * x":
        st.markdown("- 계산식: \(x^3 + 2x\)")
        st.markdown(f"- 계산 과정: \n 1) \(x^3 = {x_val ** 3}\)\n 2) \(2x = {2 * x_val}\)\n 3) \(x^3 + 2x = {x_val ** 3 + 2 * x_val}\)")
    elif operation == "sin(x) + x":
        sin_val = math.sin(x_val)
        st.markdown("- 계산식: \(sin(x) + x\)")
        st.markdown(f"- 계산 과정: \n 1) \(sin(x) = {sin_val:.4f}\)\n 2) \(sin(x) + x = {sin_val + x_val:.4f}\)")
    elif operation == "cos(x) + x":
        cos_val = math.cos(x_val)
        st.markdown("- 계산식: \(cos(x) + x\)")
        st.markdown(f"- 계산 과정: \n 1) \(cos(x) = {cos_val:.4f}\)\n 2) \(cos(x) + x = {cos_val + x_val:.4f}\)")
    elif operation == "exp(x) - x":
        exp_val = math.exp(x_val)
        st.markdown("- 계산식: \(exp(x) - x\)")
        st.markdown(f"- 계산 과정: \n 1) \(exp(x) = {exp_val:.4f}\)\n 2) \(exp(x) - x = {exp_val - x_val:.4f}\)")
    elif operation == "log(x + 1)":
        if x_val + 1 > 0:
            log_val = math.log(x_val + 1)
            st.markdown("- 계산식: \(log(x + 1)\)")
            st.markdown(f"- 계산 과정: \n 1) \(x + 1 = {x_val + 1:.4f}\)\n 2) \(log(x + 1) = {log_val:.4f}\)")
        else:
            st.error("x + 1이 0보다 커야 log(x + 1)가 정의됩니다.")

    st.markdown(f"### 최종 결과값: {y.data}")