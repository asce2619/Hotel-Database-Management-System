import tkinter as tk
from tkinter import *
from tkinter import ttk  # For dropdown functionality
import cx_Oracle

# Initialize Oracle client
cx_Oracle.init_oracle_client(lib_dir="/Users/n/Hotel DBMS/Hotel-Database-Management-System/oracle_client")

# Create main root window
root = Tk()
root.title('Hotel DBMS GUI')
root.geometry("600x400")

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
main_frame = Frame(root)
create_frame = Frame(root)
drop_frame = Frame(root)
insert_frame = Frame(root)

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
        feedback_label.config(text="Login successful!", fg="green")
        raise_frame(main_frame)
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        feedback_label.config(text=f"Error: {error.message}", fg="red")

# Function to create tables
def create_tables():
    try:
        for sql in CREATE_TABLES_SQL:
            cursor.execute(sql)
        connection.commit()
        feedback_create.config(text="Tables created successfully!", fg="green")
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        feedback_create.config(text=f"Error: {error.message}", fg="red")

# Function to drop tables
def drop_tables():
    try:
        for sql in DROP_TABLES_SQL:
            cursor.execute(sql)
        connection.commit()
        feedback_drop.config(text="Tables dropped successfully!", fg="green")
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        feedback_drop.config(text=f"Error: {error.message}", fg="red")

# Function to insert data into all tables
def insert_data_into_all_tables():
    try:
        for table, queries in INSERT_DATA_SQL.items():
            for query in queries:
                cursor.execute(query)
        connection.commit()
        feedback_insert_all.config(text="Data inserted into all tables successfully!", fg="green")
    except cx_Oracle.DatabaseError as e:
        feedback_insert_all.config(text=f"Error: {e}", fg="red")
 
# Function to insert data into selected table
def insert_data_into_selected_table():
    selected_table = table_dropdown.get()
    if selected_table == "Select a table":
        feedback_table_insert.config(text="Please select a table!", fg="red")
        return
    try:
        for query in INSERT_DATA_SQL.get(selected_table, []):
            cursor.execute(query)
        connection.commit()
        feedback_table_insert.config(text=f"Data inserted into {selected_table} successfully!", fg="green")
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        feedback_table_insert.config(text=f"Error: {error.message}", fg="red")

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
Button(main_frame, text="Create Tables", command=lambda: raise_frame(create_frame)).pack(pady=10)
Button(main_frame, text="Drop Tables", command=lambda: raise_frame(drop_frame)).pack(pady=10)
Button(main_frame, text="Insert Data", command=lambda: raise_frame(insert_frame)).pack(pady=10)
Button(main_frame, text="Logout", command=logout).pack(pady=20)

# GUI Layout for Create Frame
Label(create_frame, text="Create Tables", font=("Helvetica", 16)).pack(pady=20)
Button(create_frame, text="Create All Tables", command=create_tables).pack(pady=10)
feedback_create = Label(create_frame, text="", fg="green")
feedback_create.pack(pady=10)
Button(create_frame, text="Back", command=lambda: raise_frame(main_frame)).pack(pady=20)

# GUI Layout for Drop Frame
Label(drop_frame, text="Drop Tables", font=("Helvetica", 16)).pack(pady=20)
Button(drop_frame, text="Drop All Tables", command=drop_tables).pack(pady=10)
feedback_drop = Label(drop_frame, text="", fg="green")
feedback_drop.pack(pady=10)
Button(drop_frame, text="Back", command=lambda: raise_frame(main_frame)).pack(pady=20)

# GUI Layout for Insert Frame
Label(insert_frame, text="Insert Data", font=("Helvetica", 16)).pack(pady=20)

# Insert All Data Button
Button(insert_frame, text="Insert All Data", command=insert_data_into_all_tables).pack(pady=10)
feedback_insert_all = Label(insert_frame, text="", fg="green")
feedback_insert_all.pack(pady=10)

# Dropdown for specific table insertion
Label(insert_frame, text="Insert into Specific Table:").pack(pady=5)
table_dropdown = ttk.Combobox(insert_frame, values=list(INSERT_DATA_SQL.keys()), state="readonly")
table_dropdown.set("Select a table")
table_dropdown.pack(pady=10)
Button(insert_frame, text="Insert Data into Selected Table", command=insert_data_into_selected_table).pack(pady=10)
feedback_table_insert = Label(insert_frame, text="", fg="green")
feedback_table_insert.pack(pady=10)

Button(insert_frame, text="Back", command=lambda: raise_frame(main_frame)).pack(pady=20)

# Initialize all frames
for frame in (login_frame, main_frame, create_frame, drop_frame, insert_frame):
    frame.grid(row=0, column=0, sticky='news')

# Start the application
raise_frame(login_frame)
root.mainloop()
