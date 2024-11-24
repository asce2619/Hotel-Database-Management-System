import tkinter as tk
from tkinter import *
import cx_Oracle

# Initialize Oracle client
cx_Oracle.init_oracle_client(lib_dir="/Users/n/Hotel DBMS/Hotel-Database-Management-System/oracle_client")

# Create main root window
root = Tk()
root.title('Hotel DBMS GUI')
root.geometry("600x400")

# List of dynamic options (tables fetched from the database)
OPTIONS = [""]

# Creating application frames
login_frame = Frame(root)
main_frame = Frame(root)
query_frame = Frame(root)
create_frame = Frame(root)
alter_frame = Frame(root)
drop_frame = Frame(root)

# Function to raise frames
def raise_frame(frame):
    frame.tkraise()

# Initialize frames in the window
for frame in (login_frame, main_frame, query_frame, create_frame, alter_frame, drop_frame):
    frame.grid(row=0, column=0, sticky='news')

# Function to connect to the database
def connect_to_db():
    # Extract username and password from entry fields
    username = user_entry.get()
    password = pwd_entry.get()

    # Attempt to establish a connection
    try:
        # Connect to Oracle DB
        global connection, cursor
        connection = cx_Oracle.connect(
            user=username,
            password=password,
            dsn="(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=oracle.scs.ryerson.ca)(PORT=1521))(CONNECT_DATA=(SID=orcl)))"
        )

        # Check if the connection was successful
        if connection.version:
            print(f"Connected to Oracle DB, version: {connection.version}")
            cursor = connection.cursor()
            feedback_label.config(text="Login successful!", fg="green")

            # Fetch table names to populate dropdown options
            cursor.execute("SELECT table_name FROM user_tables ORDER BY table_name")
            tables = cursor.fetchall()
            OPTIONS.clear()
            OPTIONS.extend([table[0] for table in tables])

            # Update dropdown menus in the GUI
            update_menu()

            # Switch to the main menu frame
            raise_frame(main_frame)
        else:
            feedback_label.config(text="Login failed. Please try again.", fg="red")
    except cx_Oracle.DatabaseError as e:
        # Handle connection errors
        error, = e.args
        feedback_label.config(text=f"Error: {error.message}", fg="red")

        # Clear input fields to prompt for correct login credentials
        user_entry.delete(0, END)
        pwd_entry.delete(0, END)

# Update dropdown menus with fetched table names
def update_menu():
    query_menu["menu"].delete(0, "end")
    alter_menu["menu"].delete(0, "end")
    for table_name in OPTIONS:
        query_menu["menu"].add_command(label=table_name, command=tk._setit(selected_table, table_name))
        alter_menu["menu"].add_command(label=table_name, command=tk._setit(selected_alter_table, table_name))
    if OPTIONS:
        selected_table.set(OPTIONS[0])
        selected_alter_table.set(OPTIONS[0])

# Query table function
def query_table():
    table_name = selected_table.get()
    result_text.config(state=NORMAL)
    result_text.delete("1.0", END)
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        for row in rows:
            result_text.insert(END, f"{row}\n")
    except Exception as e:
        result_text.insert(END, f"Query error: {e}")
    result_text.config(state=DISABLED)

# Create test table function
def create_test_table():
    try:
        cursor.execute("CREATE TABLE TEST_ROOM (RoomNumber VARCHAR2(50), Price INT)")
        connection.commit()
        feedback_main.config(text="Table 'TEST_ROOM' created.", fg="green")
        OPTIONS.append("TEST_ROOM")
        update_menu()
    except Exception as e:
        feedback_main.config(text=f"Error creating table: {e}", fg="red")

# Drop test table function
def drop_test_table():
    try:
        cursor.execute("DROP TABLE TEST_ROOM")
        connection.commit()
        feedback_main.config(text="Table 'TEST_ROOM' dropped.", fg="green")
        OPTIONS.remove("TEST_ROOM")
        update_menu()
    except Exception as e:
        feedback_main.config(text=f"Error dropping table: {e}", fg="red")

# Populate table (Alter example)
def populate_table():
    table_name = selected_alter_table.get()
    data = [("101", 150), ("102", 200), ("103", 250)]
    feedback_alter.config(text="", fg="green")
    try:
        for room, price in data:
            cursor.execute(f"INSERT INTO {table_name} (RoomNumber, Price) VALUES (:1, :2)", (room, price))
        connection.commit()
        feedback_alter.config(text="Data inserted successfully!", fg="green")
    except Exception as e:
        feedback_alter.config(text=f"Error inserting data: {e}", fg="red")

# Logout and close connection
def logout():
    try:
        cursor.close()
        connection.close()
    except:
        pass
    root.quit()

# GUI Layout for Login Frame
Label(login_frame, text="Hotel DBMS Login", font=("Helvetica", 16)).pack(pady=20)
Label(login_frame, text="Username:").pack()
user_entry = Entry(login_frame, width=30)
user_entry.pack(pady=5)
Label(login_frame, text="Password:").pack()
pwd_entry = Entry(login_frame, show='*', width=30)
pwd_entry.pack(pady=5)
Button(login_frame, text="Login", command=connect_to_db).pack(pady=20)
feedback_label = Label(login_frame, text="", fg="red")
feedback_label.pack(pady=10)

# GUI Layout for Main Frame
Label(main_frame, text="Hotel DBMS Main Menu", font=("Helvetica", 16)).pack(pady=20)
Button(main_frame, text="Query Table", command=lambda: raise_frame(query_frame)).pack(pady=10)
Button(main_frame, text="Create Test Table", command=create_test_table).pack(pady=10)
Button(main_frame, text="Drop Test Table", command=drop_test_table).pack(pady=10)
Button(main_frame, text="Alter Table", command=lambda: raise_frame(alter_frame)).pack(pady=10)
Button(main_frame, text="Logout", command=logout).pack(pady=20)
feedback_main = Label(main_frame, text="", fg="green")
feedback_main.pack(pady=10)

# GUI Layout for Query Frame
Label(query_frame, text="Query a Table", font=("Helvetica", 16)).pack(pady=20)
selected_table = StringVar(query_frame)
query_menu = OptionMenu(query_frame, selected_table, *OPTIONS)
query_menu.pack(pady=10)
Button(query_frame, text="Run Query", command=query_table).pack(pady=10)
result_text = Text(query_frame, wrap=WORD, width=60, height=10, state=DISABLED)
result_text.pack(pady=10)
Button(query_frame, text="Back", command=lambda: raise_frame(main_frame)).pack(pady=20)

# GUI Layout for Alter Frame
Label(alter_frame, text="Alter a Table (Insert Data)", font=("Helvetica", 16)).pack(pady=20)
selected_alter_table = StringVar(alter_frame)
alter_menu = OptionMenu(alter_frame, selected_alter_table, *OPTIONS)
alter_menu.pack(pady=10)
Button(alter_frame, text="Insert Data", command=populate_table).pack(pady=10)
feedback_alter = Label(alter_frame, text="", fg="green")
feedback_alter.pack(pady=10)
Button(alter_frame, text="Back", command=lambda: raise_frame(main_frame)).pack(pady=20)

# Start the Application
raise_frame(login_frame)
root.mainloop()
