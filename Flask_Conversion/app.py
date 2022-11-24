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
    if request.method == 'POST':
        engine = request.form['engine']
        num = int(request.form['amount'])
        name = request.form['search']
        print(engine)
        print(num)
        print(name)
        
        chromeOptions = Options()
        chromeOptions.add_argument("--incognito") # open chrome in incognito
        chromeOptions.add_argument("--headless") # open chrome in headless mode
        
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chromeOptions)

        driver.get("https://images.google.com") # loads google images
        driver.find_element('xpath','//*[@id="L2AGLb"]/div').click() # presses accept all

        search_bar = driver.find_element("name", "q") # finds the search bar
        search_bar.clear()
        search_bar.send_keys(unquote_plus(name)) 
        search_bar.send_keys(Keys.RETURN)
        images = []
        x=0
        y=1
        im = 3
        while len(images) < num:
            count = 0
            if y % 25 == 0:
                y += 1
            try:
                driver.find_element('xpath','//*[@id="islrg"]/div[1]/div[{}]'.format(y)).click() # click on top 5 images
                while True:

                    image = driver.find_element('xpath','//*[@id="Sva75c"]/div[{}]/div/div/div[3]/div[2]/c-wiz/div[2]/div[1]/div[1]/div[2]/div/a/img'.format(im))
                    img_src = image.get_attribute("src")
                    x += 1
                    im+=1
                    y += 1
                    if img_src != "" or img_src !=None:
                        images.append(img_src) # appends the image url to array
                    break
            except NoSuchElementException:
                # images.append(no_img)
                num+=1
                x += 1
        print(images)
        images = json.dumps(images)

        driver.close() # closes the browser
        return images # converts to json for compatability
    return render_template('viewer.html')

if __name__=='__main__':
    app.run(debug = True)