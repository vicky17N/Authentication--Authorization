from tkinter import *
import tkinter.messagebox
import mysql.connector

db1 = mysql.connector.connect(host='localhost',user='root',password='',db='assessment')
db2 = mysql.connector.connect(host='localhost',user='root',password='',db='authentication')
cursor1 = db1.cursor()
cursor2 = db2.cursor()

def adminlogin():
    username = admin_username.get()
    password = admin_password.get()
    if username == 'vicky' and password == 'vicky@123':
        tkinter.messagebox.showinfo('Authenticate', 'Welcome Admin')
        adminhome()
    else:
        tkinter.messagebox.showinfo('Authenticate', 'Invalid')

def admin():
    global admin_frame
    global admin_username
    global admin_password
    admin_frame=Frame(homepage)
    admin_frame.pack()
    admin_username=StringVar()
    admin_password=StringVar()
    Label(admin_frame,text='Username',font=('Arisl',13)).pack()
    Entry(admin_frame,textvariable=admin_username,font=('arial',13)).pack()
    Label(admin_frame,text='password',font=('Arial',13)).pack()
    Entry(admin_frame,textvariable=admin_password,font=('Arial',13)).pack()
    Button(admin_frame,text='login',font=('Arial',13),bg='gray',fg='White',width='10',height='1',command=adminlogin).pack()

def adminhome():
    global adminpage
    adminpage=Toplevel(homepage)
    adminpage.geometry('1200x700')
    adminpage.title('Admin Home')
    adminpage.configure(bg='Aqua')
    addcategory=Button(adminpage,text='AddQuestion category',font=('Arial',15),bg='gray',fg='White',width='22',height='1',command=category_form)
    addcategory.place(x=200,y=50)
    addquestions = Button(adminpage, text='Add Question', font=('Arial', 15), bg='gray', fg='White', width='13', height='1',command=question_form)
    addquestions.place(x=600, y=50)

def category_form():
    global category_frame
    global category
    category = StringVar()
    category_frame=Frame(adminpage,height=180,width=500,bg='White').place(x=90,y=140)
    Label(adminpage,text='Enter category',font=('Arial',15),bg='Aqua').place(x=160,y=170)
    Entry(adminpage,textvariable=category,font=('Arial',15),bg='Aqua').place(x=340,y=170)
    Button(adminpage,text='ADD',height=1,width=15,bg='gray',fg='White',command=storecategory).place(x=340,y=220)

def storecategory():
    value = category.get()
    cursor1.execute('insert into storecatogry(name)values(%s)',[value])
    db1.commit()
    tkinter.messagebox.showinfo('Assessment','category Added')

def categories():
    cursor1.execute('select name from storecatogry')
    new = []
    a = cursor1.fetchall()
    for i in a:
        new.append(i[0])
    return new



def question_form():
    global Question_frame
    global question
    global op1
    global op2
    global op3
    global op4
    global answer
    global selected
    question=StringVar()
    op1=StringVar()
    op2=StringVar()
    op3=StringVar()
    op4=StringVar()
    answer=StringVar()
    selected=StringVar()
    Question_frame = Frame(adminpage,height=500,width=500,bg='White').place(x=600,y=140)
    a=categories()
    selected.set('--------selected--------')
    Label(adminpage,text='Select category',font=('Arial',15)).place(x=640,y=180)
    OptionMenu(adminpage,selected,*a).place(x=820,y=180)
    Label(adminpage, text='Question', font=('Arial', 15)).place(x=640, y=230)
    Entry(adminpage,textvariable=question,font=('Arial',15),bg='Aqua').place(x=820,y=230)
    Label(adminpage, text='option A', font=('Arial', 15)).place(x=640, y=280)
    Entry(adminpage, textvariable=op1, font=('Arial', 15), bg='Aqua').place(x=820, y=280)
    Label(adminpage,text='option B',font=('Arial',15)).place(x=640,y=330)
    Entry(adminpage,textvariable=op2,font=('Arial',15),bg='Aqua').place(x=820,y=330)
    Label(adminpage,text='option C',font=('Arial',15)).place(x=640,y=380)
    Entry(adminpage,textvariable=op3,font=('Arial',15),bg='Aqua').place(x=820,y=380)
    Label(adminpage,text='option D',font=('Arial',15)).place(x=640,y=430)
    Entry(adminpage,textvariable=op4,font=('Arial',15),bg='Aqua').place(x=820,y=430)
    Label(adminpage, text='Answer', font=('Arial', 15)).place(x=640, y=480)
    Entry(adminpage, textvariable=answer, font=('Arial', 15), bg='Aqua').place(x=820, y=480)
    Button(adminpage,text='ADD',font=('Arial',15),bg='gray',fg='White',width=15,height=1,command=storequestios).place(x=850,y=530)

def storequestios():
    quest = question.get()
    opA =op1.get()
    opB=op2.get()
    opC=op3.get()
    opD=op4.get()
    ans = answer.get()
    clicked=selected.get()
    cursor1.execute('insert into question(Qstn,opA,opB,opC,opD,ans,category)values(%s,%s,%s,%s,%s,%s,%s)',[quest,opA,opB,opC,opD,ans,clicked])
    db1.commit()
    tkinter.messagebox.showinfo('Assessment','Question Added')

def userlogin():
    username=user_username.get()
    password=user_password.get()
    cursor2.execute('select * from authentication where username=%s and password=%s',[username,password])
    a=cursor2.fetchone()
    if a!= None:
        tkinter.messagebox.showinfo('Quiz','Welcome user')
    else:
        tkinter.messagebox.showinfo('quiz','Invalid user')
    quiz()

class quiz():
    def __init__(self):
        global selectedvalue
        global home
        self.mark = 0
        selectedvalue = StringVar()
        home = Frame(homepage,height=700,width=1200,bg='aqua').place(x=0,y=0)
        a = categories()
        selectedvalue.set('Select Category')
        OptionMenu(home,selectedvalue,*a).place(x=150,y=50)
        Button(home,text='Start Test',font=('calibri',15),width='15',command=self.new,height='1',bg='gray',fg='White').place(x=800,y=50)

    def new(self):
        global data
        selected = selectedvalue.get()
        cursor1.execute('select * from question where category=%s',[selected])
        data = cursor1.fetchall()
        self.i = len(data)
        self.question()

    def question(self):
        a = data[self.i-1]
        ques = Text(home,font=('calibri',15),width=70,height=5,bg='White')
        ques.place(x=250,y=200)
        ques.insert(END,a[1])
        self.var=StringVar()
        self.ans = a[6]
        Radiobutton(home,text=a[2],font=('calibri',15),value=a[2],variable=self.var,bg='aqua',width=10).place(x=300,y=350)
        Radiobutton(home,text=a[3],font=('calibri',15),value=a[3],variable=self.var,bg='aqua',width=10).place(x=800,y=350)
        Radiobutton(home,text=a[4],font=('calibri',15),value=a[4],variable=self.var,bg='aqua',width=10).place(x=300,y=450)
        Radiobutton(home,text=a[5],font=('calibri',15),value=a[5],variable=self.var,bg='aqua',width=10).place(x=800,y=450)
        Button(home,text='Next',font=('calibri',15),width='15',command=lambda :self.next(a[6]),height='1',bg='gray',fg='White').place(x=850,y=500)

    def next(self,ans):
        var = self.var.get()
        if ans == var:
            self.mark = self.mark + 1
        if self.i >= 2:
            self.i = self.i-1
            self.question()
        else:
            self.end()

    def end(self):
        tkinter.messagebox.showinfo('Assessment',f'you have answered {self.mark} questions correctly')

def user():
    global user_frame
    global user_username
    global user_password
    user_frame=Frame(homepage)
    user_frame.pack()
    user_username=StringVar()
    user_password=StringVar()
    Label(user_frame,text='username',font=('Arial',13)).pack()
    Entry(user_frame,textvariable=user_username,font=('Arial',13)).pack()
    Label(user_frame,text='password',font=('Arial',13)).pack()
    Entry(user_frame,textvariable=user_password,font=('Arial',13)).pack()
    Button(user_frame,text='Login',font=('Arial',13),bg='gray',fg='white',width='10',height='1',command=userlogin).pack()
    Button(user_frame, text='Signup', font=('Arial', 13), bg='gray',fg='white', width='10', height='1',command=register).pack()

def register():
    global register_frame
    global register_name
    global register_mail
    global register_address
    global register_gender
    global register_username
    global register_password
    register_frame=Frame(homepage)
    register_frame.pack()
    register_name=StringVar()
    register_mail=StringVar()
    register_address=StringVar()
    register_gender=StringVar()
    register_username=StringVar()
    register_password=StringVar()
    Label(register_frame,text='Name',font=('Arial',13)).pack()
    Entry(register_frame,textvariable=register_name,font=('Arial',13)).pack()
    Label(register_frame,text='Mail',font=('Arial',13)).pack()
    Entry(register_frame,textvariable=register_mail,font=('Arial',13)).pack()
    Label(register_frame,text='Address',font=('Arial',13)).pack()
    Entry(register_frame,textvariable=register_address,font=('Arial',13)).pack()
    Label(register_frame,text='gender',font=('Arial',13)).pack()
    Entry(register_frame,textvariable=register_gender,font=('Arial',13)).pack()
    Radiobutton(register_frame,text='Male',variable=register_gender,value='Male',font=('Arial',13)).pack()
    Radiobutton(register_frame, text='Female', variable=register_gender, value='Female', font=('Arial', 13)).pack()
    Label(register_frame, text='Username', font=('Arial', 13)).pack()
    Entry(register_frame, textvariable=register_username, font=('Arial', 13)).pack()
    Label(register_frame, text='Password', font=('Arial', 13)).pack()
    Entry(register_frame, textvariable=register_password, font=('Arial', 13)).pack()
    Button(register_frame,text='Submit',command=storedata,font=('Arial',13),bg='gray',fg='white',width='10',height='1').pack()

def storedata():
    name=register_name.get()
    mail=register_mail.get()
    address=register_address.get()
    gender=register_gender.get()
    username=register_username.get()
    password=register_password.get()
    cursor2.execute('insert into authentication(name,email,gender,address,username,password)values(%s,%s,%s,%s,%s,%s)',[name,mail,address,gender,username,password])
    db2.commit()
    notify.config(text='Registered Successfully')

def mainpage():
    global homepage
    global notify
    homepage=Tk()
    homepage.geometry('1200x700')
    homepage.configure(bg='lightblue')
    homepage.title('Authenticate')
    but1=Button(homepage,text='Admin',command=admin,font=('Arial',15,'bold'),bg='gray',fg='white',width='10',height='1')
    but1.pack()
    but2=Button(homepage, text='User', command=user, font=('Arial', 15, 'bold'), bg='gray', fg='white', width='10',height='1')
    but2.pack()
    notify=Label(homepage,font=('calibri',12),fg='green')
    notify.pack()
    homepage.mainloop()

mainpage()