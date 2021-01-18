import time
import json
import os
import datetime
import sqlite3 
import subprocess
import psutil
import signal
import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from datetime import date
from tkinter import Tk,Button,Label,Entry,Text,Frame,messagebox,ttk,END
from PIL import ImageTk, Image

def connect():
    global conn
    conn = sqlite3.connect("pendingMsgs")
    conn.execute("""CREATE TABLE if not exists log
    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Body TEXT NOT NULL,
    Time TEXT NOT NULL)""")

def send():
    global ans,conn,recievers,inp1,inp2,timeE,frame1,remiderE,hl,sl,reminderButton,TimerButton,FIXED,fixedButton
    
    if(recievers):
        size = len(recievers)
    else:
        size=0

    if(size==0):
        contact =  inp1.get()
    else:
        contact=list(recievers)
        recievers = []

    text = str(inp2.get("1.0","end-1c"))
    nameCheck,textCheck=1,1
    if(timeE!=None):
        if(timeE.get()=="" or timeE.get()=="Time at which you want to send(hh:mm:ss)"):
            timeE = None
    if(remiderE!=None):
        if(remiderE.get()=="" or remiderE=="Date at which you want to send(YYYY:MM:DD)"):
            remiderE=None
    if(text=="Type your message" or text==""):
        messagebox.showerror('showerror','Kindly write your message first')
        textCheck=0
    if(contact=="Name of person" or contact==""):
        messagebox.showerror('showerror','Kindly provide the name or names')
        nameCheck=0
    if(timeE != None and textCheck==1 and nameCheck==1):
        alarm =  str(timeE.get())  
        if(alarm!=""):
            if(remiderE != None):
                dateTemp = remiderE.get()
                remiderE.grid_remove()
                reminderButton.grid()
                remiderE=None
            else:
                dateTemp = datetime.datetime.now().strftime("%Y-%m-%d")
            tempDate = alarm.split(" ")
            if(len(tempDate)==2):
                pass
            else:
                alarm = dateTemp +" "+ tempDate[0]
            if(size>1):
                for i in range(size):
                    conn.execute("""
                    INSERT INTO log (Name,Body,Time,fixed) VALUES ('%s','%s','%s','%d')
                    """%(contact[i],text,alarm,FIXED))
                    conn.commit()      
            else:
                conn.execute("""
                INSERT INTO log (Name,Body,Time,fixed) VALUES ('%s','%s','%s','%d')
                """%(contact,text,alarm,FIXED))
                conn.commit()
                messagebox.showinfo('showinfo','Message is stored and will be sent')
                # setTime = datetime.datetime.now().strftime("%H:%M:%S")
                # while(setTime != alarm):
                #     setTime = datetime.datetime.now().strftime("%H:%M:%S")
        timeE.grid_remove()
        TimerButton.grid()
        timeE = None
        FIXED=0
        fixedButton.config(text="Send Daily")
    elif(timeE==None and textCheck==1 and nameCheck==1 ): 
        timeE1 = datetime.datetime.now().strftime("%Y-%m-%d %X")
        if(size>1):
            for i in range(size):
                conn.execute("""
                INSERT INTO log (Name,Body,Time,fixed) VALUES ('%s','%s','%s','%d')
                """%(contact[i],text,timeE1,FIXED))
                conn.commit()     
        else:
            conn.execute("""
            INSERT INTO log (Name,Body,Time,fixed) VALUES ('%s','%s','%s','%d')
            """%(contact,text,timeE1,FIXED))
            conn.commit()
        FIXED=0
        fixedButton.config(text="Send Daily")

def contentClean(a):
    if a==1:
        global inp1
        if(inp1.get() == "Name of person"): 
            inp1.delete(0,'end')
    elif a==2:
        global inp2
        if(inp2.get("1.0","end-1c") == "Type your message"): 
            inp2.delete('1.0','end')
    elif a==3:
        global timeE
        if(timeE.get() == "Time at which you want to send(hh:mm:ss)"): 
            timeE.delete(0,'end')
    elif a==4:
        global remiderE
        if(remiderE.get() == "Date at which you want to send(YYYY:MM:DD)"): 
           remiderE.delete(0,'end')

def contentFill(a):
    if a==1:
        global inp1
        if(inp1.get() == ""): 
            inp1.insert(0,'Name of person')
    elif a==2:
        global inp2
        if(inp2.get("1.0","end-1c") == ""): 
            inp2.insert('1.0','Type your message')
    elif a==3:
        global timeE
        if(timeE.get() == ""): 
            timeE.insert(0,'Time at which you want to send(hh:mm:ss)')
    elif a==4:
        global remiderE
        if(remiderE.get() == ""): 
           remiderE.insert(0,'Date at which you want to send(YYYY-MM-DD)')
        
def showTimer():
    global timeE,TimerButton
    TimerButton.grid_remove()
    timeE = Entry(frame1,textvariable="")
    timeE.insert(0,'Time at which you want to send(hh:mm:ss)')
    timeE.bind("<FocusOut>",lambda args: contentFill(3))
    timeE.grid(row=4,column=0,ipadx='60',ipady='3',pady=(10,5))
    timeE.bind("<FocusIn>",lambda args: contentClean(3))

def showReminder():
    global reminderButton,remiderE
    reminderButton.grid_remove()
    remiderE = Entry(frame1,textvariable="")
    remiderE.insert(0,'Date at which you want to send(YYYY:MM:DD)')
    remiderE.bind("<FocusOut>",lambda args: contentFill(4))
    remiderE.bind("<FocusIn>",lambda args: contentClean(4))
    remiderE.grid(row=5,column=0,ipadx='60',ipady='3',pady=(5,10))

def closeF():
    global menu
    menu.destroy()
    # driver.close()
    global logBook
    logBook.terminate()
    parent = psutil.Process(logBook.pid)
    children = parent.children(recursive=True)
    child_pid = children[0].pid
    subprocess.check_output("Taskkill /PID %d /F"%child_pid)

def add():
    global inp1
    global recievers
    recievers.append(inp1.get())
    inp1.delete(0,'end')

global recievers
recievers = []

def back(a,b):
    b.grid_remove()
    a.grid()

def clearLog(a,f):
    y = messagebox.askyesno('askyesno','Do you want to delete this messages?')
    if(y==True):
        global conn
        conn.execute("DELETE FROM log WHERE rowid = %d"%(a))
        conn.commit()
        conn.execute("REINDEX log")
        conn.commit()
        messagebox.showinfo('showinfo','Message Deleted')
        f.grid_remove()
        Display()

def Display():
    global frame1
    frame1.grid_remove()
    cursor = conn.execute("""SELECT * FROM log""")
    displayFrame = Frame(menu)
    displayFrame.grid()
    i,a=0,0
    panel = []
    delete = []
    for data in cursor:
        panel.append(Label(displayFrame,text=data)) 
        panel[a].grid(row=i,column=0)
        delete.append(Button(displayFrame,text='Delete',command=lambda a=data[0]: clearLog(a,displayFrame)))
        delete[a].grid(row=i,column=1,pady=10,ipadx='40',padx=(5,5))
        a=a+1
        i=i+1
    exit = Button(displayFrame,text='Back',command=lambda: back(frame1,displayFrame))
    exit.grid(row=(i+1),column=0,pady=10,ipadx='40',padx=(5,5))

def fixedmsg():
    global FIXED,fixedButton
    if(FIXED==0):
        y= messagebox.askyesno('askyesno','Do you want to fix this message?')
        if(y==True):
            FIXED = 1
            fixedButton.config(text="Fixed")
            messagebox.showinfo('showinfo','Message is fixed. This message will be sent everyday at the given time. Go to log if you want to remove this message.')
    elif(FIXED==1):
        y= messagebox.askyesno('askyesno','Do you want to remove this message from being send daily?')
        if(y==True):
            FIXED = 0
            fixedButton.config(text="Send Daily")
            messagebox.showinfo('showinfo','Message is removed and will not be send daily.')


def main():
    connect()
    
    global frame1,FIXED,fixedButton
    FIXED=0
    logBook = subprocess.Popen(["runLog.py"],shell=True)

    global menu,inp1,inp2,timeE,TimerButton,frame1,plural,reminderButton,remiderE
    menu = Tk()
    frame1 = Frame(menu)
    frame1.grid()
    timeE=None
    remiderE=None

    img = Image.open("whatsapp.png")
    img = img.resize((100,100),Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)

    logo = Label(frame1,image=img)
    logo.grid(row=0,column=0)

    inp1 = Entry(frame1)
    inp1.insert(0,'Name of person')
    inp1.bind("<FocusIn>",lambda args: contentClean(1))
    inp1.bind("<FocusOut>",lambda args: contentFill(1))
    inp1.grid(row=1,column=0,ipadx='60',ipady='3',pady='10',padx='20')
    plural = Button(frame1,text="  Add  ",command = lambda: add())
    plural.grid(row=2,column=0,pady=10,ipadx='40')

    inp2 = Text(frame1,height=15,width=30)
    inp2.insert('1.0','Type your message')
    inp2.bind("<FocusIn>",lambda args: contentClean(2))
    inp2.bind("<FocusOut>",lambda args: contentFill(2))
    inp2.grid(row=3,column=0)

    TimerButton = Button(frame1,text='Add Timer',command = lambda: showTimer())
    TimerButton.grid(row=4,column=0,pady=(10,10),ipadx=60,sticky='nesw',padx=65)

    reminderButton = Button(frame1,text='Add Reminder',command = lambda: showReminder())
    reminderButton.grid(row=5,column=0,pady=10,ipadx=60,sticky='nesw',padx=65)

    fixedButton = Button(frame1,text='Send Daily',command = lambda: fixedmsg())
    fixedButton.grid(row=6,column=0,pady=10,ipadx=60,sticky='nesw',padx=65)

    seeLog = Button(frame1,text='Log',command=lambda:Display())
    seeLog.grid(row=7,column=0,pady=10,ipadx=60,sticky='nesw',padx=65)

    close = Button(frame1,text='Close',command=lambda:closeF())
    close.grid(row=8,column=0,pady=10,ipadx=60,sticky='nesw',padx=65)

    sub1 = Button(frame1,text=' Submit ',command=lambda:send())
    sub1.grid(row=9,column=0,pady=(10,10),ipadx=60,sticky='nesw',padx=65)

    menu.mainloop()

if __name__ == "__main__":
    main()
