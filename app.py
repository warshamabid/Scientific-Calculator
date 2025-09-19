import pandas as pd
import sympy as sp
import streamlit as st
from sympy import symbols, log

# ---------- Page / Theme ----------
st.set_page_config(page_title="SciCalc • Streamlit", page_icon="🧮", layout="centered")

# Degree-based trig inverse
def asind(z): 
    return sp.asin(z) * 180 / sp.pi

def acosd(z): 
    return sp.acos(z) * 180 / sp.pi

def atand(z): 
    return sp.atan(z) * 180 / sp.pi

# Base-10 logarithm function
def log10(z): 
    return log(z, 10)

# Expression evaluator
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
            "log": sp.log,
            "log10": log10,
            "exp": sp.exp,
            "abs": sp.Abs,
            "floor": sp.floor,
            "ceil": sp.ceiling,
            "pi": sp.pi,
            "e": sp.E,
        })
    except Exception as e:
        return f"Error: {e}"
