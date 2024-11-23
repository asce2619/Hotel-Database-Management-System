import tkinter as tk
from tkinter import *
import cx_Oracle

# Initialize Oracle client with the versioned path directly
cx_Oracle.init_oracle_client(lib_dir="/Users/n/Hotel DBMS/Hotel-Database-Management-System/oracle_client")

root = Tk()
root.title('Hotel DBMS GUI')
root.geometry("570x310")

OPTIONS = [""]  # This will be populated with table names later

# Creating window frames
login = Frame(root)
mainwindow = Frame(root)
query_page = Frame(root)
create_page = Frame(root)
alter_page = Frame(root)
drop_page = Frame(root)

# Function to switch frames
def frameraise(frame):
    frame.tkraise()

# Manage frames
for frame in (login, mainwindow, query_page, alter_page, drop_page):
    frame.grid(row=0, column=0, sticky='news')

# Create function to handle login
def create_connection():
    global username, password, cursor, connection
    username = user.get()
    password = pwd.get()
    try:
        connection = cx_Oracle.connect(user=username, password=password, dsn="(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=oracle.scs.ryerson.ca)(PORT=1521))(CONNECT_DATA=(SID=orcl)))")
        if connection.version != 0:
            print(connection.version)
            cursor = connection.cursor()
            frameraise(mainwindow)
            result.config(width=60, height=5)
            result2.config(width=60, height=5)
            cursor.execute("select table_name from user_tables order by table_name")
            optionList = cursor.fetchall()
            for string in optionList:
                OPTIONS.append(string)
            OPTIONS.remove("")
            updateMenu()
    except Exception as e:
        print(f"Error: {e}")  # Print the error to debug
        ins["text"] = "Invalid username/password. Please Try Again"
        user.delete(0, END)
        pwd.delete(0, END)

# Query table
def query_click():
    translated_query = table.get().translate({ord("'"): None, ord(','): None, ord('('): None, ord(')'): None})
    query = f'select * from {translated_query}'
    result.config(state=NORMAL)
    if result.get('1.0', END) != '':
        result.delete('1.0', END)
    try:
        cursor.execute(query)
        row = cursor.fetchall()
        result.insert(END, row)
    except:
        result.insert(END, "Query Command is incorrect or table does not exist")
    result.config(state=DISABLED)

# Create table
def insert_click():
    sql_create = 'CREATE TABLE TEST_ROOM (RoomNumber VARCHAR2(50), Price INT)'
    if result.get('1.0', END) != '':
        result.delete('1.0', END)
    try:
        cursor.execute(sql_create)
        updateLabel['text'] = "Table Created"
        OPTIONS.append("TEST_ROOM")
        updateMenu()
    except:
        updateLabel['text'] = "Table already exists"

# Drop table
def drop_click():
    sql_drop = "DROP TABLE TEST_ROOM"
    try:
        cursor.execute(sql_drop)
        updateLabel['text'] = 'Table Dropped'
        OPTIONS.remove("TEST_ROOM")
        updateMenu()
    except:
        updateLabel['text'] = "Table does not exist"

# Alter table
def alter_click():
    buffer = targetTable.get()
    values = ["('101', 150)", "('102', 200)", "('103', 250)"]
    result2.config(state=NORMAL)
    if result2.get('1.0', END) != '':
        result2.delete('1.0', END)
    for value in values:
        sql_alter = f"INSERT INTO {buffer}(RoomNumber, Price) VALUES {value}"
        try:
            cursor.execute(sql_alter)
            connection.commit()
            result2.insert(END, f'Inserted: {value}, ')
        except:
            result2.insert(END, f"Error with: {sql_alter}")
            break
    result2.config(state=DISABLED)

# Exit application
def exit_click():
    cursor.close()
    connection.close()
    close_window()

def close_window():
    root.quit()
    exit(0)

def updateMenu():
    tables_ddown["menu"].delete(0, "end")
    alter_ddown["menu"].delete(0, "end")
    for string in OPTIONS:
        tables_ddown["menu"].add_command(label=string, command=tk._setit(table, string))
        alter_ddown["menu"].add_command(label=string, command=tk._setit(targetTable, string))
    table.set(OPTIONS[0])
    targetTable.set(OPTIONS[0])

root.protocol("WM_DELETE_WINDOW", close_window)

# Login page GUI
welcome = Label(login, text='Welcome to Hotel DBMS GUI.')
ins = Label(login, text="Enter your username and password")
user_frame = Frame(login)
user_text = Label(user_frame, text='Username')
user = Entry(user_frame, width=20)
user_text.pack(side=LEFT, padx=5)
user.pack(side=RIGHT, padx=5)
pass_frame = Frame(login)
pass_text = Label(pass_frame, text='Password')
pwd = Entry(pass_frame, show='*', width=20)
pass_text.pack(side=LEFT, padx=5)
pwd.pack(side=RIGHT, padx=5)
login_button = Button(login, text='Login', command=create_connection)

# Main window GUI
to_query = Button(mainwindow, text='Query Table', width=30, command=lambda: frameraise(query_page))
to_create = Button(mainwindow, text='Create Table', width=30, command=insert_click)
to_alter = Button(mainwindow, text='Alter Table', width=30, command=lambda: frameraise(alter_page))
to_drop = Button(mainwindow, text='Drop Table', width=30, command=drop_click)
introLabel = Label(mainwindow, text="Welcome to the Hotel DBMS")
updateLabel = Label(mainwindow, text="Select an option")
exit_button = Button(mainwindow, text='Exit', width=30, command=exit_click)

# Query page GUI
query_button = Button(query_page, text='Query', width=30, command=query_click)
result = Text(query_page, wrap=WORD, height=0, width=0, state=DISABLED)
table = StringVar(query_page)
tables_ddown = OptionMenu(query_page, table, *OPTIONS)
back_button = Button(query_page, text='Back', width=30, command=lambda: frameraise(mainwindow))

# Alter page GUI
alter_button = Button(alter_page, text='Populate Table', width=30, command=alter_click)
result2 = Text(alter_page, wrap=WORD, height=0, width=0, state=DISABLED)
targetTable = StringVar(alter_page)
alter_ddown = OptionMenu(alter_page, targetTable, *OPTIONS)
back_button2 = Button(alter_page, text='Back', width=30, command=lambda: frameraise(mainwindow))

# Drop page GUI
drop_button = Button(drop_page, text='Drop Table', width=30, command=drop_click)
back_button3 = Button(drop_page, text='Back', width=30, command=lambda: frameraise(mainwindow))

# Layout for each frame
# (Similar layout logic as in your original script)

# Initialize application
frameraise(login)
root.mainloop()
