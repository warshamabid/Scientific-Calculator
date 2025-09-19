import pandas as pd
import sympy as sp
import streamlit as st
from sympy import symbols
from sympy import symbols, log

# ---------- Page / Theme ----------
st.set_page_config(page_title="SciCalc • Streamlit", page_icon="🧮", layout="centered")
@@ -68,6 +68,9 @@ def asind(z): return sp.asin(z)*180/sp.pi
def acosd(z): return sp.acos(z)*180/sp.pi
def atand(z): return sp.atan(z)*180/sp.pi

# Base-10 logarithm function
def log10(z): return log(z, 10)

def evaluate(expr: str) -> sp.Expr | str:
    """Safely evaluate with SymPy; returns sympy object or string error."""
    if not expr:
@@ -87,7 +90,7 @@ def evaluate(expr: str) -> sp.Expr | str:
        "abs": sp.Abs,
        "ln": sp.log,
        "log": sp.log,     # natural log by default; user can write log10
        "log10": sp.log10,
        "log10": log10,    # base-10 logarithm
        "exp": sp.exp,
        "floor": sp.floor,
        "ceil": sp.ceiling,
@@ -192,14 +195,20 @@ def plot_if_symbolic(sym_val):
        st.session_state.memory = 0.0
    elif button_action == "mem_plus":
        try:
            val = float(evaluate(st.session_state.display))
            st.session_state.memory += val
            expr = st.session_state.display.strip()
            res = evaluate(expr)
            if not isinstance(res, str):
                val = float(sp.N(res))
                st.session_state.memory += val
        except Exception:
            st.warning("Cannot M+ current expression.")
    elif button_action == "mem_minus":
        try:
            val = float(evaluate(st.session_state.display))
            st.session_state.memory -= val
            expr = st.session_state.display.strip()
            res = evaluate(expr)
            if not isinstance(res, str):
                val = float(sp.N(res))
                st.session_state.memory -= val
        except Exception:
            st.warning("Cannot M- current expression.")
    elif button_action == "equals":
@@ -209,6 +218,7 @@ def plot_if_symbolic(sym_val):
        if not isinstance(res, str):
            st.session_state.ans = out
            push_history(expr, out)
            plot_if_symbolic(res)
    elif button_action == "sign_change":
        if st.session_state.display.startswith("-"):
            st.session_state.display = st.session_state.display[1:]
