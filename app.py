import re
import math
import numpy as np
import pandas as pd
import sympy as sp
import streamlit as st
from sympy import symbols

# ---------- Page / Theme ----------
st.set_page_config(page_title="SciCalc • Streamlit", page_icon="🧮", layout="centered")
st.title("🧮 Scientific Calculator")
st.caption("Streamlit • SymPy-powered • Plotting • History • Degree/Radian toggle")

# ---------- Session State Defaults ----------
if "display" not in st.session_state:
    st.session_state.display = ""
if "ans" not in st.session_state:
    st.session_state.ans = "0"
if "memory" not in st.session_state:
    st.session_state.memory = 0.0
if "history" not in st.session_state:
    st.session_state.history = []
if "angle_mode" not in st.session_state:
    st.session_state.angle_mode = "RAD"

# ---------- Angle Mode ----------
col_mode1, col_mode2 = st.columns([1, 3])
with col_mode1:
    st.session_state.angle_mode = st.radio(
        "Angle", ["RAD", "DEG"], index=0, horizontal=True
    )
with col_mode2:
    st.write("")

# ---------- Helpers ----------
x = symbols("x")

def _preprocess(expr: str) -> str:
    if not expr:
        return expr
    expr = expr.replace("^", "**")
    expr = re.sub(r"(\))\s*%", r"\1/100", expr)
    expr = re.sub(r"(\d+(\.\d+)?)\s*%", r"(\1)/100", expr)
    expr = re.sub(r"(\d+|\([^\(\)]*\))\s*!",
                  lambda m: f"factorial({m.group(1)})", expr)
    expr = expr.replace("×", "*").replace("÷", "/")
    return expr

# Degree wrappers
def sind(z): return sp.sin(sp.pi*z/180)
def cosd(z): return sp.cos(sp.pi*z/180)
def tand(z): return sp.tan(sp.pi*z/180)
def asind(z): return sp.asin(z)*180/sp.pi
def acosd(z): return sp.acos(z)*180/sp.pi
def atand(z): return sp.atan(z)*180/sp.pi

def evaluate(expr: str) -> sp.Expr | str:
    if not expr:
        return ""
    expr = _preprocess(expr)
    expr = expr.replace("Ans", f"({st.session_state.ans})")
    common_locals = {
        "x": x, "pi": sp.pi, "e": sp.E,
        "sqrt": sp.sqrt, "abs": sp.Abs, "ln": sp.log,
        "log": sp.log, "log10": sp.log10, "exp": sp.exp,
        "floor": sp.floor, "ceil": sp.ceiling,
        "gamma": sp.gamma, "factorial": sp.factorial,
        "sinh": sp.sinh, "cosh": sp.cosh, "tanh": sp.tanh,
        "asinh": sp.asinh, "acosh": sp.acosh, "atanh": sp.atanh,
    }
    if st.session_state.angle_mode == "DEG":
        trig_locals = {
            "sin": sind, "cos": cosd, "tan": tand,
            "asin": asind, "acos": acosd, "atan": atand,
        }
    else:
        trig_locals = {
            "sin": sp.sin, "cos": sp.cos, "tan": sp.tan,
            "asin": sp.asin, "acos": sp.acos, "atan": sp.atan,
        }
    locals_dict = {**common_locals, **trig_locals}
    try:
        sym = sp.sympify(expr, locals=locals_dict, convert_xor=True)
        return sp.simplify(sym)
    except Exception as e:
        return f"Error: {str(e)}"

def push_history(expr: str, result_str: str):
    st.session_state.history.insert(0, {"expr": expr, "result": result_str})
    st.session_state.history = st.session_state.history[:50]

def show_result(sym_val) -> str:
    if isinstance(sym_val, str):
        st.error(sym_val)
        return sym_val
    try:
        num = sp.N(sym_val, 16)
    except Exception:
        num = sym_val
    st.latex(sp.latex(sp.simplify(sym_val)))
    return str(num)

def plot_if_symbolic(sym_val):
    if isinstance(sym_val, str):
        return
    if x in getattr(sym_val, "free_symbols", set()):
        st.subheader("Plot")
        colA, colB = st.columns(2)
        xmin = colA.number_input("x min", value=-10.0)
        xmax = colB.number_input("x max", value=10.0)
        if xmax <= xmin:
            st.info("Set xmax > xmin to plot.")
            return
        try:
            f = sp.lambdify(x, sym_val, "numpy")
            xs = np.linspace(xmin, xmax, 600)
            ys = f(xs)
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots()
            ax.plot(xs, ys)
            ax.set_xlabel("x")
            ax.set_ylabel("f(x)")
            ax.grid(True, which="both", alpha=0.3)
            st.pyplot(fig, clear_figure=True)
        except Exception as e:
            st.warning(f"Could not plot: {e}")

# ---------- Input box ----------
st.session_state.display = st.text_input(
    "Expression",
    value=st.session_state.display,
    key="input_box",
    placeholder="Type or use the buttons… e.g., sin(30)+sqrt(2)^2, 5!, log10(100), x^2+2*x+1"
)

# ---------- Button helpers ----------
def sync_display(new_val):
    st.session_state.display = new_val
    st.session_state.input_box = new_val  # keep input box synced

def add(txt): sync_display(st.session_state.display + txt)
def backspace(): sync_display(st.session_state.display[:-1])
def clear_all(): sync_display("")
def set_ans(): add("Ans")

def equals():
    expr = st.session_state.display.strip()
    res = evaluate(expr)
    out = show_result(res)
    if not isinstance(res, str):
        st.session_state.ans = out
        push_history(expr, out)
        plot_if_symbolic(res)

def mem_clear(): st.session_state.memory = 0.0
def mem_recall(): add(str(st.session_state.memory))
def mem_plus():
    try:
        val = float(evaluate(st.session_state.display))
        st.session_state.memory += val
    except Exception:
        st.warning("Cannot M+ current expression.")
def mem_minus():
    try:
        val = float(evaluate(st.session_state.display))
        st.session_state.memory -= val
    except Exception:
        st.warning("Cannot M- current expression.")

# ---------- Buttons ----------
# Row 1
r1 = st.columns(6)
for idx, (label, fn) in enumerate([
    ("MC", mem_clear), ("MR", mem_recall), ("M+", mem_plus),
    ("M-", mem_minus), ("Ans", set_ans), ("C", clear_all)
]):
    if r1[idx].button(label): fn()

# Row 2
r2 = st.columns(7)
for idx, token in enumerate(["sin(", "cos(", "tan(", "asin(", "acos(", "atan(", "ln("]):
    if r2[idx].button(token): add(token)

# Row 3
r3 = st.columns(7)
for idx, token in enumerate(["log10(", "sqrt(", "(", ")", "^", "!", "%"]):
    if r3[idx].button(token): add(token)

# Row 4-6
rows = [
    ["7", "8", "9", "÷", "×", "π", "e"],
    ["4", "5", "6", "-", ",", "x", "^2"],
    ["1", "2", "3", "+", ".", "±", "⌫"],
]
for row in rows:
    cols = st.columns(7)
    for i, key in enumerate(row):
        if cols[i].button(key):
            if key == "÷": add("/")
            elif key == "×": add("*")
            elif key == "π": add("pi")
            elif key == "^2": add("^2")
            elif key == "±":
                if st.session_state.display.startswith("-"):
                    sync_display(st.session_state.display[1:])
                else:
                    sync_display("-" + st.session_state.display)
            elif key == "⌫": backspace()
            else: add(key)

# Equals
eq_col1, eq_col2 = st.columns([3, 1])
if eq_col2.button("="): equals()
eq_col1.info("Tips: ^ is power, ! is factorial, % is percent, Ans is last result, use x to enable plotting.")

# ---------- History ----------
st.subheader("History")
if st.session_state.history:
    df_hist = pd.DataFrame(st.session_state.history)
    st.dataframe(df_hist, use_container_width=True, hide_index=True)
    csv = df_hist.to_csv(index=False).encode("utf-8")
    st.download_button("Download history (CSV)", csv, "calc_history.csv", "text/csv")
else:
    st.caption("No history yet. Calculate something!")

# ---------- Footer ----------
st.divider()
st.caption("Made with ❤️ using Streamlit + SymPy. Degree mode maps trig functions to degrees.")
