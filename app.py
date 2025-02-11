from flask import Flask, render_template, request
import sqlite3
import re
import datetime
import os

app = Flask(__name__)

def department_exists(department):
    try:
        conn = sqlite3.connect('company.db')
        cursor = conn.cursor()
        cursor.execute("SELECT Name FROM Departments WHERE Name COLLATE NOCASE = ?", (department,))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False

def get_employees_by_department(department):
    try:
        conn = sqlite3.connect('company.db')
        cursor = conn.cursor()
        cursor.execute("SELECT Name, Department, Salary, Hire_Date FROM Employees WHERE Department COLLATE NOCASE = ?", (department,))
        employees = cursor.fetchall()
        conn.close()
        return employees
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []

def get_manager_of_department(department):
    try:
        conn = sqlite3.connect('company.db')
        cursor = conn.cursor()
        cursor.execute("SELECT Manager FROM Departments WHERE Name COLLATE NOCASE = ?", (department,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

def get_employees_hired_after(date):
    try:
        conn = sqlite3.connect('company.db')
        cursor = conn.cursor()
        cursor.execute("SELECT Name, Department, Salary, Hire_Date FROM Employees WHERE Hire_Date > ?", (date,))
        employees = cursor.fetchall()
        conn.close()
        return employees
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []

def get_total_salary(department):
    try:
        conn = sqlite3.connect('company.db')
        cursor = conn.cursor()
        cursor.execute("SELECT SUM(Salary) FROM Employees WHERE Department COLLATE NOCASE = ?", (department,))
        total = cursor.fetchone()[0]
        conn.close()
        return total if total else 0
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return 0

def format_employees(employees):
    if not employees:
        return "No employees found."
    formatted = ["Employees found:"]
    for emp in employees:
        formatted.append(f"Name: {emp[0]}, Department: {emp[1]}, Salary: ${emp[2]}, Hire Date: {emp[3]}")
    return "\n".join(formatted)

def process_query(query):
    query = query.strip()
    
    # Show all employees in department
    match = re.match(r'(?i)Show me all employees in the (.*?) department', query)
    if match:
        department = match.group(1).strip()
        if not department_exists(department):
            return f"Department '{department}' not found."
        employees = get_employees_by_department(department)
        return format_employees(employees) if employees else f"No employees found in {department} department."
    
    # Manager of department
    match = re.match(r'(?i)Who is the manager of the (.*?) department', query)
    if match:
        department = match.group(1).strip()
        if not department_exists(department):
            return f"Department '{department}' not found."
        manager = get_manager_of_department(department)
        return f"The manager of {department} department is {manager}." if manager else f"No manager found for {department} department."
    
    # Employees hired after date
    match = re.match(r'(?i)List all employees hired after (.*)', query)
    if match:
        date_str = match.group(1).strip()
        try:
            hire_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return "Invalid date format. Please use YYYY-MM-DD."
        employees = get_employees_hired_after(hire_date)
        return format_employees(employees) if employees else f"No employees hired after {date_str} found."
    
    # Total salary expense for department
    match = re.match(r'(?i)What is the total salary expense for the (.*?) department', query)
    if match:
        department = match.group(1).strip()
        if not department_exists(department):
            return f"Department '{department}' not found."
        total = get_total_salary(department)
        return f"The total salary expense for {department} department is ${total}."
    
    return "Sorry, I couldn't understand your query. Please try another question."

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form.get('query', '')
        response = process_query(user_input)
        return response
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)