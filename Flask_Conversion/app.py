#app.py
from flask import Flask, render_template,request
from urllib.parse import unquote_plus 
from selenium import webdriver
from time import sleep
import json
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

app = Flask(__name__, template_folder='template', static_folder='style')

@app.route('/', methods=['GET','POST'])
def basic():
    global pos,before,driver
    if request.method == 'POST':
        engine = request.form['engine']
        filter = request.form['filter']
        num = int(request.form['amount'])
        name = request.form['search']
        space = 0
        if name.upper() == before.upper() and driver:
            x=pos[0]
            y=pos[1]
            im = pos[2]
        else:
            
            x=1
            y=1 
            im = 3
            pos = (x,y,im)
            before = name
            driver.close()
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chromeOptions)
            driver.get("https://images.google.com") # loads google images
            driver.find_element('xpath','//*[@id="L2AGLb"]/div').click() # presses accept all
            
                
            search_bar = driver.find_element("name", "q") # finds the search bar
            search_bar.clear()
            search_bar.send_keys(unquote_plus(name)) 
            search_bar.send_keys(Keys.RETURN)
        images = []
        if filter == "tb":
            driver.find_element('xpath','//*[@id="yDmH0d"]/div[2]/c-wiz/div[1]/div/div[1]/div[2]/div[2]/div').click()
            driver.find_element('xpath','//*[@id="yDmH0d"]/div[2]/c-wiz/div[2]/div[2]/c-wiz[1]/div/div/div[1]/div/div[2]/div').click()
            driver.find_element('xpath','//*[@id="yDmH0d"]/div[2]/c-wiz/div[2]/div[2]/c-wiz[1]/div/div/div[3]/div/a[3]/div').click()
            space = 0.4
        
        while len(images) < num:
            count = 0
            if y % 25 == 0:
                y += 1
            try:
                driver.find_element('xpath','//*[@id="islrg"]/div[1]/div[{}]'.format(y)).click() # click on top 5 images
                while True:
                    sleep(space)
                    image = driver.find_element('xpath','//*[@id="Sva75c"]/div[{}]/div/div/div[3]/div[2]/c-wiz/div[2]/div[1]/div[1]/div[2]/div/a/img'.format(im))
                    img_src = image.get_attribute("src")
                    if filter == "tb":
                        print(img_src[-4:])
                        if img_src[-4:] != ".png":
                            num +=1
                    x += 1
                    im+=1
                    y += 1
                    if img_src != "" or img_src !=None:
                        images.append(img_src) # appends the image url to array
                    break
            except NoSuchElementException:
                num+=1
                x += 1
                sleep(0.3)
        pos = (x,y,im)
        before = name
        images = json.dumps(images)

        # driver.close( ) # closes the browser
        return images # converts to json for compatability
    return render_template('viewer.html')

if __name__=='__main__':
    chromeOptions = Options()
    chromeOptions.add_argument("--incognito") # open chrome in incognito
    chromeOptions.add_argument("--headless") # open chrome in headless mode
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chromeOptions)
   

    pos = (1,1,3)
    before = ""
    app.run(debug = True)