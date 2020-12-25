from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time as t
import os
import pyautogui
import json
from datetime import date
from datetime import datetime
import csv
import pandas
import numpy
import sys

secretData = json.load(
    open('credentials.json', 'r'))

# example = json.load(open('Time Table.json', 'r'))
# print(example['Day/Time'])


emailID = secretData['emailID']
password = secretData['password']

botOptions = Options()
botOptions.add_argument('--use-fake-ui-for-media-stream')
botOptions.add_argument('--disable-infobars')
botOptions.add_argument('--disable-notifications')


class dateTimeCls:
    def dayFn(self):
        dayToday = date.today().weekday()
        if(dayToday == 0):
            day = "Monday"
        elif(dayToday == 1):
            day = "Tuesday"
        elif(dayToday == 2):
            day = "Wednessday"
        elif(dayToday == 3):
            day = "Thursday"
        elif(dayToday == 4):
            day = "Friday"
        elif(dayToday == 5):
            day = "Saturday"
        elif(dayToday == 6):
            day = "Sunday"
        return day

    def timeFn(self):
        now = datetime.now()
        current_time = now.strftime("%I:%M %p")
        return current_time


class timeTableCls:
    def __init__(self):
        self.per = 0

    def periodSel(self, time):
        per = self.per
        if(time >= '09:30 AM' and time <= '10:30 AM'):
            per = 1
            print(per, 'st Period')
        elif(time >= '10:30 AM' and time <= '11:30 AM'):
            per = 2
            print(per, 'nd Period')
        elif(time >= '11:30 AM' and time <= '11:45 AM'):
            per = 0
            print('BREAK')
        elif(time >= '11:45 AM' and time <= '12:45 PM'):
            per = 3
            print(per, 'rd Period')
        elif(time >= '12:45 PM' and time <= '01:45 PM'):
            per = 4
            print(per+'th Period')
        elif(time >= '01:45 PM' and time <= '02:30 PM'):
            per = 0
            print('BREAK')
        elif(time >= '02:30 PM' and time <= '03:30 PM'):
            per = 4
            print(per, 'th Period')
        elif(time >= '03:30 PM' and time <= '04:30 PM'):
            per = 6
            print(per, 'th Period')
        elif(time > '04:30 PM'):
            sys.exit('Class time is over')
        return per

    def brkFn(self, per):
        if(per == 0):
            brkTime = True
        else:
            brkTime = False
        return brkTime

    def subFn(self, day, per):
        if(day == 'Monday' or day == 'Wednessday'):
            if(per == 3 or per == 4):
                sub_conf = 'y'
            else:
                sub_conf = 'n'
        elif(day == 'Tuesday'):
            if(per == 2 or per == 4):
                sub_conf = 'y'
            else:
                sub_conf = 'n'
        else:
            sub_conf = 'n'
        return sub_conf


class subjCls:
    def urlDeclare(self, sub):
        if(sub == 'y'):
            url = 'https://accounts.google.com/signin/v2/identifier?ltmpl=meet&continue=https%3A%2F%2Fmeet.google.com%2Ficf-xcxx-qjr%3Fhs%3D196&flowName=GlifWebSignIn&flowEntry=ServiceLogin'
        else:
            url = 'https://classroom.google.com/u/1/c/MTE1MzE3MzgyMTY0'
        return url


class meet_bot:
    def __init__(self):
        self.bot = webdriver.Chrome(options=botOptions)

    def login(self, email, passw, url, sub):
        bot = self.bot

        bot.get(url)
        bot.implicitly_wait(20)

        emailIdInput = bot.find_element_by_xpath('//*[@id="identifierId"]')
        emailIdInput.send_keys(email)

        nextBtn = bot.find_element_by_xpath(
            '//*[@id="identifierNext"]/div/button')
        nextBtn.click()

        bot.implicitly_wait(20)

        passwordInput = bot.find_element_by_xpath(
            "//*[@id='password']/div[1]/div/div[1]/input")
        passwordInput.send_keys(passw)

        finishBtn = bot.find_element_by_xpath(
            '//*[@id="passwordNext"]/div/button')
        finishBtn.click()
        if(sub == 'n'):
            t.sleep(2)
            meetLink = bot.find_element_by_xpath(
                '//*[@id="yDmH0d"]/div[2]/div/div[1]/div/div[2]/div[2]/div/span/a')
            meetLink.click()
        t.sleep(5)
        print('key pressed')
        pyautogui.hotkey('tab')
        pyautogui.hotkey('ctrl', 'd')
        pyautogui.hotkey('ctrl', 'e')
        bot.implicitly_wait(20)
        if(sub == 'y'):
            joinBtn = bot.find_element_by_css_selector(
                '#yDmH0d > c-wiz > div > div > div:nth-child(8) > div.crqnQb > div > div > div.vgJExf > div > div.KieQAe > div.d7iDfe.NONs6c > div > div.Sla0Yd > div > div.XCoPyb > div.uArJ5e.UQuaGc.Y5sE8d.uyXBBb.xKiqt > span')
            joinBtn.click()
        else:
            try:
                joinBtn = bot.find_element_by_css_selector(
                    '#yDmH0d > c-wiz > div > div > div:nth-child(8) > div.crqnQb > div > div > div.vgJExf > div > div.KieQAe > div.d7iDfe.NONs6c > div > div.Sla0Yd > div > div.XCoPyb > div.uArJ5e.UQuaGc.Y5sE8d.uyXBBb.xKiqt > span')
                joinBtn.click()
            except:
                print("Loading took too much time")


dtObj = dateTimeCls()
day = dtObj.dayFn()
time = dtObj.timeFn()
ttObj = timeTableCls()
period = ttObj.periodSel(time)
brk = ttObj.brkFn(period)
if(brk):
    sys.exit("it's BREAK time")
else:
    subject = ttObj.subFn(day, period)
    print(subject)
subObj = subjCls()
url = subObj.urlDeclare(subject)
obj = meet_bot()
obj.login(emailID, password, url, subject)
