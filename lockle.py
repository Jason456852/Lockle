import tkinter as tk
from tkinter import simpledialog
import mysql.connector as sql
import argon2
from cryptography.fernet import Fernet
import base64

'''GUI settings'''
window = tk.Tk()
window.title("Lockle 2.0")
# window.iconphoto(True, tk.PhotoImage(file='icon.png'))
window.resizable(False, False)
window.geometry("1100x600")
'''sidebar'''
sidebar = tk.Frame(master=window, width=97, height=600, borderwidth=2)
sidebar.pack(side=tk.LEFT, expand=False)
'''display side'''
display = tk.Frame(master=window, width=1000, height=600, borderwidth=2, relief=tk.SUNKEN)
display.pack(fill=tk.BOTH, expand=True)



'''inputs'''
inputs_list = [None]
f = None

'''database setup'''
db = None
while True:
    """CREATE A DATABASE WITH init.py BEFORE RUNNING THE FILE"""
    passwd = simpledialog.askstring(" ", "Input database password:")
    try:
        db = sql.connect(host="""SQL HOST""", user="""SQL USER""", passwd=passwd, database='accounts')
    except:
        pass
    else:
        break
mycursor = db.cursor()

'''key setup'''
while True:
    try:
        pd = simpledialog.askstring(" ", "Input password:").encode('utf-8')
        salt = simpledialog.askstring(" ", "Input salt:").encode('utf-8')
        key = base64.urlsafe_b64encode(argon2.hash_password(password=pd, salt=salt)[:32])
        encrypted = """CREATE A ENCRYPTED BTYES WITH pd AND salt IN init.py FILE"""
        f = Fernet(key)
        decrypted = f.decrypt(encrypted)
        break
    except:
        pass



'''database access function'''
def access(values=[]):
    query_dict = {
        "insert": "insert into ac (target, email, username, password) values (%s, %s, %s, %s);",
        "update": {
                "target": "update ac set target = %s where target = %s;",
                "email": "update ac set email = %s where target = %s;",
                "username": "update ac set username = %s where target = %s;",
                "password": "update ac set password = %s where target = %s;"
            },
        "delete": "delete from ac where target = %s;",
        "select": "select * from ac where target = %s;",
        "list": "select * from ac;"
    }
    success, query = int(1), values[0]
    length = len(values)
    if query == "insert" and length == 5:
        target, email, username, password = values[1], values[2], values[3], values[4]
        mycursor.execute(query_dict[query], (target, email, username, password))
        db.commit()
        success = int(0)
    if query == "update" and length == 4:
        set, new, target = values[1], values[2], values[3]
        mycursor.execute(query_dict[query][set], (new, target))
        db.commit()
        success = int(0)
    if query == "delete" and length == 2:
        target = values[1]
        mycursor.execute(query_dict[query], ([target]))
        db.commit()
        success = int(0)
    if query == "select" and length == 2:
        target = values[1]
        mycursor.execute(query_dict[query], ([target]))
        for widget in display.winfo_children():
            if any(widget.grid_info()) and widget.grid_info()["row"] >= 5:
                widget.grid_remove()
        description = ["Target", "Email", "Username", "Password"]
        for n, i in enumerate(description):
            temp = tk.Label(master=display, text=i).grid(row=3, column=n, sticky='w')
        line = ""
        for i in range(16):
            line += "------------"
        tk.Label(master=display, text=line).grid(row=2, column=0, columnspan=4, sticky='w')
        tk.Label(master=display, text=line).grid(row=4, column=0, columnspan=4, sticky='w')
        for r, i in enumerate(mycursor):
            if r >= (page-1) * 15 and r < page * 15:
                for c in range(4):
                    if c == 0:
                        tk.Label(master=display, text=i[c]).grid(row=r+5, column=c, sticky='w')
                    else:
                        tk.Label(master=display, text=f.decrypt(i[c].encode()).decode()).grid(row=r+5, column=c, sticky='w')
        success = int(0)
    if query == "list" and length == 2:
        page = values[1]
        mycursor.execute(query_dict[query])
        for widget in display.winfo_children():
            if any(widget.grid_info()) and widget.grid_info()["row"] >= 5:
                widget.grid_remove()
        description = ["Target", "Email", "Username", "Password"]
        for n, i in enumerate(description):
            temp = tk.Label(master=display, text=i).grid(row=3, column=n, sticky='w')
        line = ""
        for i in range(16):
            line += "------------"
        tk.Label(master=display, text=line).grid(row=2, column=0, columnspan=4, sticky='w')
        tk.Label(master=display, text=line).grid(row=4, column=0, columnspan=4, sticky='w')
        for r, i in enumerate(mycursor):
            if r >= (page-1) * 15 and r < page * 15:
                for c in range(4):
                    if c == 0:
                        tk.Label(master=display, text=i[c]).grid(row=r+5, column=c, sticky='w')
                    else:
                        tk.Label(master=display, text=f.decrypt(i[c].encode()).decode()).grid(row=r+5, column=c, sticky='w')
        success = int(0)
    return success



'''buttons'''
btn_insert = tk.Button(master=sidebar, text="Insert", width=12, relief=tk.GROOVE, command=(lambda: display_mode(0, insert_widgets)))
btn_update = tk.Button(master=sidebar, text="Update", width=12, relief=tk.GROOVE, command=(lambda: display_mode(1, update_widgets)))
btn_delete = tk.Button(master=sidebar, text="Delete", width=12, relief=tk.GROOVE, command=(lambda: display_mode(2, delete_widgets)))
btn_select = tk.Button(master=sidebar, text="Select", width=12, relief=tk.GROOVE, command=(lambda: display_mode(3, select_widgets)))
btn_list = tk.Button(master=sidebar, text="List", width=12, relief=tk.GROOVE, command=(lambda: display_mode(4, list_widget)))
btn_insert.place(x=0, y=0)
btn_update.place(x=0, y=30)
btn_delete.place(x=0, y=60)
btn_select.place(x=0, y=90)
btn_list.place(x=0, y=120)

'''insert display side'''
insert_widgets = {"title": [tk.Label(master=display, text="Insert", font=(None, 12, "bold"))],
                  "target": [tk.Label(master=display, text="Target:"), tk.Entry(master=display)],
                  "email": [tk.Label(master=display, text="Email:"), tk.Entry(master=display)],
                  "username": [tk.Label(master=display, text="Username:"), tk.Entry(master=display)],
                  "password": [tk.Label(master=display, text="Password:"), tk.Entry(master=display)]
                  }
'''update display side'''
update_widgets = {"title": [tk.Label(master=display, text="Update", font=(None, 12, "bold"))],
                  "set": [tk.Label(master=display, text="Set:"), tk.Entry(master=display)],
                  "new": [tk.Label(master=display, text="New Value:"), tk.Entry(master=display)],
                  "target": [tk.Label(master=display, text="Target:"), tk.Entry(master=display)]
                  }
'''delete display side'''
delete_widgets = {"title": [tk.Label(master=display, text="Delete", font=(None, 12, "bold"))],
                  "target": [tk.Label(master=display, text="Target:"), tk.Entry(master=display)]
                  }
'''select display side'''
select_widgets = {"title": [tk.Label(master=display, text="Select", font=(None, 12, "bold"))],
                  "target": [tk.Label(master=display, text="Target:"), tk.Entry(master=display)]
                  }
'''list display side'''
list_widget = {"title": [tk.Label(master=display, text="List", font=(None, 12, "bold"))],
               "page": [tk.Label(master=display, text="Page:"), tk.Entry(master=display)]
               }

'''grid size function'''
def display_mode(id, widgets):
    global inputs_list
    display.grid_columnconfigure(0, minsize=100)
    display.grid_columnconfigure(1, minsize=300)
    display.grid_columnconfigure(2, minsize=300)
    display.grid_columnconfigure(3, minsize=300)
    for widget in display.winfo_children():
            widget.grid_remove()
    for row, info in enumerate(widgets.values()):
        for column, widget in enumerate(info):
            widget.grid(row=row, column=column, sticky="w")
    id_tag = ["insert", "update", "delete", "select", "list"]
    inputs_list = [None]
    inputs_list[0] = id_tag[id]



'''insert function'''
def inserting():
    global inputs_list
    if any(inputs_list[1:]):
        if inputs_list[1] is not None:
            inputs_list[1] = inputs_list[1].lower()
            if inputs_list[2] is not None:
                inputs_list[2] = f.encrypt(inputs_list[2].encode()).decode()
            if inputs_list[3] is not None:
                inputs_list[3] = f.encrypt(inputs_list[3].encode()).decode()
            if inputs_list[4] is not None:
                inputs_list[4] = f.encrypt(inputs_list[4].encode()).decode()
            return access(inputs_list)
        else:
            return int(2)
    else:
        return int(1)

'''update function'''
def updating():
    global inputs_list
    if any(inputs_list[1:]):
        set = ["target", "email", "username", "password"]
        if inputs_list[1] in set:
            if inputs_list[3] is not None:
                inputs_list[3] = inputs_list[3].lower()
                if inputs_list[1] == "password" or inputs_list[1] == "username" or inputs_list[1] == "email":
                    if inputs_list[2] is not None:
                        inputs_list[2] = f.encrypt(inputs_list[2].encode()).decode()
                    else: 
                        return int(1)
                return access(inputs_list)
            return int(2)
        else:
            return int(3)
    return int(1)

'''delete function'''
def deleting():
    global inputs_list
    if inputs_list[1] is not None:
        inputs_list[1] = inputs_list[1].lower()
        return access(inputs_list)
    return int(1)

'''select function'''
def selecting():
    global inputs_list
    if inputs_list[1] is not None:
        inputs_list[1] = inputs_list[1].lower()
        return access(inputs_list)
    else:
        return int(1)

'''list function'''
def listing():
    global inputs_list
    if inputs_list[1] is not None:
        if inputs_list[1].isnumeric():
            inputs_list[1] = int(inputs_list[1])
            return access(inputs_list)
        else:
            return int(4)
    else:
        return int(1)



'''press ENTER to execute with given infomation'''
def enter_pressed(event):
    global inputs_list
    query = inputs_list[0].lower()
    for widget in display.winfo_children():
        if widget.winfo_class() == 'Entry' and widget.winfo_ismapped():
            entry_input = widget.get() if widget.get() else None
            inputs_list.append(entry_input)
    error_code, entry_info = 0, ""
    if query == "insert":
        error_code = inserting()
        entry_info = f"Target = {inputs_list[1]}\nEmail = {inputs_list[2]}\nUsername = {inputs_list[3]}\nPassword = {inputs_list[4]}"
    if query == "update":
        error_code = updating()
        entry_info = f"Set = {inputs_list[1]}\nNew = {inputs_list[2]}\nTarget = {inputs_list[3]}"
    if query == "delete":
        error_code = deleting()
        entry_info = f"Target = {inputs_list[1]}"
    if query == "select":
        error_code = selecting()
        entry_info = f"Target = {inputs_list[1]}"
    if query == "list":
        error_code = listing()
        entry_info = f"Page = {inputs_list[1]}"
    if error_code == 0:
        for widget in display.winfo_children():
            if widget.winfo_class() == 'Entry' and widget.winfo_ismapped():
                widget.delete(0, tk.END)
        success_str = f"Query: {query} finished.\n" + entry_info
        lbl_success_str = tk.Label(master=display, text=success_str)
        lbl_success_str.place(relx=0.52, rely=0.97, anchor="s")
        display.after(10000, lbl_success_str.destroy)
        inputs_list = [query]
    else:
        display.bell()
        error_code_message = ["", "Empty entries", "Empty target", "Set type not exist", "Not a number"]
        error_str = f"Error: {query} ({int(error_code)}: {error_code_message[error_code]}).\n" + entry_info
        lbl_error_str = tk.Label(master=display, text=error_str)
        lbl_error_str.place(relx=0.52, rely=0.97, anchor="s")
        display.after(10000, lbl_error_str.destroy)
        inputs_list = [query]

'''press ESC to clear all entry boxes'''
def escape_pressed(event):
    for widget in display.winfo_children():
        if widget.winfo_class() == 'Entry' and widget.winfo_ismapped():
            widget.delete(0, tk.END)



window.bind("<Return>", enter_pressed)
window.bind("<Escape>", escape_pressed)
window.mainloop()
