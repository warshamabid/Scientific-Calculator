import streamlit as st
import sympy as sp

st.set_page_config(page_title="Scientific Calculator", page_icon="🧮", layout="centered")

st.title("🧮 Scientific Calculator")

# Initialize session state
if "display" not in st.session_state:
    st.session_state.display = ""

# Function to safely evaluate mathematical expressions
def evaluate(expression):
    try:
        return sp.sympify(expression).evalf()
    except Exception:
        return "Error"

# Display screen
st.text_input("Display", st.session_state.display, key="display_box", disabled=True)

# Define calculator buttons
buttons = [
    ["7", "8", "9", "/", "sqrt"],
    ["4", "5", "6", "*", "exp"],
    ["1", "2", "3", "-", "^"],
    ["0", ".", "(", ")", "+"],
    ["sin", "cos", "tan", "log", "C"],
    ["=",]
]

# Layout buttons in rows
for row_idx, row in enumerate(buttons):
    cols = st.columns(len(row))
    for col_idx, token in enumerate(row):
        if cols[col_idx].button(token, key=f"{row_idx}-{col_idx}-{token}"):  # ✅ unique key added
            if token == "=":
                expr = st.session_state.display.strip()
                res = evaluate(expr)
                st.session_state.display = str(res)
            elif token == "C":
                st.session_state.display = ""
            elif token in ["sin", "cos", "tan", "log", "sqrt", "exp"]:
                st.session_state.display += f"{token}("
            elif token == "^":
                st.session_state.display += "**"
            else:
                st.session_state.display += token
