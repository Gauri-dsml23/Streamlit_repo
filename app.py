import streamlit as st


st.set_page_config(page_title="Basic Calculator", page_icon="🧮", layout="centered")

st.title("Basic Calculator")
st.write("Calculate with addition, subtraction, multiplication, or division.")

with st.form("calculator"):
	first_number = st.number_input("First number", value=0.0)
	operation = st.selectbox(
		"Operation",
		["Addition (+)", "Subtraction (-)", "Multiplication (*)", "Division (/)"]
	)
	second_number = st.number_input("Second number", value=0.0)
	calculate = st.form_submit_button("Calculate")

if calculate:
	if operation == "Addition (+)":
		result = first_number + second_number
		symbol = "+"
	elif operation == "Subtraction (-)":
		result = first_number - second_number
		symbol = "-"
	elif operation == "Multiplication (*)":
		result = first_number * second_number
		symbol = "*"
	elif second_number == 0:
		st.error("Cannot divide by zero. Enter a non-zero second number.")
		st.stop()
	else:
		result = first_number / second_number
		symbol = "/"

	output = f"{first_number:g} {symbol} {second_number:g} = {result:g}"
	st.session_state["calculation_output"] = output

if "calculation_output" in st.session_state:
	st.success(st.session_state["calculation_output"])
	st.download_button(
		"Download result",
		data=st.session_state["calculation_output"],
		file_name="calculation_result.txt",
		mime="text/plain",
	)