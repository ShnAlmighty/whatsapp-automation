from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
import json
import os
import datetime
from datetime import date
from tkinter import Tk,Button,Label,Entry,Text,Frame,messagebox,ttk
from PIL import ImageTk, Image
import sqlite3 
import subprocess
import psutil
import signal
import sys

def connect():
    global conn
    conn = sqlite3.connect("pendingMsgs")
    conn.execute("""CREATE TABLE if not exists log
    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Body TEXT NOT NULL,
    Time TEXT NOT NULL)""")

# def clearLog():
#     cursor = conn.execute("SELECT Name,Time,Body FROM log")
#     while(cursor):
#         cursor = conn.execute("SELECT Name,Time,Body FROM log")
#         for row in cursor:
#             contact = row[0]
#             text = row[2]
#             currentTimeTemp = datetime.datetime.now().strftime("%H:%M:%S")
#             currentTime =  datetime.datetime.strptime(currentTimeTemp,"%H:%M:%S")
#             tempDate = datetime.datetime.strptime(row[1],"%H:%M:%S")
#             if(tempDate < currentTime):
#                 alarm = datetime.datetime.now().strftime("%H:%M:%S")
#                 inp_xpath_search = "//*[@id='side']/div[1]/div/label/div/div[2]"
#                 input_box_search = WebDriverWait(driver,50).until(lambda driver: driver.find_element_by_xpath(inp_xpath_search))
#                 input_box_search.click()
#                 time.sleep(1)
#                 input_box_search.send_keys(contact)
#                 time.sleep(1)
#                 selected_contact = driver.find_element_by_xpath("//span[@title='"+contact+"']")
#                 time.sleep(1)
#                 selected_contact.click() 
#                 oldText = WebDriverWait(driver,50).until(lambda driver:driver.find_element_by_xpath("""//*[@id="main"]/div[3]/div/div/div[3]"""))
#                 time.sleep(1)
#                 inp_xpath = '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]'
#                 input_box = WebDriverWait(driver,50).until(lambda driver:driver.find_element_by_xpath(inp_xpath))
#                 time.sleep(1)
#                 input_box.send_keys(text + Keys.ENTER)
#                 messagebox.showinfo('showinfo','Message sent to {} at {}'.format(contact,alarm))
#                 conn.execute("DELETE FROM log WHERE NAME = {}".format(contact))
#                 conn.commit()

def send():
    global ans,conn,recievers
    if(recievers):
        size = len(recievers)
    else:
        size=0
    ans = "yes"
    if(ans == "yes"):
        global inp1,inp2,timeE,frame1,driver
        if(size==0):
            contact =  str(inp1.get()) 
        else:
            contact=list(recievers)
            recievers = []
        text = str(inp2.get("1.0","end-1c"))
        if(timeE != None):
            alarm =  str(timeE.get())  
            if(alarm!="" or timeE == None):
                if(size>1):
                    for i in range(size):
                        conn.execute("""
                        INSERT INTO log (Name,Body,Time) VALUES ('%s','%s','%s')
                        """%(contact[i],text,alarm))
                        conn.commit()      
                else:
                    conn.execute("""
                    INSERT INTO log (Name,Body,Time) VALUES ('%s','%s','%s')
                    """%(contact,text,alarm))
                    conn.commit()
                    messagebox.showinfo('showinfo','Message is stored and will be sent')
                    # clearLog()
                    # os.startfile("runLog.py")
                    # setTime = datetime.datetime.now().strftime("%H:%M:%S")
                    # while(setTime != alarm):
                    #     setTime = datetime.datetime.now().strftime("%H:%M:%S")
        else: 
            timeE1 = datetime.datetime.now().strftime("%H:%M:%S")
            if(size>1):
                for i in range(size):
                    conn.execute("""
                    INSERT INTO log (Name,Body,Time) VALUES ('%s','%s','%s')
                    """%(contact[i],text,timeE1))
                    conn.commit()     
            else:
                conn.execute("""
                INSERT INTO log (Name,Body,Time) VALUES ('%s','%s','%s')
                """%(contact,text,timeE1))
                conn.commit()
                messagebox.showinfo('showinfo','Message is stored and will be sent')
            # conn.execute("""
            #     INSERT INTO log (Name,Body,Time) VALUES ('%s','%s','%s')
            #     """%(contact,text,timeE1))
            # conn.commit()
            messagebox.showinfo('showinfo','Message is stored and will be sent')
            # os.startfile("runLog.py")
            # alarm=datetime.datetime.now().strftime("%H %M %S")
            # inp_xpath_search = "//*[@id='side']/div[1]/div/label/div/div[2]"
            # input_box_search = WebDriverWait(driver,50).until(lambda driver: driver.find_element_by_xpath(inp_xpath_search))
            # input_box_search.click()
            # time.sleep(1)
            # input_box_search.send_keys(contact)
            # time.sleep(1)
            # selected_contact = driver.find_element_by_xpath("//span[@title='"+contact+"']")
            # time.sleep(1)
            # selected_contact.click() 
            # oldText = WebDriverWait(driver,50).until(lambda driver:driver.find_element_by_xpath("""//*[@id="main"]/div[3]/div/div/div[3]"""))
            # #messagebox.showinfo('showinfo',oldText.text)
            # time.sleep(1)
            # inp_xpath = '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]'
            # input_box = WebDriverWait(driver,50).until(lambda driver:driver.find_element_by_xpath(inp_xpath))
            # time.sleep(1)
            # input_box.send_keys(text + Keys.ENTER)
            # messagebox.showinfo('showinfo','Message sent to {} at {}'.format(contact,alarm))
            # readText = driver.find_element_by_xpath("""//*[@id="main"]/div[3]/div/div/div[3]""")


def showTimer():
    global hl,timeE,TimerButton
    TimerButton.grid_remove()
    hl = Label(frame1,text='Time at which you want to send (hh:mm:ss)')
    hl.grid(row=6,column=0,pady=(10,0),ipadx='40')
    timeE = Entry(frame1,textvariable="")
    timeE.grid(row=7,column=0,ipadx='60',ipady='3')

def closeF():
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

def Display():
    global frame1
    frame1.grid_remove()
    cursor = conn.execute("""SELECT * FROM log""")
    displayFrame = Frame(menu)
    displayFrame.grid()
    i,a=0,0
    panel = []
    for data in cursor:
        panel.append(Label(displayFrame,text=data)) 
        panel[a].grid(row=i,column=0)
        a=a+1
        i=i+1
    exit = Button(displayFrame,text='Back',command=lambda: back(frame1,displayFrame))
    exit.grid(row=(i+1),column=0,pady=10,ipadx='40')
            

def main():
    connect()
    
    global logBook,frame1
    logBook = subprocess.Popen(["runLog.py"],shell=True)

    global menu,ans,inp1,inp2,timeE,TimerButton,frame1,plural
    menu = Tk()
    frame1 = Frame(menu)
    frame1.grid()
    timeE=None

    img = Image.open("whatsapp.png")
    img = img.resize((100,100),Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)

    logo = Label(frame1,image=img)
    logo.grid(row=0,column=0)

    l1 = Label(frame1,text='Name of person')
    l1.grid(row=1,column=0,sticky='nesw',pady=(10,0))
    inp1 = Entry(frame1)
    inp1.grid(row=2,column=0,ipadx='60',ipady='3',pady='10',padx='20')
    plural = Button(frame1,text="  Add  ",command = lambda: add())
    plural.grid(row=3,column=0,pady=10,ipadx='40')

    l2 = Label(frame1,text='Type your message')
    l2.grid(row=4,column=0)
    inp2 = Text(frame1,height=15,width=30)
    inp2.grid(row=5,column=0)

    TimerButton = Button(frame1,text='Add Timer',command = lambda: showTimer())
    TimerButton.grid(row=6,column=0,pady=10,ipadx='40')

    seeLog = Button(frame1,text='  Log  ',command=lambda:Display())
    seeLog.grid(row=8,column=0,pady=10,ipadx='40')

    close = Button(frame1,text='Close',command=lambda:closeF())
    close.grid(row=9,column=0,pady=10,ipadx='40')

    sub1 = Button(frame1,text=' Submit ',command=lambda:send())
    sub1.grid(row=10,column=0,pady=10,ipadx='40')

    menu.mainloop()

if __name__ == "__main__":
    main()