from glob import glob
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, StringVar, Radiobutton
from tkinter import ttk
import tkinter as tk
from tkinter.messagebox import showinfo
import pyodbc
from datetime import datetime

# database connection
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=LAPTOP-7NSQJHHP;'
                      'Database=hotel;'
                      'Trusted_Connection=yes;')
                      
cursor = conn.cursor()

window = Tk()
def checkin():
    now = datetime.now()
    checkindate = now.strftime("%Y-%m-%d")

    roomnumber = room_entry.get()
    cnic = cnic_entry.get()
    checkinStatus = 'x'
    result = cursor.execute("select top 1 * from booking where custcnic =(?) order by bookingid desc", (cnic))
    for i in result:
        checkinStatus = i[3]
        print(checkinStatus)

    if  checkinStatus == None:
        cursor.execute("update booking set checkin = (?) where roomid = (?) and custcnic = (?)",
        (checkindate,roomnumber,cnic))
        conn.commit()
        showinfo(title='Result',message="Checked In Successfully!")
    else:
        showinfo(title='Result',message="You have Not Registered or Have Already Check in!")

def checkout():
    now = datetime.now()
    checkoutdate = now.strftime("%Y-%m-%d")

    roomnumber = room_entry.get()
    cnic = cnic_entry.get()

    checkoutStatus = None
    result = cursor.execute("select top 1 * from booking where custcnic =(?) order by bookingid desc", (cnic))
    for i in result:
        checkoutStatus = i[4]
        print(checkoutStatus)

    if checkoutStatus == None:
        cursor.execute("update room set roomstatus= (?) where roomid =(?)",("free", roomnumber))
        conn.commit()
        cursor.execute("update booking set checkout = (?) where roomid = (?) and custcnic = (?)",
        (checkoutdate,roomnumber,cnic))
        conn.commit()
        showinfo(title='Result',message="Checked Out Successfully!")
    else:
        showinfo(title='Result',message="You have Already Check Out!")
    

def create_customer():
    name = custName.get()
    cnic =custCNIC.get()
    address = custAddress.get()
    gender = custGender.get()
    number= custNo.get()
    cursor.execute('Insert into customer values (?,?,?,?,?)', cnic, name, address, gender, number)
    conn.commit()
    #insertion in db left
    home_page()

def book_room():
    now = datetime.now()
    checkindate = now.strftime("%Y-%m-%d")

    room_number = selected_room.get().split(" ")[0]
    print(room_number)
    payment_type = paymenttype.get()
    print(payment_type)
    
    cnic = custcnic.get()
    print(cnic)
    # insertion in db left
    cursor.execute("update room set roomstatus= (?) where roomid =(?)",("taken", room_number))
    conn.commit()
    cursor.execute("insert into booking (roomid, custcnic, checkin, paymenttype) values (?,?,?,?)",
    (room_number, cnic, checkindate, payment_type))
    conn.commit()

    home_page()

def room_page():
    global window
    global selected_type
    global cursor
    global selected_room
    global paymenttype
    global custcnic
    rooms = []
    window.destroy()
    window = Tk()

    window.geometry("1189x673")
    window.configure(bg = "#FFFFFF")
    canvas = Canvas(window,bg = "#FFFFFF",height = 673,width = 1189,bd = 0,highlightthickness = 0,relief = "ridge")

    canvas.place(x = 0, y = 0)
    bg_room_img = PhotoImage(file="./room/bg.png")
    roomimg = canvas.create_image(594,336,image=bg_room_img)
    selected_type = tk.StringVar()
    month_cb = ttk.Combobox(window, textvariable=selected_type, font=("Arial", 20))
    month_cb['values'] = ('single', 'double', 'twin', 'studio')

    # prevent typing a value
    month_cb['state'] = 'readonly'
    month_cb.place(x=380, y=130)
    room_status= "free"
    def month_changed(event):
        result = cursor.execute("Select * from room where roomtype=(?) and roomstatus=(?)",(selected_type.get(), room_status))
        rooms = []
        for i in result:
            rooms.append(f"{i[0]} {i[3]}")
        
        rooms_cb.set('')
        rooms_cb['values'] = (tuple(rooms))

    month_cb.bind('<<ComboboxSelected>>', month_changed)

    
    selected_room = tk.StringVar()
    rooms_cb = ttk.Combobox(window, textvariable=selected_room, font=("Arial", 20))
    rooms_cb['values'] = (tuple(rooms))

    # prevent typing a value
    rooms_cb['state'] = 'readonly'
    rooms_cb.place(x=470, y=222)



    paymenttype = Entry(bd=0,bg="#DDEED0",highlightthickness=0,font=("Inter Bold", 32))
    paymenttype.place(x=390,y=312,width=249,height=54)


    custcnic = Entry(bd=0,bg="#DDEED0",highlightthickness=0,font=("Inter Bold", 32))
    custcnic.place(x=198,y=395,width=249,height=54)

    canvas.create_text(396,21,anchor="nw",text="Book A Room",fill="#FFFFFF",font=("Inter Bold", 48))
    canvas.create_text(42,121,anchor="nw",text="Room Type:",fill="#FFFFFF",font=("Inter Bold", 40))
    canvas.create_text(33,210,anchor="nw",text="Available Rooms:",fill="#FFFFFF",font=("Inter Bold", 40))
    canvas.create_text(42,396,anchor="nw",text="CNIC:",fill="#FFFFFF",font=("Inter Bold", 40))
    canvas.create_text(33,307,anchor="nw",text="Payment Type:",fill="#FFFFFF",font=("Inter Bold", 40))

    button_image_1 = PhotoImage(file=("./room/button_1.png"))
    button_1 = Button(image=button_image_1,borderwidth=0,highlightthickness=0,command=book_room,relief="flat")
    button_1.place(x=465,y=571,width=275,height=75)
    window.mainloop()

def customer_page():
    global window
    global custName, custCNIC, custAddress, custGender, custNo
    window.destroy()
    window = Tk()

    window.geometry("1189x673")
    window.configure(bg = "#FFFFFF")

    canvas = Canvas( window, bg = "#3FA7B5",height = 673, width = 1189,bd = 0,highlightthickness = 0,relief = "ridge")
    canvas.place(x = 0, y = 0)
    image_image_1 = PhotoImage(file=("./customer/bg.png"))
    image_1 = canvas.create_image(594,336,image=image_image_1)


    custName = Entry(bd=0,bg="#BBC9C9",highlightthickness=0,font=("Inter Bold", 32))
    custName.place(x=482,y=121,width=249,height=54)

    custCNIC = Entry(bd=0,bg="#BBC9C9",highlightthickness=0,font=("Inter Bold", 32))
    custCNIC.place(x=482,y=207,width=249,height=54)


    custAddress = Entry(bd=0,bg="#BBC9C9",highlightthickness=0,font=("Inter Bold", 32))
    custAddress.place(x=482,y=293,width=249,height=54)


    custGender = Entry(bd=0,bg="#BBC9C9",highlightthickness=0,font=("Inter Bold", 32))
    custGender.place(x=482,y=379,width=249,height=54)


    custNo = Entry(bd=0,bg="#BBC9C9",highlightthickness=0,font=("Inter Bold", 32))
    custNo.place(x=482,y=480,width=249,height=54)

    canvas.create_text(396,21,anchor="nw",text="Create Customer",fill="#FFFFFF",font=("Inter Bold", 48))
    canvas.create_text(317,126,anchor="nw",text="Name:",fill="#FFFFFF",font=("Inter Bold", 40))
    canvas.create_text(323,212,anchor="nw",text="CNIC:",fill="#FFFFFF",font=("Inter Bold", 40))
    canvas.create_text(266,293,anchor="nw",text="Address:",fill="#FFFFFF",font=("Inter Bold", 40))
    canvas.create_text(282,381,anchor="nw",text="Gender:",fill="#FFFFFF",font=("Inter Bold", 40))
    canvas.create_text(235,478,anchor="nw",text="Phone No:",fill="#FFFFFF",font=("Inter Bold", 40))

    button_image_1 = PhotoImage(file=("./customer/button_1.png"))
    button_1 = Button(image=button_image_1,borderwidth=0,highlightthickness=0,command=create_customer,relief="flat")
    button_1.place(x=465,y=571,width=275,height=75)
    window.mainloop()

def home_page():
    global window
    global room_entry   #we use the global keyword if you want to change a global variable inside a function
    global cnic_entry
    window.destroy()
    window = Tk()

    window.geometry("1189x673")
    canvas = Canvas(window,bg = "#1449F1",height = 673,width = 1189,bd = 0,highlightthickness = 0,relief = "ridge")

    canvas.place(x = 0, y = 0)
    img1 = PhotoImage(file="./home_page/image_1.png")
    canvas.create_image(594,336,image=img1)


    room_entry = Entry(bd=0,bg="#FFFFFF",highlightthickness=0,font=("Inter Bold", 32))
    room_entry.place(x=350,y=135,width=249,height=54)


    cnic_entry = Entry(bd=0,bg="#FFFFFF",highlightthickness=0,font=("Inter Bold", 32))
    cnic_entry.place(x=350,y=215,width=249,height=54)

    canvas.create_text(82,36,anchor="nw",text="Booking",fill="#FFFFFF",font=("Bold", 48))
    canvas.create_text(82,131,anchor="nw",text="Room NO:",fill="#FFFFFF",font=("Bold", 40))
    canvas.create_text(82,216,anchor="nw",text="Cust CNIC:",fill="#FFFFFF",font=("Bold", 40))

    checkinBtn = Button(text= "Check In",borderwidth=0,highlightthickness=0,relief="flat",font=("Inter Bold", 32), fg="white", bg= "#5072A7")
    checkinBtn.place(x=200,y=323,width=224,height=65)

    checkoutBtn = Button(text= "Check Out",borderwidth=0,highlightthickness=0,relief="flat",font=("Inter Bold", 32), fg="white", bg= "#5072A7")
    checkoutBtn.place(x=500,y=323,width=224,height=65)


    button_2 = Button(text="Book a Room",borderwidth=0,highlightthickness=0,command=room_page,relief="flat",font=("Inter Bold", 32), fg="white", bg= "#5072A7")
    button_2.place(x=492,y=539,width=272,height=73)

    custbtn = Button(text="Create Cust",borderwidth=0,highlightthickness=0,command=customer_page,relief="flat",font=("Inter Bold", 32), fg="white", bg= "#5072A7")
    custbtn.place(x=129,y=538,width=277,height=73)
    window.mainloop()
    
def login():
    staffun = staffusername.get()
    staffpw = staffpassword.get()
    
    result = cursor.execute("Select username, password from staff")
    for i in result:
        if(staffun==i[0] and staffpw == i[1]):
            home_page()     #if a staff member matches meaning we will login
            return
        else:
            showinfo(title='Login Error',message="No Staff Exist with these Credentials!")


window.geometry("1189x673")

canvas = Canvas(window,bg = "#FFFFFF",height = 673,width = 1189,bd = 0,highlightthickness = 0,relief = "ridge")

canvas.place(x = 0, y = 0)

login_img = PhotoImage(file="./login_page/image_1.png")
image_1 = canvas.create_image(594,336,image=login_img)


staffusername = Entry(bd=0,bg="#FFFFFF", font=("Arial", 32))
staffusername.place(x=110,y=200,width=350,height=55)

staffpassword = Entry(bd=0,bg="#FFFFFF", font=("Arial", 32))
staffpassword.place(x=110,y=370,width=350,height=55)


canvas.create_text(100,45, anchor="nw", text="Enter your Credentials", fill="#FFFFFF", font=("Bold", 48))
canvas.create_text(100,136, anchor="nw", text="UserName:", fill="#FFFFFF", font=("Bold", 40))
canvas.create_text(100,312, anchor="nw", text="Password:", fill="#FFFFFF", font=("Bold", 40))

button_1 = Button(text= "Login!", borderwidth=0,command=login, font=("Bold", 40), bg= "#6CB4EE", fg="white")
button_1.place(x=192, y=489, width=224,height=65)

window.mainloop()