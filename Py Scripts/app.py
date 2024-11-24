import tkinter as tk
from tkinter import *
import cx_Oracle
import oracledb

# Initialize main Tkinter window
root = Tk()
root.title('Hotel DBMS GUI')
root.geometry("570x310")

# Ensure OPTIONS has at least one placeholder value
OPTIONS = ["Select a Table"]

# Define frames
login = Frame(root)
mainwindow = Frame(root)
query_page = Frame(root)
create_page = Frame(root)
alter_page = Frame(root)
drop_page = Frame(root)

# Function to switch between frames
def frameraise(frame):
    frame.tkraise()

# Arrange frames on the grid
for frame in (login, mainwindow, query_page, create_page, alter_page, drop_page):
    frame.grid(row=0, column=0, sticky='news')

# Login-related variables
username = None
password = None
cursor = None
connection = None

# Create connection to Oracle database
def get_connection():
    username = "XXXXXX"
    password = "XXXXXX"
    dsn = "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(Host=oracle.scs.ryerson.ca)(Port=1521))(CONNECT_DATA=(SID=orcl)))"
    
    try:
        # Try to connect to the database
        conn = oracledb.connect(user=username, password=password, dsn=dsn)
        return conn
    except oracledb.Error as e:
        print(f"An error has occurred while connecting to the database: {e}")
        return None

# Query table
def query_click():
    translated_query = table.get().translate({ord("'"): None, ord(","): None, ord("("): None, ord(")"): None})
    query = f"SELECT * FROM {translated_query}"
    result.config(state=NORMAL)
    result.delete('1.0', END)
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        result.insert(END, rows if rows else "No data found")
    except Exception as e:
        result.insert(END, f"Error: {e}")
    result.config(state=DISABLED)

# Create table dynamically
def create_dynamic_table():
    table_name = table_name_entry.get()
    columns = columns_entry.get()

    # Form the CREATE TABLE SQL query
    create_table_sql = f"CREATE TABLE {table_name} ({columns})"

    try:
        cursor.execute(create_table_sql)
        connection.commit()
        OPTIONS.append(table_name)
        updateMenu()
        result.insert(END, "Table created successfully.")
    except Exception as e:
        result.insert(END, f"Error: {e}")
    result.config(state=DISABLED)

# Drop table
def drop_click():
    sql_drop = f"DROP TABLE {table_name_entry.get()}"
    result2.config(state=NORMAL)
    result2.delete('1.0', END)
    try:
        cursor.execute(sql_drop)
        connection.commit()
        OPTIONS.remove(table_name_entry.get())
        updateMenu()
        result2.insert(END, "Table dropped successfully.")
    except Exception as e:
        result2.insert(END, f"Error: {e}")
    result2.config(state=DISABLED)

# Alter table
def alter_click():
    buffer = targetTable.get()
    values = ["('101', 150)", "('102', 200)", "('103', 250)"]
    result2.config(state=NORMAL)
    result2.delete('1.0', END)
    for value in values:
        sql_alter = f"INSERT INTO {buffer} (RoomNumber, Price) VALUES {value}"
        try:
            cursor.execute(sql_alter)
            connection.commit()
            result2.insert(END, f"Inserted: {value}\n")
        except Exception as e:
            result2.insert(END, f"Error: {e}\n")
    result2.config(state=DISABLED)

# Exit the application
def exit_click():
    if cursor:
        cursor.close()
    if connection:
        connection.close()
    root.quit()

# Update dropdown menus
def updateMenu():
    tables_ddown["menu"].delete(0, "end")
    alter_ddown["menu"].delete(0, "end")
    for table_name in OPTIONS:
        tables_ddown["menu"].add_command(label=table_name, command=tk._setit(table, table_name))
        alter_ddown["menu"].add_command(label=table_name, command=tk._setit(targetTable, table_name))
    table.set(OPTIONS[0])
    targetTable.set(OPTIONS[0])

root.protocol("WM_DELETE_WINDOW", exit_click)

# Login page layout
welcome = Label(login, text="Welcome to Hotel DBMS GUI.")
ins = Label(login, text="Enter your username and password")
user = Entry(login, width=20)
pwd = Entry(login, show="*", width=20)
login_button = Button(login, text="Login", command=get_connection)
welcome.pack()
ins.pack()
user.pack()
pwd.pack()
login_button.pack()

# Main window layout
to_query = Button(mainwindow, text="Query Table", width=30, command=lambda: frameraise(query_page))
to_create = Button(mainwindow, text="Create Table", width=30, command=lambda: frameraise(create_page))
to_alter = Button(mainwindow, text="Alter Table", width=30, command=lambda: frameraise(alter_page))
to_drop = Button(mainwindow, text="Drop Table", width=30, command=drop_click)
exit_button = Button(mainwindow, text="Exit", width=30, command=exit_click)
to_query.pack()
to_create.pack()
to_alter.pack()
to_drop.pack()
exit_button.pack()

# Query page layout
table = StringVar(query_page)
table.set(OPTIONS[0])
tables_ddown = OptionMenu(query_page, table, *OPTIONS)
query_button = Button(query_page, text="Query", width=30, command=query_click)
result = Text(query_page, wrap=WORD, height=10, width=50, state=DISABLED)
back_button = Button(query_page, text="Back", width=30, command=lambda: frameraise(mainwindow))
tables_ddown.pack()
query_button.pack()
result.pack()
back_button.pack()

# Create page layout (Dynamic Table Creation)
Label(create_page, text="Create a New Table", font=("Helvetica", 16)).pack(pady=20)

Label(create_page, text="Table Name:").pack()
table_name_entry = Entry(create_page, width=30)
table_name_entry.pack(pady=5)

Label(create_page, text="Columns (e.g., name VARCHAR2(100), age INT):").pack()
columns_entry = Entry(create_page, width=50)
columns_entry.pack(pady=5)

create_button = Button(create_page, text="Create Table", width=30, command=create_dynamic_table)
create_button.pack(pady=20)

result = Text(create_page, wrap=WORD, height=10, width=50, state=DISABLED)
result.pack(pady=10)

back_button_create = Button(create_page, text="Back", width=30, command=lambda: frameraise(mainwindow))
back_button_create.pack(pady=20)

# Alter page layout
targetTable = StringVar(alter_page)
targetTable.set(OPTIONS[0])
alter_ddown = OptionMenu(alter_page, targetTable, *OPTIONS)
alter_button = Button(alter_page, text="Populate Table", width=30, command=alter_click)
result2 = Text(alter_page, wrap=WORD, height=10, width=50, state=DISABLED)
back_button2 = Button(alter_page, text="Back", width=30, command=lambda: frameraise(mainwindow))
alter_ddown.pack()
alter_button.pack()
result2.pack()
back_button2.pack()

# Start the application
frameraise(login)
root.mainloop()
