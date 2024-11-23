

-- Table: Hotel
CREATE TABLE Hotel (
    Hotel_ID NUMBER PRIMARY KEY,
    H_Name VARCHAR2(50) NOT NULL,
    Address VARCHAR2(100) NOT NULL
);

-- Table: Room
CREATE TABLE Room (
    Room_No NUMBER PRIMARY KEY,
    Status VARCHAR2(20) DEFAULT 'UNOCCUPIED',
    R_Capacity NUMBER NOT NULL,
    Hotel_ID NUMBER NOT NULL,
    FOREIGN KEY (Hotel_ID) REFERENCES Hotel(Hotel_ID)
);

-- Table: Hotel_Service
CREATE TABLE Hotel_Service (
    Service_ID NUMBER PRIMARY KEY,
    Service_Description VARCHAR2(100) NOT NULL,
    Ser_Cost NUMBER NOT NULL
);

-- Table: Guest
CREATE TABLE Guest (
    Guest_ID NUMBER PRIMARY KEY,
    G_Name VARCHAR2(50) NOT NULL,
    ContactInfo VARCHAR2(50)
);

-- Table: Staff
CREATE TABLE Staff (
    Staff_ID NUMBER PRIMARY KEY,
    Staff_Name VARCHAR2(50) NOT NULL,
    Salary NUMBER NOT NULL,
    Hotel_ID NUMBER NOT NULL,
    FOREIGN KEY (Hotel_ID) REFERENCES Hotel(Hotel_ID)
);

-- Table: Staff_Role
CREATE TABLE Staff_Role (
    Role_ID NUMBER PRIMARY KEY,
    R_Position VARCHAR2(50) NOT NULL,
    Dept VARCHAR2(50) NOT NULL,
    Staff_ID NUMBER NOT NULL,
    FOREIGN KEY (Staff_ID) REFERENCES Staff(Staff_ID)
);

-- Table: Supplier
CREATE TABLE Supplier (
    Supplier_ID NUMBER NOT NULL,
    Items_Supplied VARCHAR2(20),
    Hotel_ID NUMBER NOT NULL,
    Order_No NUMBER NOT NULL PRIMARY KEY,
    CONSTRAINT Hotel_Supplied FOREIGN KEY (Hotel_ID) REFERENCES Hotel(Hotel_ID)
);

-- Decomposed Table: Inventory_Details
CREATE TABLE Inventory_Details (
    Inventory_ID NUMBER PRIMARY KEY,
    Hotel_ID NUMBER NOT NULL,
    Item_Name VARCHAR2(50) NOT NULL,
    Quantity NUMBER NOT NULL,
    Reorder_Level VARCHAR2(20) CHECK (Reorder_Level IN ('Satisfactory', 'Refill Required'))
);

-- Decomposed Table: Order_Hotel_Mapping
CREATE TABLE Order_Hotel_Mapping (
    Order_No NUMBER PRIMARY KEY,
    Hotel_ID NUMBER NOT NULL,
    FOREIGN KEY (Hotel_ID) REFERENCES Hotel(Hotel_ID)
);

-- Table: Other_Guests
CREATE TABLE Other_Guests (
    OG_Name VARCHAR2(50),
    ContactInfo VARCHAR2(50),
    Guest_ID NUMBER NOT NULL,
    FOREIGN KEY (Guest_ID) REFERENCES Guest(Guest_ID)
);

-- Table: Payment
CREATE TABLE Payment (
    Invoice_ID NUMBER UNIQUE,
    Payment_Date DATE NOT NULL,
    Pay_Method VARCHAR2(20),
    Guest_ID NUMBER NOT NULL,
    FOREIGN KEY (Guest_ID) REFERENCES Guest(Guest_ID)
);

-- Decomposed Table: Reservation_Details
CREATE TABLE Reservation_Details (
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
);

-- Decomposed Table: Room_Hotel_Mapping
CREATE TABLE Room_Hotel_Mapping (
    Room_No NUMBER PRIMARY KEY,
    Hotel_ID NUMBER NOT NULL,
    FOREIGN KEY (Hotel_ID) REFERENCES Hotel(Hotel_ID)
);

-- Decomposed Table: Guest_Reservation_Mapping
CREATE TABLE Guest_Reservation_Mapping (
    Guest_ID NUMBER NOT NULL,
    Reservation_ID NUMBER NOT NULL,
    PRIMARY KEY (Guest_ID, Reservation_ID),
    FOREIGN KEY (Guest_ID) REFERENCES Guest(Guest_ID),
    FOREIGN KEY (Reservation_ID) REFERENCES Reservation_Details(Reservation_ID)
);

-- Table: Check_in_out
CREATE TABLE Check_in_out (
    Reservation_ID NUMBER PRIMARY KEY,
    Status VARCHAR2(20) DEFAULT 'OCCUPIED',
    Check_in_out VARCHAR2(20) DEFAULT 'Checked-in',
    FOREIGN KEY (Reservation_ID) REFERENCES Reservation_Details(Reservation_ID)
);
