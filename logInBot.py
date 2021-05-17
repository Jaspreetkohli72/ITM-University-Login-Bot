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
import sys

winFlag = 0
if(os.name == 'nt'):
    print("Windows")
    filename = 'configWin.json'
    winFlag = 1
elif(os.name == 'posix'):
    print("linux")
    filename = 'configLin.json'


def writeToJSONFile(path, filename, data):
    filePathNameWExt = './'+path+'/'+filename
    with open(filePathNameWExt, 'w')as fp:
        json.dump(data, fp)


configRead = json.load(
    open(filename, 'r+'))


iLoad = configRead['initialRun']
if(iLoad):
    userData = input("Enter the path to userdata folder\n")
    if(userData == "" or userData == " "):
        exit('no data entered')
    else:
        if(os.path.isdir(userData)):
            print('User Data Directory Saved')
        else:
            exit('Directory not found')
    exPath = input("Enter the path to chromedriver\n")
    if(exPath == "" or exPath == " "):
        exit('no data entered')
    else:
        if(os.path.exists(exPath)):
            print('Chromedriver path Saved')
        else:
            exit('File not found not found')
    data = {}
    data['initialRun'] = False
    data['uData'] = userData
    data['chromedriverPath'] = exPath
    writeToJSONFile('./', filename, data)
else:
    print("False")
    userData = configRead['uData']
    if(os.path.exists(userData)):
        print('userdata Found')
    else:
        exit('Userdata not found not found')
    exPath = configRead['chromedriverPath']
    if(os.path.exists(exPath)):
        print('Chromedriver Found')
    else:
        exit('File not found not found')


botOptions = Options()
botOptions.add_argument('--use-fake-ui-for-media-stream')
botOptions.add_argument('--disable-infobars')
botOptions.add_argument('--disable-notifications')
botOptions.add_argument('user-data-dir='+userData)


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
            print(per, 'th Period')
        elif(time >= '01:45 PM' and time <= '02:30 PM'):
            per = 0
            print('BREAK')
        elif(time >= '02:30 PM' and time <= '03:30 PM'):
            per = 5
            print(per, 'th Period')
        elif(time >= '03:30 PM' and time <= '04:30 PM'):
            per = 6
            print(per, 'th Period')
        elif(time > '04:30 PM'):
            print('class time is over')
            t.sleep(10)
            sys.exit(0)
        return per

    def brkFn(self, per):
        if(per == 0):
            brkTime = True
        else:
            brkTime = False
        return brkTime

    def subFn(self, day, per):
        if(day == 'Wednessday'):
            if(per == 1 or per == 2):
                sub_conf = 'e'
            elif(per == 3):
                sub_conf = 'j'
            else:
                sub_conf = 'n'
        elif(day == 'Friday' or day == 'Saturday'):
            if(per == 3 or per == 4):
                sub_conf = 'e'
            elif(day == 'Saturday' and per == 1):
                sub_conf = 'j'
            else:
                sub_conf = 'n'
        elif(day == 'Monday'):
            if(per == 5 or per == 6):
                sub_conf = 'jl'
            else:
                sub_conf = 'n'
        elif(day == 'Thursday'):
            if(per == 1):
                sub_conf = 'j'
            else:
                sub_conf = 'n'
        else:
            sub_conf = 'n'
        return sub_conf


class subjCls:
    def urlDeclare(self, sub):
        meet = 'http://meet.google.com/'
        if(sub == 'e'):
            classCode = 'poh aeys nnu'
            url = meet+classCode.replace(' ', '-')
        elif(sub == 'jl'):
            classCode = 'shd wswc avf'
            url = meet+classCode.replace(" ", "-")
        elif(sub == 'j'):
            classCode = 'iak fqqv cfc'
            url = meet+classCode.replace(" ", "-")
        else:
            url = 'https://classroom.google.com/u/1/c/MTE1MzE3MzgyMTY0'
        return url


class meet_bot:
    def __init__(self):
        self.bot = webdriver.Chrome(
            executable_path=exPath, options=botOptions)

    def login(self, url, sub):
        bot = self.bot

        bot.get(url)
        bot.implicitly_wait(20)
        if(sub == 'n'):
            meetLink = bot.find_element_by_xpath(
                '//*[@id="yDmH0d"]/div[4]/div/div/div[1]/div/div[2]/div[2]/div/span/a/div')
            meetLink.click()
        t.sleep(5)
        print('key pressed')
        pyautogui.hotkey('tab')
        #pyautogui.hotkey('ctrl', 'd')
        pyautogui.hotkey('ctrl', 'e')
        bot.implicitly_wait(20)
        if(sub == 'e'):
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
    print("it's BREAK time")
    t.sleep(10)
    sys.exit(0)
else:
    subject = ttObj.subFn(day, period)
    print(subject)
subObj = subjCls()
url = subObj.urlDeclare(subject)
print(url)
obj = meet_bot()
obj.login(url, subject)
