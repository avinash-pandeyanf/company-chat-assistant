import sqlite3

def init_db():
    conn = sqlite3.connect('company.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Employees (
            ID INTEGER PRIMARY KEY,
            Name TEXT,
            Department TEXT,
            Salary INTEGER,
            Hire_Date DATE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Departments (
            ID INTEGER PRIMARY KEY,
            Name TEXT,
            Manager TEXT
        )
    ''')

    employees = [
        (1, 'Alice', 'Sales', 50000, '2021-01-15'),
        (2, 'Bob', 'Engineering', 70000, '2020-06-10'),
        (3, 'Charlie', 'Marketing', 60000, '2022-03-20')
    ]
    cursor.executemany('INSERT INTO Employees VALUES (?, ?, ?, ?, ?)', employees)

    departments = [
        (1, 'Sales', 'Alice'),
        (2, 'Engineering', 'Bob'),
        (3, 'Marketing', 'Charlie')
    ]
    cursor.executemany('INSERT INTO Departments VALUES (?, ?, ?)', departments)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized.")