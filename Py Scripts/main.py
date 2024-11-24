import tkinter as tk
from tkinter import *
from tkinter import ttk  # For dropdown functionality
import cx_Oracle
import pandas as pd
import customtkinter as ctk

# Initialize Oracle client
cx_Oracle.init_oracle_client(lib_dir="/Users/n/Hotel DBMS/Hotel-Database-Management-System/oracle_client")


# Set the appearance mode and color theme
ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "dark-blue", "green"

# Initialize the root window
root = ctk.CTk()
root.title("Hotel Database Management GUI")
root.geometry("1200x1200")  # Default size
root.minsize(800, 600)      # Set a minimum window size
root.maxsize(1920, 1080)    # Optionally set a maximum window size

# Configure grid for responsive layout
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)


CREATE_TABLES_SQL = [
    """CREATE TABLE Hotel (
        Hotel_ID NUMBER PRIMARY KEY,
        H_Name VARCHAR2(50) NOT NULL,
        Address VARCHAR2(100) NOT NULL
    )""",
    """CREATE TABLE Room (
        Room_No NUMBER PRIMARY KEY,
        Status VARCHAR2(20) DEFAULT 'UNOCCUPIED',
        R_Capacity NUMBER NOT NULL,
        Hotel_ID NUMBER NOT NULL,
        FOREIGN KEY (Hotel_ID) REFERENCES Hotel(Hotel_ID)
    )""",
    """CREATE TABLE Guest (
        Guest_ID NUMBER PRIMARY KEY,
        G_Name VARCHAR2(50) NOT NULL,
        ContactInfo VARCHAR2(50)
    )""",
    """CREATE TABLE Hotel_Service (
        Service_ID NUMBER PRIMARY KEY,
        Service_Description VARCHAR2(100) NOT NULL,
        Ser_Cost NUMBER NOT NULL
    )""",
    """CREATE TABLE Staff (
        Staff_ID NUMBER PRIMARY KEY,
        Staff_Name VARCHAR2(50) NOT NULL,
        Salary NUMBER NOT NULL,
        Hotel_ID NUMBER NOT NULL,
        FOREIGN KEY (Hotel_ID) REFERENCES Hotel(Hotel_ID)
    )""",
    """CREATE TABLE Staff_Role (
        Role_ID NUMBER PRIMARY KEY,
        R_Position VARCHAR2(50) NOT NULL,
        Dept VARCHAR2(50) NOT NULL,
        Staff_ID NUMBER NOT NULL,
        FOREIGN KEY (Staff_ID) REFERENCES Staff(Staff_ID)
    )""",
    """CREATE TABLE Supplier (
        Supplier_ID NUMBER NOT NULL,
        Items_Supplied VARCHAR2(20),
        Hotel_ID NUMBER NOT NULL,
        Order_No NUMBER NOT NULL PRIMARY KEY,
        FOREIGN KEY (Hotel_ID) REFERENCES Hotel(Hotel_ID)
    )""",
    """CREATE TABLE Inventory_Details (
        Inventory_ID NUMBER PRIMARY KEY,
        Hotel_ID NUMBER NOT NULL,
        Item_Name VARCHAR2(50) NOT NULL,
        Quantity NUMBER NOT NULL,
        Reorder_Level VARCHAR2(20) CHECK (Reorder_Level IN ('Satisfactory', 'Refill Required'))
    )""",
    """CREATE TABLE Order_Hotel_Mapping (
        Order_No NUMBER PRIMARY KEY,
        Hotel_ID NUMBER NOT NULL,
        FOREIGN KEY (Hotel_ID) REFERENCES Hotel(Hotel_ID)
    )""",
    """CREATE TABLE Other_Guests (
        OG_Name VARCHAR2(50),
        ContactInfo VARCHAR2(50),
        Guest_ID NUMBER NOT NULL,
        FOREIGN KEY (Guest_ID) REFERENCES Guest(Guest_ID)
    )""",
    """CREATE TABLE Payment (
        Invoice_ID NUMBER UNIQUE,
        Payment_Date DATE NOT NULL,
        Pay_Method VARCHAR2(20),
        Guest_ID NUMBER NOT NULL,
        FOREIGN KEY (Guest_ID) REFERENCES Guest(Guest_ID)
    )""",
    """CREATE TABLE Reservation_Details (
        Reservation_ID NUMBER PRIMARY KEY,
        Hotel_ID NUMBER NOT NULL,
        Guest_ID NUMBER NOT NULL,
        Room_No NUMBER,
        Status VARCHAR2(20) DEFAULT 'RESERVED',
        Stay_Cost NUMBER NOT NULL,
        Start_Date DATE NOT NULL,
        End_Date DATE NOT NULL,
        FOREIGN KEY (Guest_ID) REFERENCES Guest(Guest_ID),
        FOREIGN KEY (Hotel_ID) REFERENCES Hotel(Hotel_ID),
        FOREIGN KEY (Room_No) REFERENCES Room(Room_No)
    )""",
    """CREATE TABLE Room_Hotel_Mapping (
        Room_No NUMBER PRIMARY KEY,
        Hotel_ID NUMBER NOT NULL,
        FOREIGN KEY (Hotel_ID) REFERENCES Hotel(Hotel_ID)
    )""",
    """CREATE TABLE Guest_Reservation_Mapping (
        Guest_ID NUMBER NOT NULL,
        Reservation_ID NUMBER NOT NULL,
        PRIMARY KEY (Guest_ID, Reservation_ID),
        FOREIGN KEY (Guest_ID) REFERENCES Guest(Guest_ID),
        FOREIGN KEY (Reservation_ID) REFERENCES Reservation_Details(Reservation_ID)
    )""",
    """CREATE TABLE Check_in_out (
        Reservation_ID NUMBER PRIMARY KEY,
        Status VARCHAR2(20) DEFAULT 'OCCUPIED',
        Check_in_out VARCHAR2(20) DEFAULT 'Checked-in',
        FOREIGN KEY (Reservation_ID) REFERENCES Reservation_Details(Reservation_ID)
    )"""
]


DROP_TABLES_SQL = [
    "DROP TABLE Check_in_out CASCADE CONSTRAINTS",
    "DROP TABLE Guest_Reservation_Mapping CASCADE CONSTRAINTS",
    "DROP TABLE Room_Hotel_Mapping CASCADE CONSTRAINTS",
    "DROP TABLE Reservation_Details CASCADE CONSTRAINTS",
    "DROP TABLE Payment CASCADE CONSTRAINTS",
    "DROP TABLE Other_Guests CASCADE CONSTRAINTS",
    "DROP TABLE Order_Hotel_Mapping CASCADE CONSTRAINTS",
    "DROP TABLE Inventory_Details CASCADE CONSTRAINTS",
    "DROP TABLE Supplier CASCADE CONSTRAINTS",
    "DROP TABLE Staff_Role CASCADE CONSTRAINTS",
    "DROP TABLE Staff CASCADE CONSTRAINTS",
    "DROP TABLE Guest CASCADE CONSTRAINTS",
    "DROP TABLE Hotel_Service CASCADE CONSTRAINTS",
    "DROP TABLE Room CASCADE CONSTRAINTS",
    "DROP TABLE Hotel CASCADE CONSTRAINTS"
]


INSERT_DATA_SQL = {
    "Hotel": [
        "INSERT INTO Hotel VALUES (1, 'Hotel Sunshine', '123 Main Street')",
        "INSERT INTO Hotel VALUES (2, 'Hotel Moonlight', '456 Oak Avenue')",
    ],
    "Room": [
        "INSERT INTO Room VALUES (101, 'UNOCCUPIED', 2, 1)",
        "INSERT INTO Room VALUES (102, 'UNOCCUPIED', 4, 2)",
    ],
    "Guest": [
        "INSERT INTO Guest VALUES (1, 'John Doe', '123-456-7890')",
        "INSERT INTO Guest VALUES (2, 'Jane Smith', '987-654-3210')"
    ],
    "Hotel_Service": [
        "INSERT INTO Hotel_Service VALUES (201, 'Room Cleaning', 20)",
        "INSERT INTO Hotel_Service VALUES (202, 'Laundry', 15)"
    ],
    "Staff": [
        "INSERT INTO Staff VALUES (301, 'Alice Johnson', 5000, 1)",
        "INSERT INTO Staff VALUES (302, 'Bob Brown', 4000, 2)"
    ],
    "Staff_Role": [
        "INSERT INTO Staff_Role VALUES (401, 'Manager', 'Administration', 301)",
        "INSERT INTO Staff_Role VALUES (402, 'Receptionist', 'Front Desk', 302)"
    ],
    "Supplier": [
        "INSERT INTO Supplier VALUES (501, 'Bedsheets', 1, 1001)",
        "INSERT INTO Supplier VALUES (502, 'Shampoo', 2, 1002)"
    ],
    "Inventory_Details": [
        "INSERT INTO Inventory_Details VALUES (601, 1, 'Bedsheets', 50, 'Satisfactory')",
        "INSERT INTO Inventory_Details VALUES (602, 2, 'Shampoo', 30, 'Refill Required')"
    ],
    "Order_Hotel_Mapping": [
        "INSERT INTO Order_Hotel_Mapping VALUES (1001, 1)",
        "INSERT INTO Order_Hotel_Mapping VALUES (1002, 2)"
    ],
    "Other_Guests": [
        "INSERT INTO Other_Guests VALUES ('Charlie White', '555-123-4567', 1)",
        "INSERT INTO Other_Guests VALUES ('Daisy Green', '555-987-6543', 2)"
    ],
    "Payment": [
        "INSERT INTO Payment VALUES (1101, TO_DATE('2024-01-01', 'YYYY-MM-DD'), 'Cash', 1)",
        "INSERT INTO Payment VALUES (1102, TO_DATE('2024-01-02', 'YYYY-MM-DD'), 'Card', 2)"
    ],
    "Reservation_Details": [
        "INSERT INTO Reservation_Details VALUES (1201, 1, 1, 101, 'RESERVED', 200, TO_DATE('2024-02-01', 'YYYY-MM-DD'), TO_DATE('2024-02-03', 'YYYY-MM-DD'))",
        "INSERT INTO Reservation_Details VALUES (1202, 2, 2, 102, 'RESERVED', 300, TO_DATE('2024-03-01', 'YYYY-MM-DD'), TO_DATE('2024-03-04', 'YYYY-MM-DD'))"
    ],
    "Room_Hotel_Mapping": [
        "INSERT INTO Room_Hotel_Mapping VALUES (101, 1)",
        "INSERT INTO Room_Hotel_Mapping VALUES (102, 2)"
    ],
    "Guest_Reservation_Mapping": [
        "INSERT INTO Guest_Reservation_Mapping VALUES (1, 1201)",
        "INSERT INTO Guest_Reservation_Mapping VALUES (2, 1202)"
    ],
    "Check_in_out": [
        "INSERT INTO Check_in_out VALUES (1201, 'OCCUPIED', 'Checked-in')",
        "INSERT INTO Check_in_out VALUES (1202, 'RESERVED', 'Checked-out')"
    ]
}


# Creating application frames
login_frame = Frame(root)
login_frame = ctk.CTkFrame(root)
main_frame = ctk.CTkFrame(root)
create_frame = ctk.CTkFrame(root)
drop_frame = ctk.CTkFrame(root)
insert_frame = ctk.CTkFrame(root)
query_frame = ctk.CTkFrame(root)
advance_query_frame = ctk.CTkFrame(root)
update_frame = ctk.CTkFrame(root)
show_table_frame = ctk.CTkFrame(root)

import customtkinter as ctk
from tkinter import messagebox, Toplevel, Text, Scrollbar, END, RIGHT, BOTTOM, VERTICAL, HORIZONTAL, BOTH, NONE
import pandas as pd
import cx_Oracle

# Function to raise frames
def raise_frame(frame):
    frame.tkraise()

# Function to connect to the database
def connect_to_db():
    global connection, cursor
    username = user_entry.get()
    password = pwd_entry.get()
    try:
        connection = cx_Oracle.connect(
            user=username,
            password=password,
            dsn="(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=oracle.scs.ryerson.ca)(PORT=1521))(CONNECT_DATA=(SID=orcl)))"
        )
        cursor = connection.cursor()
        feedback_label.configure(text="Login successful!", text_color="green")
        raise_frame(main_frame)
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        feedback_label.configure(text=f"Error: {error.message}", text_color="red")

# Functions for CRUD operations
def create_tables():
    try:
        for sql in CREATE_TABLES_SQL:
            cursor.execute(sql)
        connection.commit()
        feedback_create.configure(text="Tables created successfully!", text_color="green")
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        feedback_create.configure(text=f"Error: {error.message}", text_color="red")

# Function to drop tables
def drop_tables():
    try:
        for sql in DROP_TABLES_SQL:
            cursor.execute(sql)
        connection.commit()
        feedback_drop.configure(text="Tables dropped successfully!", text_color="green")
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        feedback_drop.configure(text=f"Error: {error.message}", text_color="red")

# Function to insert data into all tables
def insert_data_into_all_tables():
    try:
        for table, queries in INSERT_DATA_SQL.items():
            for query in queries:
                cursor.execute(query)
        connection.commit()
        feedback_insert_all.configure(text="Data inserted into all tables successfully!", text_color="green")
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        feedback_insert_all.configure(text=f"Error: {error.message}", text_color="red")

# Function to insert data into selected table
def insert_data_into_selected_table():
    selected_table = table_dropdown.get()
    if selected_table == "Select a table":
        feedback_table_insert.configure(text="Please select a table!", text_color="red")
        return
    try:
        for query in INSERT_DATA_SQL.get(selected_table, []):
            cursor.execute(query)
        connection.commit()
        feedback_table_insert.configure(text=f"Data inserted into {selected_table} successfully!", text_color="green")
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        feedback_table_insert.configure(text=f"Error: {error.message}", text_color="red")

# Function to query data
def query_data():
    selected_table = query_table_dropdown.get()
    if selected_table == "Select a table":
        feedback_query.configure(text="Please select a table to query!", text_color="red")
        return
    try:
        cursor.execute(f"SELECT * FROM {selected_table}")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        
        if rows:
            df = pd.DataFrame(rows, columns=columns)
            result_window = ctk.CTkToplevel(root)
            result_window.title(f"Data from {selected_table}")
            result_window.geometry("800x400")

            text = ctk.CTkTextbox(result_window, wrap=NONE)
            text.pack(fill=BOTH, expand=True)
            text.insert(END, df.to_string(index=False))

            scrollbar_y = ctk.CTkScrollbar(result_window, orientation=VERTICAL, command=text.yview)
            scrollbar_y.pack(side=RIGHT, fill=ctk.Y)
            scrollbar_x = ctk.CTkScrollbar(result_window, orientation=HORIZONTAL, command=text.xview)
            scrollbar_x.pack(side=BOTTOM, fill=ctk.X)
            text.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

            feedback_query.configure(text="Query executed successfully!", text_color="green")
        else:
            feedback_query.configure(text="No data found for the query.", text_color="red")
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        feedback_query.configure(text=f"Error: {error.message}", text_color="red")

# Function to run advanced query
def advance_query_data():
    query = custom_query_entry.get("1.0", END).strip()
    if not query:
        feedback_advance_query.configure(text="Please enter a query!", text_color="red")
        return
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        
        if rows:
            df = pd.DataFrame(rows, columns=columns)
            result_window = ctk.CTkToplevel(root)
            result_window.title("Advanced Query Results")
            result_window.geometry("800x400")

            text = ctk.CTkTextbox(result_window, wrap=NONE)
            text.pack(fill=BOTH, expand=True)
            text.insert(END, df.to_string(index=False))

            scrollbar_y = ctk.CTkScrollbar(result_window, orientation=VERTICAL, command=text.yview)
            scrollbar_y.pack(side=RIGHT, fill=ctk.Y)
            scrollbar_x = ctk.CTkScrollbar(result_window, orientation=HORIZONTAL, command=text.xview)
            scrollbar_x.pack(side=BOTTOM, fill=ctk.X)
            text.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

            feedback_advance_query.configure(text="Query executed successfully!", text_color="green")
        else:
            feedback_advance_query.configure(text="No data found for the query.", text_color="red")
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        feedback_advance_query.configure(text=f"Error: {error.message}", text_color="red")

def update_data():
    selected_table = update_table_dropdown.get()
    update_query = update_query_entry.get("1.0", "end").strip()
    
    if selected_table == "Select a table" or not update_query:
        feedback_update.configure(text="Please select a table and provide an update query!", text_color="red")
        return

    try:
        cursor.execute(update_query)
        connection.commit()
        feedback_update.configure(text=f"Record updated successfully in {selected_table}!", text_color="green")
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        feedback_update.configure(text=f"Error: {error.message}", text_color="red")

def show_table_data():
    selected_table = show_table_dropdown.get()
    if selected_table == "Select a table":
        feedback_show_table.configure(text="Please select a table to display data!", text_color="red")
        return
    
    try:
        # Execute query to fetch all data from the selected table
        cursor.execute(f"SELECT * FROM {selected_table}")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]  # Extract column names
        
        if rows:
            # Create a DataFrame for better presentation
            df = pd.DataFrame(rows, columns=columns)
            
            # Create a new window to display the data
            result_window = ctk.CTkToplevel(root)
            result_window.title(f"Data from {selected_table}")
            result_window.geometry("800x400")
            
            # Create a text widget to display the DataFrame
            text_widget = ctk.CTkTextbox(result_window, wrap="none")
            text_widget.pack(fill="both", expand=True)
            text_widget.insert("end", df.to_string(index=False))
            
            # Add scrollbars
            scrollbar_y = ctk.CTkScrollbar(result_window, orientation="vertical", command=text_widget.yview)
            scrollbar_y.pack(side="right", fill="y")
            scrollbar_x = ctk.CTkScrollbar(result_window, orientation="horizontal", command=text_widget.xview)
            scrollbar_x.pack(side="bottom", fill="x")
            text_widget.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
            
            feedback_show_table.configure(text="Data displayed successfully!", text_color="green")
        else:
            feedback_show_table.configure(text="No data found for the selected table.", text_color="red")
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        feedback_show_table.configure(text=f"Error: {error.message}", text_color="red")


# Logout and close connection
def logout():
    try:
        cursor.close()
        connection.close()
    except:
        pass
    root.destroy()

# Login Frame
ctk.CTkLabel(login_frame, text="Hotel DBMS Login", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)

# Username Label and Entry
ctk.CTkLabel(login_frame, text="Username:", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
user_entry = ctk.CTkEntry(login_frame, width=250, placeholder_text="Enter your username")
user_entry.pack(pady=5)

# Password Label and Entry
ctk.CTkLabel(login_frame, text="Password:", font=ctk.CTkFont(size=14)).pack(pady=(10, 5))
pwd_entry = ctk.CTkEntry(login_frame, show="*", width=250, placeholder_text="Enter your password")
pwd_entry.pack(pady=5)

# Login Button
ctk.CTkButton(login_frame, text="Login", command=connect_to_db, width=200, fg_color="#4CAF50").pack(pady=20)

# Feedback Label
feedback_label = ctk.CTkLabel(login_frame, text="", text_color="red", font=ctk.CTkFont(size=12))
feedback_label.pack(pady=10)


# GUI Layout for Main Frame
ctk.CTkLabel(main_frame, text="Hotel DBMS Main Menu", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
ctk.CTkButton(main_frame, text="Create Tables", command=lambda: raise_frame(create_frame), width=200).pack(pady=10)
ctk.CTkButton(main_frame, text="Drop Tables", command=lambda: raise_frame(drop_frame), width=200).pack(pady=10)
ctk.CTkButton(main_frame, text="Insert Data", command=lambda: raise_frame(insert_frame), width=200).pack(pady=10)
ctk.CTkButton(main_frame, text="Query Data", command=lambda: raise_frame(query_frame), width=200).pack(pady=10)
ctk.CTkButton(main_frame, text="Advance Query Data", command=lambda: raise_frame(advance_query_frame), width=200).pack(pady=10)
ctk.CTkButton(main_frame, text="Update Table", command=lambda: raise_frame(update_frame), width=200).pack(pady=10)
ctk.CTkButton(main_frame, text="Show Table Data", command=lambda: raise_frame(show_table_frame), width=200).pack(pady=10)
ctk.CTkButton(main_frame, text="Logout", command=logout, width=200).pack(pady=20)

# GUI Layout for Create Frame
ctk.CTkLabel(create_frame, text="Create Tables", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
ctk.CTkButton(create_frame, text="Create All Tables", command=create_tables, width=200).pack(pady=10)
feedback_create = ctk.CTkLabel(create_frame, text="", text_color="green")
feedback_create.pack(pady=10)
ctk.CTkButton(create_frame, text="Back", command=lambda: raise_frame(main_frame), width=200).pack(pady=20)

# GUI Layout for Drop Frame
ctk.CTkLabel(drop_frame, text="Drop Tables", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
ctk.CTkButton(drop_frame, text="Drop All Tables", command=drop_tables, width=200).pack(pady=10)
feedback_drop = ctk.CTkLabel(drop_frame, text="", text_color="green")
feedback_drop.pack(pady=10)
ctk.CTkButton(drop_frame, text="Back", command=lambda: raise_frame(main_frame), width=200).pack(pady=20)

# GUI Layout for Insert Frame
ctk.CTkLabel(insert_frame, text="Insert Data", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
ctk.CTkButton(insert_frame, text="Insert All Data", command=insert_data_into_all_tables, width=200).pack(pady=10)
feedback_insert_all = ctk.CTkLabel(insert_frame, text="", text_color="green")
feedback_insert_all.pack(pady=10)

# Dropdown for specific table insertion
ctk.CTkLabel(insert_frame, text="Insert into Specific Table:").pack(pady=5)
table_dropdown = ctk.CTkOptionMenu(insert_frame, values=list(INSERT_DATA_SQL.keys()))
table_dropdown.set("Select a table")
table_dropdown.pack(pady=10)
ctk.CTkButton(insert_frame, text="Insert Data into Selected Table", command=insert_data_into_selected_table, width=200).pack(pady=10)
feedback_table_insert = ctk.CTkLabel(insert_frame, text="", text_color="green")
feedback_table_insert.pack(pady=10)
ctk.CTkButton(insert_frame, text="Back", command=lambda: raise_frame(main_frame), width=200).pack(pady=20)

# GUI Layout for Query Frame
ctk.CTkLabel(query_frame, text="Query Data from Table", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
query_table_dropdown = ctk.CTkOptionMenu(query_frame, values=list(INSERT_DATA_SQL.keys()))
query_table_dropdown.set("Select a table")
query_table_dropdown.pack(pady=10)
ctk.CTkButton(query_frame, text="Query Data", command=query_data, width=200).pack(pady=10)
feedback_query = ctk.CTkLabel(query_frame, text="", text_color="green")
feedback_query.pack(pady=10)
ctk.CTkButton(query_frame, text="Back", command=lambda: raise_frame(main_frame), width=200).pack(pady=20)

# GUI Layout for Advance Query Data Frame
ctk.CTkLabel(advance_query_frame, text="Advance Query Data", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
ctk.CTkLabel(advance_query_frame, text="Enter your custom SQL query below:").pack(pady=10)
custom_query_entry = ctk.CTkTextbox(advance_query_frame, height=300, width=600)
custom_query_entry.pack(pady=10)
ctk.CTkButton(advance_query_frame, text="Execute Query", command=advance_query_data, width=200).pack(pady=10)
feedback_advance_query = ctk.CTkLabel(advance_query_frame, text="", text_color="green")
feedback_advance_query.pack(pady=10)
ctk.CTkButton(advance_query_frame, text="Back", command=lambda: raise_frame(main_frame), width=200).pack(pady=20)

# GUI Layout for Update Frame
ctk.CTkLabel(update_frame, text="Update Records in Table", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
ctk.CTkLabel(update_frame, text="Select a table to update:").pack(pady=10)
update_table_dropdown = ctk.CTkOptionMenu(update_frame, values=list(INSERT_DATA_SQL.keys()))
update_table_dropdown.set("Select a table")
update_table_dropdown.pack(pady=10)
ctk.CTkLabel(update_frame, text="Enter your SQL UPDATE query below:").pack(pady=10)
update_query_entry = ctk.CTkTextbox(update_frame, height=100, width=500)
update_query_entry.pack(pady=10)
ctk.CTkButton(update_frame, text="Execute Update", command=update_data, width=200).pack(pady=10)
feedback_update = ctk.CTkLabel(update_frame, text="", text_color="green")
feedback_update.pack(pady=10)
ctk.CTkButton(update_frame, text="Back", command=lambda: raise_frame(main_frame), width=200).pack(pady=20)

# GUI Layout for Show Table Data Frame
ctk.CTkLabel(show_table_frame, text="Show Table Data", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
ctk.CTkLabel(show_table_frame, text="Select a table to display data:").pack(pady=10)
show_table_dropdown = ctk.CTkOptionMenu(show_table_frame, values=list(INSERT_DATA_SQL.keys()))
show_table_dropdown.set("Select a table")
show_table_dropdown.pack(pady=10)
ctk.CTkButton(show_table_frame, text="Show Data", command=show_table_data, width=200).pack(pady=10)
feedback_show_table = ctk.CTkLabel(show_table_frame, text="", text_color="green")
feedback_show_table.pack(pady=10)
ctk.CTkButton(show_table_frame, text="Back", command=lambda: raise_frame(main_frame), width=200).pack(pady=20)

# Ensure frames are instances of CTkFrame
for frame in (login_frame, main_frame, create_frame, drop_frame, insert_frame, query_frame, advance_query_frame, update_frame, show_table_frame):
    frame.grid(row=0, column=0, sticky='nsew')

# Configure root to allow responsive resizing
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Start the application with the login frame
raise_frame(login_frame)
root.mainloop()
