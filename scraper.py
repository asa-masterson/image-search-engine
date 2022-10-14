from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import os
from pathlib import Path
from time import sleep

chromeOptions = Options()
chromeOptions.add_argument("--kiosk") # open chrome as fullscreen
chromeOptions.add_argument("--incognito") # open chrome in incognito
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chromeOptions)
#driver = webdriver.Chrome((os.fspath(Path(__file__).resolve().parent / "chromedriver")), chrome_options=chromeOptions)
driver.get("https://images.google.com") # loads google images
driver.find_element('xpath','//*[@id="L2AGLb"]/div').click() # presses accept all

search_bar = driver.find_element("name", "q") # finds the search bar
search_bar.clear()
search_bar.send_keys("asa masterson") # searches for there query
search_bar.send_keys(Keys.RETURN)
#driver.get_screenshot_as_file('./tmp.png') # takes a screenshot

images = []
x=0
y=1
while x < 5:
    count = 0
    driver.find_element('xpath','//*[@id="islrg"]/div[1]/div[{}]'.format(y)).click() # click on top 5 images
    while True:
        image = driver.find_element('xpath','//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img')
        img_src = image.get_attribute("src")
        if img_src[:10] == "data:image" and count<=10: # keeps checking image unless its been a seconf
            count += 1
            sleep(0.1)
        elif count>10: # move to the next image cos it took too long
            y += 1
            break
        else:
            x += 1
            y += 1
            images.append(img_src) # appends the image url to array
            break

print(images)
#sleep(5)

driver.close() # closes the browser