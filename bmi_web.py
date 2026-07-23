import json

import streamlit as st


DATA_FILE = "bmi_records.json"


def save_records(records):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=4)


def load_records():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def calculate_bmi(height, weight):
    height_m = height / 100
    bmi = weight / (height_m * height_m)
    return bmi


def get_bmi_category(bmi):
    if bmi < 18.5:
        return "underweight"
    elif bmi < 24:
        return "normal weight"
    elif bmi < 28:
        return "overweight"
    else:
        return "obese"


def make_record(height, weight, bmi, result):
    person = {
        "height": height,
        "weight": weight,
        "bmi": bmi,
        "result": result
    }

    return person


def get_records_for_table(records):
    table_records = []

    for index, person in enumerate(records, start=1):
        table_records.append({
            "No.": index,
            "Height": person["height"],
            "Weight": person["weight"],
            "BMI": round(person["bmi"], 2),
            "Category": person["result"]
        })

    return table_records


def show_summary(records):
    if len(records) == 0:
        st.write("Average BMI: No records")
        st.write("Highest BMI record: No records")
        return

    average = sum(person["bmi"] for person in records) / len(records)

    bmi_values = []
    for person in records:
        bmi_values.append(person["bmi"])

    highest_bmi = max(bmi_values)

    highest_record_numbers = []
    for index, person in enumerate(records, start=1):
        if person["bmi"] == highest_bmi:
            highest_record_numbers.append(str(index))

    st.write(f"Average BMI: {round(average, 2)}")
    st.write(
        f"Highest BMI record: No. {', '.join(highest_record_numbers)} "
        f"(BMI: {round(highest_bmi, 2)})"
    )


def clear_inputs():
    # Streamlit 每次点击按钮都会重新运行脚本。
    # 这里通过 session_state 改回默认值，达到简单的清空/重置效果。
    st.session_state.height = 170.0
    st.session_state.weight = 60.0
    st.session_state.current_result = ""


st.set_page_config(page_title="BMI Calculator")
st.title("BMI Calculator")

if "height" not in st.session_state:
    st.session_state.height = 170.0

if "weight" not in st.session_state:
    st.session_state.weight = 60.0

if "current_result" not in st.session_state:
    st.session_state.current_result = ""

st.subheader("Input")

height = st.number_input(
    "Height (cm)",
    min_value=0.0,
    max_value=500.0,
    value=st.session_state.height,
    step=1.0,
    key="height"
)

weight = st.number_input(
    "Weight (kg)",
    min_value=0.0,
    max_value=500.0,
    value=st.session_state.weight,
    step=1.0,
    key="weight"
)

calculate_button = st.button("Calculate and Save")
clear_button = st.button("Clear / Reset", on_click=clear_inputs)

if calculate_button:
    if not 50 <= height <= 250:
        st.error("Please enter height between 50 and 250 cm.")
    elif not 10 <= weight <= 300:
        st.error("Please enter weight between 10 and 300 kg.")
    else:
        bmi = calculate_bmi(height, weight)
        result = get_bmi_category(bmi)

        records = load_records()
        records.append(make_record(height, weight, bmi, result))
        save_records(records)

        st.session_state.current_result = (
            f"Your BMI is {round(bmi, 2)}. "
            f"You are {result}."
        )
        st.success("Record saved successfully.")

st.subheader("Current Result")

if st.session_state.current_result:
    st.info(st.session_state.current_result)
else:
    st.write("Result will be shown here.")

records = load_records()

st.subheader("Summary")
show_summary(records)

st.subheader("History Records")

table_records = get_records_for_table(records)

if len(table_records) == 0:
    st.write("No records yet.")
else:
    # Streamlit 会把列表里的字典显示成网页表格。
    st.dataframe(table_records, use_container_width=True, hide_index=True)
