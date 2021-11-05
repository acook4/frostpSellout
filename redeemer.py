#I could only get this to run in 3.6, not 3.8
import pywinauto,time
from pywinauto.application import Application

from pywinauto import mouse
from pywinauto import keyboard

import pandas as pd

#this program will use desktop automation to open chrome, open Frost's stream, then guess numbers from results.csv

doin_numbers = pd.read_csv('results.csv',delimiter=',')

app=Application().start(cmd_line=u'C:\Program Files\Google\Chrome\Application\chrome.exe --force-renderer-accessibility')
time.sleep(3)
window=app.Chrome_WidgetWin_1

#any coordinates were for my monitor only. they'll likely be different on your monitor
pywinauto.mouse.click(coords=(300,50))
time.sleep(1)

#enter site address
keyboard.send_keys("https://twitch.tv/frostprime_")
time.sleep(1)

#go to site and wait
pywinauto.mouse.click(coords=(300,100))
time.sleep(15)

for index, row, in doin_numbers.iterrows():

    current_num = str(row['NUMBER'])

    if (row['SHOULDGUESS'] == 'should_guess'):

        pywinauto.mouse.click(coords=(1650,1020))
        time.sleep(1)

        #theoretical best location to redeem first reward regardless of gamba or not
        pywinauto.mouse.click(coords=(1650,805))
        time.sleep(1)

        #type number
        keyboard.send_keys(current_num)
        time.sleep(0.5)
        print('about to submit ' + current_num)

        #redeem
        pywinauto.mouse.click(coords=(1900,1020))
        time.sleep(1.5)
    else:
        print('skipped over' + current_num)