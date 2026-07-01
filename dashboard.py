import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Load Data
# -----------------------------
students = pd.read_csv("data/students.csv")
attendance = pd.read_csv("data/attendance.csv")
instructors = pd.read_csv("data/instructors.csv")
revenue = pd.read_csv("data/revenue.csv")

# -----------------------------
# Dashboard Title
# -----------------------------
st.set_page_config(page_title="Best Brains Operations Dashboard", layout="wide")

st.title("📊 Best Brains Operations Analytics Dashboard")
st.write("An operations dashboard for tracking student enrollment, attendance, instructor utilization, and revenue.")

# -----------------------------
# KPI Calculations
# -----------------------------
active_students = students[students["Active"] == "Yes"].shape[0]

attendance_rate = attendance["Present"].mean() * 100

total_revenue = revenue["Revenue"].sum()

average_hours = instructors["HoursWorked"].mean()

# -----------------------------
# KPI Cards
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Active Students", active_students)
col2.metric("Attendance Rate", f"{attendance_rate:.1f}%")
col3.metric("Total Revenue", f"${total_revenue:,.0f}")
col4.metric("Avg Instructor Hours", f"{average_hours:.1f}")

st.divider()

# -----------------------------
# Revenue Chart
# -----------------------------
st.subheader("Monthly Revenue")

fig1 = px.bar(
    revenue,
    x="Month",
    y="Revenue",
    text="Revenue",
    title="Revenue by Month"
)

st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# Subject Distribution
# -----------------------------
st.subheader("Enrollment by Subject")

subject_counts = students["Subject"].value_counts()

fig2 = px.pie(
    values=subject_counts.values,
    names=subject_counts.index,
    title="Student Distribution"
)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# Instructor Hours
# -----------------------------
st.subheader("Instructor Workload")

fig3 = px.bar(
    instructors,
    x="InstructorID",
    y="HoursWorked",
    title="Instructor Hours Worked"
)

st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# Raw Data
# -----------------------------
st.subheader("Student Data")

st.dataframe(students)

st.divider()

st.header("Add New Student")

with st.form("add_student"):

    student_id = st.number_input(
        "Student ID",
        min_value=1000,
        step=1
    )

    subject = st.selectbox(
        "Subject",
        ["Math", "English", "Coding", "Science"]
    )

    enrollment_date = st.date_input("Enrollment Date")

    active = st.selectbox(
        "Active",
        ["Yes", "No"]
    )

    submitted = st.form_submit_button("Add Student")

if submitted:

    new_student = pd.DataFrame({

        "StudentID": [student_id],

        "Subject": [subject],

        "EnrollmentDate": [enrollment_date],

        "Active": [active]

    })

    students = pd.concat([students, new_student], ignore_index=True)

    students.to_csv("data/students.csv", index=False)

    st.success("Student added successfully!")
st.subheader("Search Students")

search = st.text_input(
    "Search by Student ID or Subject"
)

if search:

    results = students[
        students["StudentID"].astype(str).str.contains(search, case=False)
        |
        students["Subject"].str.contains(search, case=False)
    ]

    st.dataframe(results)

st.divider()
st.header("Edit Student")

student_ids = students["StudentID"].tolist()

selected_student = st.selectbox(
    "Select Student",
    student_ids
)

student = students[
    students["StudentID"] == selected_student
].iloc[0]

new_subject = st.selectbox(
    "Subject",
    ["Math","English","Coding","Science"],
    index=["Math","English","Coding","Science"].index(student["Subject"])
)

new_active = st.selectbox(
    "Active",
    ["Yes","No"],
    index=["Yes","No"].index(student["Active"])
)

if st.button("Update Student"):

    students.loc[
        students["StudentID"] == selected_student,
        "Subject"
    ] = new_subject

    students.loc[
        students["StudentID"] == selected_student,
        "Active"
    ] = new_active

    students.to_csv(
        "data/students.csv",
        index=False
    )

    st.success("Student updated!")

st.divider()
st.header("Delete Student")

delete_student = st.selectbox(
    "Choose Student to Delete",
    students["StudentID"].tolist(),
    key="delete"
)

if st.button("Delete Student"):

    students = students[
        students["StudentID"] != delete_student
    ]

    students.to_csv(
        "data/students.csv",
        index=False
    )

    st.success("Student deleted!")
    