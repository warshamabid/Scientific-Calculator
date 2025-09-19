import pandas as pd
import sympy as sp
import streamlit as st
from sympy import symbols, log

# ---------- Page / Theme ----------
st.set_page_config(page_title="SciCalc • Streamlit", page_icon="🧮", layout="centered")

# ---------- Custom Functions ----------
def asind(z):
    return sp.asin(z) * 180 / sp.pi

def acosd(z):
    return sp.acos(z) * 180 / sp.pi

def atand(z):
    return sp.atan(z) * 180 / sp.pi

# Base-10 logarithm function
def log10(z):
    return log(z, 10)

# ---------- Expression Evaluator ----------
def evaluate(expr: str):
    """Safely evaluate with SymPy; returns sympy object or string error."""
    if not expr:
        return ""
    try:
        return sp.sympify(expr, locals={
            "sin": sp.sin,
            "cos": sp.cos,
            "tan": sp.tan,
            "asin": sp.asin,
            "acos": sp.acos,
            "atan": sp.atan,
            "asind": asind,
            "acosd": acosd,
            "atand": atand,
            "sqrt": sp.sqrt,
            "ln": sp.log,
            "log": sp.log,       # natural log by default
            "log10": log10,      # base-10 logarithm
            "exp": sp.exp,
            "abs": sp.Abs,
            "floor": sp.floor,
            "ceil": sp.ceiling,
            "pi": sp.pi,
            "e": sp.E,
        })
    except Exception as e:
        return f"Error: {e}"

# ---------- Streamlit Session ----------
if "display" not in st.session_state:
    st.session_state.display = ""
if "ans" not in st.session_state:
    st.session_state.ans = 0
if "memory" not in st.session_state:
    st.session_state.memory = 0.0
if "history" not in st.session_state:
    st.session_state.history = []

def push_history(expr, result):
    st.session_state.history.append(f"{expr} = {result}")
    if len(st.session_state.history) > 10:
        st.session_state.history.pop(0)

# ---------- UI ----------
st.title("🧮 Scientific Calculator")
st.caption("Streamlit • SymPy-powered • Plotting • History • Degree/Radian toggle")

angle_mode = st.radio("Angle", ["RAD", "DEG"], horizontal=True, index=1)

expr = st.text_input("Expression", st.session_state.display)

col1, col2 = st.columns([3, 1])
with col2:
    if st.button("C"):
        st.session_state.display = ""
    if st.button("Ans"):
        st.session_state.display += str(st.session_state.ans)

# Buttons Layout
buttons = [
    ["sin(", "cos(", "tan(", "asin(", "acos(", "atan("],
    ["log10(", "sqrt(", "(", ")", "^", "!"],
    ["7", "8", "9", "÷", "×", "π"],
    ["4", "5", "6", "-", "+", "e"],
    ["1", "2", "3", ",", "x", "^2"],
    ["0", ".", "%", "=", "Ans", "±"]
]

for row in buttons:
    cols = st.columns(len(row))
    for idx, token in enumerate(row):
        if cols[idx].button(token):
            if token == "=":
                expr = st.session_state.display.strip()
                res = evaluate(expr)
                if not isinstance(res, str):
                    out = sp.N(res) if angle_mode == "RAD" else sp.N(res * 180 / sp.pi)
                    st.session_state.ans = out
                    st.session_state.display = str(out)
                    push_history(expr, out)
                else:
                    st.session_state.display = res
            elif token == "C":
                st.session_state.display = ""
            elif token == "Ans":
                st.session_state.display += str(st.session_state.ans)
            elif token == "±":
                if st.session_state.display.startswith("-"):
                    st.session_state.display = st.session_state.display[1:]
                else:
                    st.session_state.display = "-" + st.session_state.display
            else:
                st.session_state.display += token

# Display
st.text_input("Current", st.session_state.display, key="display_box")

# History
st.subheader("History")
for h in reversed(st.session_state.history):
    st.write(h)
