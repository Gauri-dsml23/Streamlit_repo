import csv
from datetime import datetime
from pathlib import Path

import streamlit as st


HISTORY_FILE = Path(__file__).with_name("calculation_history.csv")
OPERATIONS = {
    "Add": ("+", lambda left, right: left + right),
    "Subtract": ("-", lambda left, right: left - right),
    "Multiply": ("*", lambda left, right: left * right),
    "Divide": ("/", lambda left, right: left / right),
}
HISTORY_FIELDS = ["saved_at", "expression", "result"]


def save_calculation(calculation):
    file_exists = HISTORY_FILE.exists() and HISTORY_FILE.stat().st_size > 0
    with HISTORY_FILE.open("a", newline="", encoding="utf-8") as history_file:
        writer = csv.DictWriter(history_file, fieldnames=HISTORY_FIELDS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(calculation)


def read_history():
    if not HISTORY_FILE.exists():
        return []
    with HISTORY_FILE.open("r", newline="", encoding="utf-8") as history_file:
        return list(csv.DictReader(history_file))


st.set_page_config(
    page_title="Quick Math Calculator",
    page_icon="🧮",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap');
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(145deg, #f1f8f6 0%, #f8fafb 58%, #fff4ef 100%);
    }
    .block-container {
        max-width: 760px;
        padding-top: 3rem;
        padding-bottom: 3rem;
    }
    h1, h2, h3, p, label, button, input {
        font-family: "DM Sans", "Avenir Next", sans-serif;
    }
    h1 {
        color: #173d37;
        font-family: "Manrope", "Avenir Next", sans-serif;
        font-size: 2.5rem;
        line-height: 1.15;
        margin-bottom: 0.45rem;
    }
    [data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.88);
        border: 1px solid #dce9e5;
        border-radius: 8px;
        padding: 1.25rem 1.4rem;
    }
    .stButton > button[kind="primary"] {
        background: #df684f;
        border: 1px solid #df684f;
        border-radius: 6px;
        color: white;
        font-weight: 700;
    }
    .stButton > button[kind="primary"]:hover {
        background: #c9543d;
        border-color: #c9543d;
        color: white;
    }
    [data-testid="stMetricValue"] {
        color: #173d37;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<p style="color:#df684f;font-size:0.78rem;font-weight:700;letter-spacing:0.08em;'
    'margin-bottom:0.4rem">QUICK TOOL / 01</p>',
    unsafe_allow_html=True,
)
st.title("Quick Math")
st.caption("A clear answer for the numbers in front of you.")

with st.form("calculator_form"):
    left_column, right_column = st.columns(2)
    with left_column:
        left_value = st.number_input("First number", value=0.0, step=1.0)
    with right_column:
        right_value = st.number_input("Second number", value=0.0, step=1.0)

    operation = st.radio(
        "Choose an operation",
        list(OPERATIONS),
        format_func=lambda name: f"{name}  {OPERATIONS[name][0]}",
        horizontal=True,
    )
    calculate = st.form_submit_button("Calculate", type="primary", width="stretch")

if calculate:
    st.session_state.pop("last_calculation", None)
    symbol, calculate_result = OPERATIONS[operation]
    if operation == "Divide" and right_value == 0:
        st.error("Division by zero is undefined. Enter a non-zero second number.")
    else:
        result = calculate_result(left_value, right_value)
        expression = f"{left_value:g} {symbol} {right_value:g} = {result:g}"
        st.session_state["last_calculation"] = {
            "saved_at": datetime.now().astimezone().isoformat(timespec="seconds"),
            "expression": expression,
            "result": f"{result:g}",
        }

calculation = st.session_state.get("last_calculation")
if calculation:
    st.markdown("### Result")
    st.metric("Answer", calculation["result"])
    st.code(calculation["expression"], language=None)

    download_column, save_column = st.columns(2)
    with download_column:
        st.download_button(
            "Download result",
            data=calculation["expression"] + "\n",
            file_name="calculation_result.txt",
            mime="text/plain",
            width="stretch",
        )
    with save_column:
        if st.button("Save to history", width="stretch"):
            save_calculation(calculation)
            st.session_state["history_saved"] = calculation["expression"]

    if st.session_state.get("history_saved") == calculation["expression"]:
        st.success("Saved to calculation_history.csv")

history = read_history()
if history:
    st.divider()
    st.markdown("### Recent calculations")
    st.dataframe(
        [{"Calculation": row["expression"], "Saved": row["saved_at"]} for row in reversed(history[-8:])],
        hide_index=True,
        width="stretch",
    )