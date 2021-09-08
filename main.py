from tkinter import *
from tkinter import messagebox
from ttkthemes import themed_tk as tk
from db import Database

db = Database()


def populate_list():
    students_list.delete(0, END)
    for row in db.fetch():
        students_list.insert(END, row)


def add_item():
    if remark_text.get() == '' or name_text.get() == '' or roll_no.get() == '' or gpa_text.get() == '':
        messagebox.showerror('Required Fields', 'Please include all fields')
        return
    try:
        db.insert(remark_text.get(), name_text.get(),
                  roll_no.get(), gpa_text.get())
        students_list.delete(0, END)
        students_list.insert(END, f"""(remark_text.get(), name_text.get(),
                                roll_no.get(), remark_text.get())""")
    except Exception as e:
        messagebox.showerror('Floats Only', 'Please Insert Proper Value')
    # clear_text()
    populate_list()


def select_item(event):
    try:
        global selected_item
        index = students_list.curselection()[0]
        selected_item = students_list.get(index)

        remark_entry.delete(0, END)
        remark_entry.insert(END, selected_item[0])
        name_entry.delete(0, END)
        name_entry.insert(END, selected_item[1])
        # roll_no.delete(0, END)
        roll_no.set(selected_item[2])
        gpa_entry.delete(0, END)
        gpa_entry.insert(END, selected_item[3])
    except IndexError:
        pass

def remove_item():
    db.remove(selected_item[-1])
    clear_text()
    populate_list()


def update_item():
    try:
        db.update(selected_item[-1], remark_text.get(), name_text.get(),
                  roll_no.get(), gpa_text.get())
        populate_list()
    except Exception as e:
        messagebox.showerror('Floats Only', 'Please Insert Proper Value')


def clear_text():
    remark_entry.delete(0, END)
    name_entry.delete(0, END)
    roll_no.set(0)
    gpa_entry.delete(0, END)


# Create window object
app = tk.ThemedTk()
app.get_themes()
app.set_theme("yaru")

# remark
remark_text = StringVar()
remark_label = Label(app, text='Remark', font=('bold', 11), pady=20, padx=20)
remark_label.grid(row=0, column=0, sticky=W)
remark_entry = Entry(app, textvariable=remark_text)
remark_entry.grid(row=0, column=1)
# Student Name
name_text = StringVar()
name_label = Label(app, text='Full Name', font=('bold', 11), pady=20, padx=20)
name_label.grid(row=0, column=2, sticky=W)
name_entry = Entry(app, textvariable=name_text)
name_entry.grid(row=0, column=3)

# ROLL_No
roll_no = IntVar()
roll_no_label = Label(app, text='Student Roll No.', font=('bold', 11), pady=20, padx=20)
roll_no_label.grid(row=1, column=0, sticky=W)
roll_no_entry = Entry(app, textvariable=roll_no)
roll_no_entry.grid(row=1, column=1)

# GPA:
gpa_text = DoubleVar()
gpa_label = Label(app, text='GPA.', font=('bold', 11), pady=10, padx=10)
gpa_label.grid(row=1, column=2, sticky=W)
gpa_entry = Entry(app, textvariable=gpa_text)
gpa_entry.grid(row=1, column=3)

# Students List (Listbox)
students_list = Listbox(app, height=20, width=50, border=0)
students_list.grid(row=0, column=4, columnspan=4, rowspan=12, pady=20, padx=20)

# Create scrollbar
scrollbar = Scrollbar(app)
scrollbar.grid(row=3, column=3)
# Set scroll to listbox
students_list.configure(yscrollcommand=scrollbar.set)
scrollbar.configure(command=students_list.yview)
# Bind select
students_list.bind('<<ListboxSelect>>', select_item)

# Buttons
add_btn = Button(app, text='Add Student', width=12, command=add_item)
add_btn.grid(row=2, column=0, pady=20)

remove_btn = Button(app, text='Remove Student', width=12, command=remove_item)
remove_btn.grid(row=2, column=1)

update_btn = Button(app, text='Update Student', width=12, command=update_item)
update_btn.grid(row=2, column=2)

clear_btn = Button(app, text='Clear Student', width=12, command=clear_text)
clear_btn.grid(row=2, column=3)

app.title('SYIT:A')
app.geometry('1100x450')


# Populate data
populate_list()

# Start program
app.mainloop()


# To create an executable, install pyinstaller and run
# '''
# pyinstaller --onefile --add-binary='/System/Library/Frameworks/Tk.framework/Tk':'tk' --add-binary='/System/Library/Frameworks/Tcl.framework/Tcl':'tcl' part_manager.py
# '''