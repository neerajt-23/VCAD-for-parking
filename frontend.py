from tkinter import*
from tkinter import messagebox

root= Tk()
root.title("Login form")
root.geometry('1349x625') 
root.configure(bg='#333333')

def login():
    username = "vcad"
    password = "123"
    if username_entry.get()==username and password_entry.get()==password:
        messagebox.showinfo(title="Login Success", message="You successfully logged in.")
        w2=Toplevel()
    else:
       messagebox.showerror(title="Error", message="Invalid login.")
    w2=Toplevel()

    w2.title("second window")
    w2.geometry('1349x625')
    w2.configure(bg='#333333')
    lbl=Label(w2,text="Select Operation to perform: ", bg='#333333', fg="#FF3399", font=("Arial", 30))
    lbl.grid(row=0, column=0, sticky="news", pady=40)
    #lbl.place(anchor=CENTER)
    
    #e=Entry(w2,font=("Arial",20))
    #e.grid(row=1, column=1, pady=20)
    #e.place(relx=0.5,rely=0.4,anchor=CENTER)
    def counter():
        #p=e.get()
        from vehicle_count_org import K
    
    #def detection():
     #   from new1 import y

    btn=Button(w2,text="Click For Counter",bg="#FF3399", fg="#FFFFFF",font=("Arial",20),command=counter)
    btn.grid(row=1, column=2,  pady=30)

    #btn1=Button(w2,text="Click for detection",bg="#FF3399", fg="#FFFFFF",font=("Arial",20),command=detection)
    #btn1.grid(row=2, column=2, pady=30)
   
frame = Frame(bg='#333333')

# Creating widgets
login_label = Label(
    frame, text="Login", bg='#333333', fg="#FF3399", font=("Arial", 30))
username_label = Label(
    frame, text="Username", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
username_entry = Entry(frame, font=("Arial", 16))
password_entry = Entry(frame, show="*", font=("Arial", 16))
password_label = Label(
    frame, text="Password", bg='#333333', fg="#FFFFFF", font=("Arial", 16))
login_button = Button(
    frame, text="Login", bg="#FF3399", fg="#FFFFFF", font=("Arial", 16), command=login)

# Placing widgets on the screen
login_label.grid(row=0, column=0, columnspan=2, sticky="news", pady=40)
username_label.grid(row=1, column=0)
username_entry.grid(row=1, column=1, pady=20)
password_label.grid(row=2, column=0)
password_entry.grid(row=2, column=1, pady=20)
login_button.grid(row=3, column=0, columnspan=2, pady=30)

frame.pack()
root.mainloop()
