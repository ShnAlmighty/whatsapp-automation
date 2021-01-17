import sqlite3
import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
from tkinter import messagebox
import sys

conn = sqlite3.connect('pendingMsgs')

driver = webdriver.Chrome(r"PATH_TO_CHROME_DRIVER.EXE")
driver.get("https://web.whatsapp.com")

def confirm():
    global ans
    messagebox.showinfo('showinfo','Scan the OR code in web whatsapp')
    ans = messagebox.askquestion("askquestion","QR code scanning completed?")

def main():
    # Times = []
    global driver
    cursor = conn.execute("SELECT Name,Time,Body FROM log")
    while(cursor):
        cursor = conn.execute("SELECT Name,Time,Body FROM log")
        for row in cursor:
            contact = row[0]
            text = row[2]
            sentTime = row[1]
            currentTimeTemp = datetime.datetime.now().strftime("%Y-%m-%d %X")
            currentTime =  datetime.datetime.strptime(currentTimeTemp,"%Y-%m-%d %X")
            tempDate = datetime.datetime.strptime(sentTime,"%Y-%m-%d %X")
            # Times.append(tempDate)
            if(tempDate < currentTime):
                alarm = datetime.datetime.now().strftime("%Y-%m-%d %X")
                inp_xpath_search = "//*[@id='side']/div[1]/div/label/div/div[2]"
                input_box_search = WebDriverWait(driver,50).until(lambda driver: driver.find_element_by_xpath(inp_xpath_search))
                remove_value = input_box_search.text
                if(remove_value):
                    count = len(remove_value)
                    for i in range(count):
                        input_box_search.send_keys(Keys.BACKSPACE)
                input_box_search.click() 
                input_box_search.send_keys(contact)
                time.sleep(1)                           
                selected_contact = WebDriverWait(driver,50).until(lambda driver:driver.find_element_by_xpath("//span[@title='"+contact+"']")) #(r"/html/body/div[1]/div/div/div[3]/div/div[2]/div[1]/div/div/div[1]")
                time.sleep(1)
                selected_contact.click() 
                #oldText = WebDriverWait(driver,50).until(lambda driver:driver.find_element_by_xpath("""//*[@id="main"]/div[3]/div/div/div[3]"""))
                #messagebox.showinfo('showinfo',oldText.text)
                time.sleep(1)
                inp_xpath = '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]'
                input_box = WebDriverWait(driver,50).until(lambda driver:driver.find_element_by_xpath(inp_xpath))
                time.sleep(1)
                input_box.send_keys(text + Keys.ENTER)
                # messagebox.showinfo('showinfo','Message sent to {} at {}'.format(contact,alarm))
                conn.execute("""DELETE FROM log WHERE (Time = '%s' and Name = '%s' and Body = '%s')"""%(sentTime,contact,text))
                conn.commit()
                # readText = driver.find_element_by_xpath("""//*[@id="main"]/div[3]/div/div/div[3]""")
                # else:
                #     conn.execute("""DELETE FROM log WHERE (Time = '%s' and Name = '%s' and Body = '%s')"""%(sentTime,contact,text))
                #     conn.commit()
                #     messagebox.showerror('showerror','Invalid Name!!')


if __name__ == "__main__":
    main()
