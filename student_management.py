import streamlit as st
import json
import os

# File path for storing student data
data_file = "students.json"

# Load student data from the file
def load_students():
    if os.path.exists(data_file):
        with open(data_file, "r") as file:
            return [Student.from_dict(data) for data in json.load(file)]
    return []

# Save student data to the file
def save_students(students):
    with open(data_file, "w") as file:
        json.dump([student.to_dict() for student in students], file, indent=4)

class Student:
    counter = 1000

    def __init__(self, name, courses=None, balance=100):
        self.id = Student.counter
        Student.counter += 1
        self.name = name
        self.courses = courses if courses else []
        self.balance = balance

    def enroll_course(self, course):
        self.courses.append(course)

    def view_balance(self):
        return self.balance

    def pay_fee(self, amount):
        self.balance -= amount

    def show_status(self):
        return {
            "ID": self.id,
            "Name": self.name,
            "Courses": self.courses,
            "Balance": self.balance
        }

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "courses": self.courses,
            "balance": self.balance
        }

    @staticmethod
    def from_dict(data):
        student = Student(data["name"], data["courses"], data["balance"])
        student.id = data["id"]
        return student

class StudentManager:
    def __init__(self):
        self.students = load_students()

    def add_student(self, name):
        student = Student(name)
        self.students.append(student)
        save_students(self.students)
        return student.id

    def enroll_student(self, student_id, course):
        student = self.find_student(student_id)
        if student:
            student.enroll_course(course)
            save_students(self.students)

    def view_student_balance(self, student_id):
        student = self.find_student(student_id)
        return student.view_balance() if student else None

    def pay_student_fee(self, student_id, amount):
        student = self.find_student(student_id)
        if student:
            student.pay_fee(amount)
            save_students(self.students)

    def show_student_status(self, student_id):
        student = self.find_student(student_id)
        return student.show_status() if student else None

    def find_student(self, student_id):
        return next((std for std in self.students if std.id == student_id), None)

    def remove_student(self, student_id):
        self.students = [student for student in self.students if student.id != student_id]
        save_students(self.students)

# Streamlit app
st.markdown("""
    <style>
    .title {
        background-color: pink;
        padding: 10px;
        color: black;
        font-size: 24px;
        text-align: center;
        font-weight: bold;
        text-transform: uppercase;
    }
    .subheader {
        background-color: blue;
        padding: 10px;
        color: white;
        font-size: 18px;
        font-weight: bold;
    }
    .exit-message {
        background-color: green;
        color: white;
        font-size: 24px;
        text-align: center;
        font-weight: bold;
        padding: 20px;
        border-radius: 10px;
        text-transform: uppercase;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="title">Student Management System</div>', unsafe_allow_html=True)

manager = StudentManager()

# Add Student
st.markdown('<div class="subheader">Add Student</div>', unsafe_allow_html=True)
name = st.text_input("Enter Student Name:")
if st.button("Add Student"):
    if name:
        student_id = manager.add_student(name)
        st.success(f"Student '{name}' added successfully with ID {student_id}.")
    else:
        st.error("Please enter a name.")

# Display Student List
st.markdown('<div class="subheader">Student List</div>', unsafe_allow_html=True)
students = manager.students
if students:
    student_ids = [student.id for student in students]
    selected_id = st.selectbox("Select a Student ID", student_ids, format_func=lambda id: f"{id} ({next(student.name for student in students if student.id == id)})")
else:
    st.write("No students available.")

# Enroll Student
st.markdown('<div class="subheader">Enroll Student</div>', unsafe_allow_html=True)
if students:
    course = st.text_input("Enter Course Name:")
    if st.button("Enroll Student"):
        if selected_id and course:
            manager.enroll_student(selected_id, course)
            st.success(f"Student ID {selected_id} enrolled in course '{course}'.")
        else:
            st.error("Please enter both ID and course.")

# View Student Balance
st.markdown('<div class="subheader">View Student Balance</div>', unsafe_allow_html=True)
if students:
    if st.button("View Balance"):
        balance = manager.view_student_balance(selected_id)
        if balance is not None:
            st.write(f"Balance for Student ID {selected_id}: ${balance}")
        else:
            st.error("Student ID not found.")

# Pay Student Fee
st.markdown('<div class="subheader">Pay Student Fee</div>', unsafe_allow_html=True)
fee_amount = st.number_input("Enter Amount to Pay:", min_value=0, step=1, key="pay_fee_amount")
if st.button("Pay Fee"):
    if selected_id and fee_amount > 0:
        manager.pay_student_fee(selected_id, fee_amount)
        st.success(f"Fee of ${fee_amount} paid for Student ID {selected_id}.")
    else:
        st.error("Please enter both ID and amount.")

# Show Student Status
st.markdown('<div class="subheader">Show Student Status</div>', unsafe_allow_html=True)
if st.button("Show Status"):
    status = manager.show_student_status(selected_id)
    if status:
        st.write(f"ID: {status['ID']}")
        st.write(f"Name: {status['Name']}")
        st.write(f"Courses: {', '.join(status['Courses'])}")
        st.write(f"Balance: ${status['Balance']}")
    else:
        st.error("Student ID not found.")

# Remove Student
st.markdown('<div class="subheader">Remove Student</div>', unsafe_allow_html=True)
if students:
    remove_id = st.selectbox("Select Student ID to Remove", student_ids, format_func=lambda id: f"{id} ({next(student.name for student in students if student.id == id)})")
    if st.button("Remove Student"):
        if remove_id:
            manager.remove_student(remove_id)
            st.success(f"Student ID {remove_id} removed successfully.")
            st.experimental_rerun()
        else:
            st.error("Please select a student ID.")

# Exit option
if st.button("Exit"):
    st.markdown('<div class="exit-message">Thank you for using the Student Management System Application!</div>', unsafe_allow_html=True)
    st.stop()
