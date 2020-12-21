from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import pyautogui
import json

secretData = json.load(open('credentials.json', 'r'))

emailID = secretData['emailID']
password = secretData['password']

botOptions = Options()
botOptions.add_argument('--use-fake-ui-for-media-stream')
botOptions.add_argument('--disable-infobars')
botOptions.add_argument('--disable-notifications')

sub_conf = input('Is it english class (y/n) ')

if(sub_conf == 'y'):
    url = 'https://accounts.google.com/signin/v2/identifier?ltmpl=meet&continue=https%3A%2F%2Fmeet.google.com%2Ficf-xcxx-qjr%3Fhs%3D196&flowName=GlifWebSignIn&flowEntry=ServiceLogin'
else:
    url = 'https://classroom.google.com/u/1/c/MTE1MzE3MzgyMTY0'


class meet_bot:
    def __init__(self):
        self.bot = webdriver.Chrome(options=botOptions)

    def login(self, email, passw):
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
        if(sub_conf == 'n'):
            time.sleep(2)
            meetLink = bot.find_element_by_xpath(
                '//*[@id="yDmH0d"]/div[2]/div/div[1]/div/div[2]/div[2]/div/span/a')
            meetLink.click()
        time.sleep(5)
        print('key pressed')
        pyautogui.hotkey('tab')
        pyautogui.hotkey('ctrl', 'd')
        pyautogui.hotkey('ctrl', 'e')
        bot.implicitly_wait(20)
        if(sub_conf == 'y'):
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


obj = meet_bot()
obj.login(emailID, password)
