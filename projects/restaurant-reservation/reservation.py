from tkinter import *
from tkinter import messagebox

win = Tk()
win.geometry('360x600')

import sqlite3
from sqlite3 import IntegrityError, OperationalError

con = sqlite3.connect('my_contacts.db')
cur = con.cursor()
database = 'my_contacts.db'

cur.execute('create table if not exists contacts(name text , family text, customer_code text, reservation_code text primary key, phone text)')
con.commit()

def existence(reservation_code):
    if cur.execute(f'select * from contacts where reservation_code = {reservation_code}').fetchone():
        return True
    else:
        return False

def add_onclick():
    name = en_name.get()
    family = en_family.get()
    reservation_code = en_reservationcode.get()
    customer_code = en_customercode.get()
    phone = en_phone.get()

    if not(reservation_code):
        messagebox.showerror('error', 'reservation code cant be empty')
    elif not (phone.isdigit() or not reservation_code.isdigit()):
        messagebox.showerror('error', 'reservation code and phone must be DIGITS')
    elif existence(reservation_code):
        messagebox.showerror('error', 'reservation code cant be repetitive')
    else:
        cur.execute(f'insert into contacts(name, family, customer_code, reservation_code, phone) values("{name}", "{family}", "{customer_code}", "{reservation_code}", "{phone}")')
        con.commit()
        messagebox.showinfo('success', 'reservation inserted successfully')
def delete_onclick():
    reservation_code = en_reservationcode.get()
    if not (existence(reservation_code)):
        messagebox.showerror('error', 'There is no such a reservation code')
    else:
        cur.execute(f'delete from contacts where reservation_code = "{reservation_code}"')
        con.commit()
        messagebox.showinfo('Success', 'Reservation deleted successfully')

def search_onclick():
    reservation_code = en_reservationcode.get()
    if not(existence(reservation_code)):
        messagebox.showerror('error', 'There is no such a reservation code!')
    else:
        result = cur.execute(f'select * fro contacts where reservation_code = "{reservation_code}"').fetchone()
        name, family, customer_code, reservation_code, phone = result
        vname.set(name)
        vfamily.set(family)
        vcustomer.set(customer_code)
        vreservation.set(reservation_code)
        vphone.set(phone)
        en_reservationcode.config(state='disabled')
        en_customercode.config(state='disabled')

def show_onclick():
    result = cur.execute('select * from contacts').fetchall()
    text = ''
    for i in result:
        name, family, customer_code, reservation_code, phone = i
        text += f'name: {name}\nfamily:{family}\ncustomer code: {customer_code}\nreservation code: {reservation_code}\nphone: {phone}\n-----------\n'
    messagebox.showinfo('all_contacts', text)


def update_onclick():
    name = en_name.get()
    family = en_family.get()
    code = en_reservationcode.get()
    customer = en_customercode.get()
    phone = en_phone.get()


    if not (phone.isdigit()):
        messagebox.showerror('error', 'Phone must be digits')
    else:
        cur.execute(f'update contacts set name = "{name}", family = "{family}", customer_code = "{customer}", phone = "{phone}" where reservation_code = {code}')
        con.commit()
        if messagebox.showinfo('success', 'Reservation Updated successfully'):
            en_reservationcode.config(state='disabled')
            en_customercode.config(state='disabled')
            clear_onclick()


def clear_onclick():
    for i in entries:
        i.delete(0, END)

def apply_onclick():
    theme = vartheme.get()
    if theme == 'dark':
        bg_color = 'black'
        fg_color = 'white'
        entry_bg = '#333333'
    else:
        bg_color = 'white'
        fg_color = 'black'
        entry_bg = 'white'

    win.config(bg=bg_color)
    for i in labels:
        i.config(bg=bg_color, fg = fg_color)
    for j in entries:
        j.config(bg=entry_bg, fg=fg_color)
    for k in buttons:
        k.config(bg=bg_color, fg = fg_color)



lbl_title = Label(win, text='Reservation', font=('Bahnschrift', 20))

lbl_name = Label(win, text='Name:', font=('Bahnschrift', 10))
lbl_family = Label(win, text='Family:', font=('Bahnschrift', 10))
lbl_customercode = Label(win, text='Customer code:', font=('Bahnschrift', 10))
lbl_reservationcode =Label(win, text='Reservation code:', font=('Bahnschrift', 10))
lbl_phone = Label(win, text='Phone:', font=('Bahnschrift', 10))

labels = [lbl_name, lbl_family, lbl_customercode, lbl_reservationcode, lbl_phone, lbl_title]

vname = StringVar()
vfamily = StringVar()
vcustomer = StringVar()
vreservation = StringVar()
vphone = StringVar()

en_name = Entry(win, textvariable=vname)
en_family = Entry(win, textvariable=vfamily)
en_customercode = Entry(win, textvariable=vcustomer)
en_reservationcode = Entry(win, textvariable=vreservation)
en_phone = Entry(win, textvariable=vphone)

entries = [en_name,en_family, en_customercode, en_reservationcode, en_phone]

btn_add = Button(win, text='Add', command=add_onclick)
btn_delete = Button(win, text='Delete', command=delete_onclick)
btn_update = Button(win, text='Update', command=update_onclick)
btn_search = Button(win, text='Search', command=search_onclick)
btn_showall = Button(win, text='Show All', command=show_onclick)
btn_clear = Button(win, text='Clear', command=clear_onclick)

buttons = [btn_add, btn_delete, btn_update, btn_search, btn_showall, btn_clear]
#-------------grid--------------------

lbl_title.grid(row=0, columnspan=2, column=0, pady=20)

lbl_name.grid(row=1, column=0, pady=10)
lbl_family.grid(row=2, column=0, pady=10)
lbl_customercode.grid(row=3, column=0, pady=10)
lbl_reservationcode.grid(row=4, column=0, pady=10)
lbl_phone.grid(row=5, column=0, pady=10)

en_name.grid(row=1, column=1, pady=10)
en_family.grid(row=2, column=1, pady=10)
en_customercode.grid(row=3, column=1, pady=10)
en_reservationcode.grid(row=4, column=1, pady=10)
en_phone.grid(row=5, column=1, pady=10)

btn_add.grid(row=6, column=0, ipadx=45, padx=25, pady=10)
btn_delete.grid(row=6, column=1, ipadx=40, padx=25, pady=10)
btn_search.grid(row=7, column=0, ipadx=40, padx=25, pady=10)
btn_update.grid(row=7, column=1, ipadx=39, padx=25, pady=10)
btn_showall.grid(row=8, column=0, ipadx=35, padx=25, pady=10)
btn_clear.grid(row=8, column=1, ipadx=45, padx=25, pady=10)

vartheme = StringVar(value='light')
dark = Radiobutton(win, text='Dark mode', variable=vartheme, value='dark', command=apply_onclick)
light = Radiobutton(win, text='Light mode', variable=vartheme, value='light', command=apply_onclick)


dark.grid(row=9, column=0, pady=25)
light.grid(row=9, column=1, pady=25)




win.mainloop()