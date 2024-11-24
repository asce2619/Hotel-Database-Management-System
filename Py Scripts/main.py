import tkinter as tk
from tkinter import *
import cx_Oracle

# Initialize Oracle client
cx_Oracle.init_oracle_client(lib_dir="/Users/n/Hotel DBMS/Hotel-Database-Management-System/oracle_client")

# Create main root window
root = Tk()
root.title('Hotel DBMS GUI')
root.geometry("600x400")

# SQL commands for creating tables
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
    """CREATE TABLE Hotel_Service (
        Service_ID NUMBER PRIMARY KEY,
        Service_Description VARCHAR2(100) NOT NULL,
        Ser_Cost NUMBER NOT NULL
    )""",
    """CREATE TABLE Guest (
        Guest_ID NUMBER PRIMARY KEY,
        G_Name VARCHAR2(50) NOT NULL,
        ContactInfo VARCHAR2(50)
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
        CONSTRAINT Hotel_Supplied FOREIGN KEY (Hotel_ID) REFERENCES Hotel(Hotel_ID)
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

# SQL commands for dropping tables
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

# Insert sample data
INSERT_DATA_SQL = [
    "INSERT INTO Hotel VALUES (26, 'Sunshine', '123 Main Street')",
    "INSERT INTO Hotel VALUES (17, 'Moonlight', '21 Ashmore Street')",
    "INSERT INTO Hotel VALUES (39, 'DayNight', '19 Clearview Street')",
    "INSERT INTO Room VALUES (1, 'UNOCCUPIED', 2, 26)",
    "INSERT INTO Room VALUES (2, 'UNOCCUPIED', 3, 17)",
    "INSERT INTO Room VALUES (3, 'UNOCCUPIED', 4, 39)",
    "INSERT INTO Guest VALUES (1, 'Jannis Saini', '(416) 123-4567')",
    "INSERT INTO Guest VALUES (2, 'Rose Pagano', '(647) 649-8888')",
    "INSERT INTO Guest VALUES (3, 'Nitya Malik', '(647) 829-3721')",
    "INSERT INTO Hotel_Service VALUES (101, 'Room Cleaning', 50)",
    "INSERT INTO Hotel_Service VALUES (102, 'Laundry', 30)",
    "INSERT INTO Hotel_Service VALUES (103, 'Spa Services', 100)",
    "INSERT INTO Staff VALUES (201, 'John Doe', 3000, 26)",
    "INSERT INTO Staff VALUES (202, 'Jane Smith', 3500, 17)",
    "INSERT INTO Staff VALUES (203, 'Emily Brown', 3200, 39)",
    "INSERT INTO Staff_Role VALUES (301, 'Manager', 'Administration', 201)",
    "INSERT INTO Staff_Role VALUES (302, 'Receptionist', 'Front Desk', 202)",
    "INSERT INTO Staff_Role VALUES (303, 'Cleaner', 'Housekeeping', 203)",
    "INSERT INTO Supplier VALUES (401, 'Bedsheets', 26, 1001)",
    "INSERT INTO Supplier VALUES (402, 'Shampoo', 17, 1002)",
    "INSERT INTO Supplier VALUES (403, 'Soap Bars', 39, 1003)",
    "INSERT INTO Inventory_Details VALUES (501, 26, 'Bedsheets', 50, 'Satisfactory')",
    "INSERT INTO Inventory_Details VALUES (502, 17, 'Shampoos', 30, 'Refill Required')",
    "INSERT INTO Inventory_Details VALUES (503, 39, 'Soap Bars', 100, 'Satisfactory')",
    "INSERT INTO Order_Hotel_Mapping VALUES (1001, 26)",
    "INSERT INTO Order_Hotel_Mapping VALUES (1002, 17)",
    "INSERT INTO Order_Hotel_Mapping VALUES (1003, 39)",
    "INSERT INTO Reservation_Details VALUES (701, 26, 1, 1, 'RESERVED', 500, TO_DATE('2024-11-01', 'YYYY-MM-DD'), TO_DATE('2024-11-05', 'YYYY-MM-DD'))",
    "INSERT INTO Reservation_Details VALUES (702, 17, 2, 2, 'RESERVED', 750, TO_DATE('2024-10-15', 'YYYY-MM-DD'), TO_DATE('2024-10-20', 'YYYY-MM-DD'))",
    "INSERT INTO Room_Hotel_Mapping VALUES (1, 26)",
    "INSERT INTO Room_Hotel_Mapping VALUES (2, 17)",
    "INSERT INTO Room_Hotel_Mapping VALUES (3, 39)",
    "INSERT INTO Guest_Reservation_Mapping VALUES (1, 701)",
    "INSERT INTO Guest_Reservation_Mapping VALUES (2, 702)",
    "INSERT INTO Other_Guests VALUES ('Anna White', '(905) 555-6789', 1)",
    "INSERT INTO Other_Guests VALUES ('Mark Green', '(416) 456-7890', 2)",
    "INSERT INTO Payment VALUES (601, TO_DATE('2024-09-30', 'YYYY-MM-DD'), 'CASH', 1)",
    "INSERT INTO Payment VALUES (602, TO_DATE('2024-10-15', 'YYYY-MM-DD'), 'CREDIT', 2)",
    "INSERT INTO Check_in_out VALUES (701, 'OCCUPIED', 'Checked-in')",
    "INSERT INTO Check_in_out VALUES (702, 'UNOCCUPIED', 'Checked-out')"
]



# Creating application frames
login_frame = Frame(root)
main_frame = Frame(root)
create_frame = Frame(root)
drop_frame = Frame(root)
insert_frame = Frame(root)

# Function to raise frames
def raise_frame(frame):
    frame.tkraise()

# Initialize frames in the window
for frame in (login_frame, main_frame, create_frame, drop_frame, insert_frame):
    frame.grid(row=0, column=0, sticky='news')

# Function to connect to the database
def connect_to_db():
    username = user_entry.get()
    password = pwd_entry.get()
    try:
        global connection, cursor
        connection = cx_Oracle.connect(
            user=username,
            password=password,
            dsn="(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=oracle.scs.ryerson.ca)(PORT=1521))(CONNECT_DATA=(SID=orcl)))"
        )
        if connection.version:
            cursor = connection.cursor()
            feedback_label.config(text="Login successful!", fg="green")
            raise_frame(main_frame)
        else:
            feedback_label.config(text="Login failed. Please try again.", fg="red")
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        feedback_label.config(text=f"Error: {error.message}", fg="red")
        user_entry.delete(0, END)
        pwd_entry.delete(0, END)

# Function to create tables
def create_tables():
    try:
        for sql in CREATE_TABLES_SQL:
            cursor.execute(sql)
        connection.commit()
        feedback_create.config(text="All tables created successfully!", fg="green")
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        feedback_create.config(text=f"Error: {error.message}", fg="red")

# Function to drop tables
def drop_tables():
    try:
        for sql in reversed(DROP_TABLES_SQL):
            cursor.execute(sql)
        connection.commit()
        feedback_drop.config(text="All tables dropped successfully!", fg="green")
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        feedback_drop.config(text=f"Error: {error.message}", fg="red")

# Function to insert data
def insert_data():
    try:
        for sql in INSERT_DATA_SQL:
            cursor.execute(sql)
        connection.commit()
        feedback_insert.config(text="Data inserted successfully!", fg="green")
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        feedback_insert.config(text=f"Error: {error.message}", fg="red")

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
Button(insert_frame, text="Insert Sample Data", command=insert_data).pack(pady=10)
feedback_insert = Label(insert_frame, text="", fg="green")
feedback_insert.pack(pady=10)
Button(insert_frame, text="Back", command=lambda: raise_frame(main_frame)).pack(pady=20)

# Start the Application
raise_frame(login_frame)
root.mainloop()
