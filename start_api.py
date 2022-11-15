from http.server import BaseHTTPRequestHandler, HTTPServer
from re import T # to host the actual server
from urllib.parse import unquote_plus # to convert posted strings into universal format
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException # added for error handling
from time import sleep
import json
from bs4 import BeautifulSoup # because bing is awkward with all its iframes and overlays

no_img = "https://cdn.dribbble.com/users/760295/screenshots/4433975/media/03494b209a1511a61868ced337b97931.png?compress=1&resize=400x300"
# image to be shown when there are no more to be retrived
driver = None

def get_images_google(name, num):
    global driver
    if driver == None:
        chromeOptions = Options()
        #chromeOptions.add_argument("--kiosk") # open chrome as fullscreen
        chromeOptions.add_argument("--incognito") # open chrome in incognito
        # chromeOptions.add_argument("--headless") # open chrome in headless mode
        # driver = webdriver.Chrome('./chromedriver', chrome_options=chromeOptions)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chromeOptions)

        driver.get("https://images.google.com") # loads google images
        driver.find_element('xpath','//*[@id="L2AGLb"]/div').click() # presses accept all

        search_bar = driver.find_element("name", "q") # finds the search bar
        search_bar.clear()
        search_bar.send_keys(unquote_plus(name)) # searches for there query
        search_bar.send_keys(Keys.RETURN)
        #driver.get_screenshot_as_file('./tmp.png') # takes a screenshot

    images = []
    x=0
    y=1
    while len(images) < num:
        count = 0
        if y % 25 == 0:
            y += 1
        try:
            driver.find_element('xpath','//*[@id="islrg"]/div[1]/div[{}]'.format(y)).click() # click on top 5 images
            while True:

                image = driver.find_element('id','Sva75c')
                img_src = image.get_attribute("src")
                print(img_src)
                x += 1
                y += 1
                images.append(img_src) # appends the image url to array
                break
        except NoSuchElementException:
            images.append(no_img)
            x += 1

    images = json.dumps(images)
    print(images)
    #sleep(5)

    # driver.close() # closes the browser
    return images,count # converts to json for compatability

def get_images_bing(name, num): # ** UNDER CONSTRUCTION **
    chromeOptions = Options()
    #chromeOptions.add_argument("--kiosk") # open chrome as fullscreen
    chromeOptions.add_argument("--incognito") # open chrome in incognito
    #chromeOptions.add_argument("--headless") # open chrome in headless mode
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chromeOptions)

    driver.get("https://images.bing.com") # loads bing images

    search_bar = driver.find_element("name", "q") # finds the search bar
    search_bar.clear()
    search_bar.send_keys(unquote_plus(name)) # searches for there query
    search_bar.send_keys(Keys.RETURN)
    #driver.get_screenshot_as_file('./tmp.png') # takes a screenshot

    images = []
    before = False
    x=0
    y=1
    while x < num:
        count = 0
        if before == True:
            sleep(3)
            driver.back() # close current image
            print("okie")
        if y % 25 == 0:
            y += 1
        #try:
        sleep(1)
        driver.find_element('xpath','//*[@id="mmComponent_images_2"]/ul[1]/li[{}]/div/div[1]/a/div/img'.format(y)).click() # click on top 5 images
        before = True
        while True:
            driver.switch_to.frame('OverlayIFrame')
            image = driver.find_element('xpath','//*[@id="mainImageWindow"]/div[1]/div/div/div').get_attribute('innerHTML')
            soup = BeautifulSoup(image)
            print(soup.prettify())
            image = soup.find("img", class_="nofocus")
            img_src = image['src']
            if img_src[:10] == "data:image" and count<=10: # keeps checking image unless its been a second
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
        #except NoSuchElementException:
         #   images.append(no_img)
          #  x += 1

    images = json.dumps(images)
    print(images)
    #sleep(5)

    driver.close() # closes the browser
    return images # converts to json for compatability

def get_images_yahoo(name, num): # Only shows few top images - 10-15 - idk why
    chromeOptions = Options()
    #chromeOptions.add_argument("--kiosk") # open chrome as fullscreen
    chromeOptions.add_argument("--incognito") # open chrome in incognito
    chromeOptions.add_argument("--headless") # open chrome in headless mode
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chromeOptions)

    driver.get("https://images.yahoo.com") # loads yahoo images
    driver.find_element('xpath','//*[@id="consent-page"]/div/div/div/form/div[2]/div[2]/button').click() # presses accept all

    search_bar = driver.find_element("xpath", '//*[@id="yschsp"]') # finds the search bar, q didn't work - idk why
    search_bar.clear()
    search_bar.send_keys(unquote_plus(name)) # searches for there query
    search_bar.send_keys(Keys.RETURN)

    while True:
        try: # wait until the images have loaded
            image = driver.find_element('xpath','//*[@id="results"]/div[1]/ul/li[1]/a/img')
            break
        except NoSuchElementException:
            print("Im stuck") # i know, infinate loop - sorry
            sleep(0.1)
    sleep(5)
    #driver.get_screenshot_as_file('./tmp.png') # takes a screenshot

    images = []
    x=0
    y=1
    while x < num:
        try:
            image = driver.find_element('xpath','//*[@id="results"]/div[1]/ul/li[{}]/a/img'.format(y))
            img_src = image.get_attribute("src")
            x += 1
            y += 1
            count = 0
            images.append(img_src) # appends the image url to array
        except NoSuchElementException:
            print("Stuk")
            y += 1
            count += 1
            if count > 10:
                x += 1
                images.append(no_img)

    images = json.dumps(images)
    print(images)
    #sleep(5)

    driver.close() # closes the browser
    return images # converts to json for compatability


hostName = ""
PORT = 8080


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Access-Control-Allow-Origin","*")
        self.end_headers()
        path=self.path

        if path != "/favicon.ico":
            path = path[1:]
            pos = path.find("///")
            engine = path[:pos]
            path = path[pos+3:]
            pos = path.find("///")
            amount = int(path[:pos])
            if amount > 100 or amount < 1:
                self.wfile.write(bytes(str(json.dumps(["https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR-rv3poSHwWvwCAvkwR1ULT41M08oOHelrpQ&usqp=CAU"])), "utf-8"))
            else:
                query = path[pos+3:]
                if engine == "google":
                    images,count = get_images_google(query, amount)
                    self.wfile.write(bytes(str(images), "utf-8"))
                    
                elif engine == "bing":
                    pass
                    # Not Selenium Friendly >:(
                    #images = get_images_bing(query, amount)
                    #self.wfile.write(bytes(str(images), "utf-8"))
                elif engine == "yahoo":
                    images = get_images_yahoo(query, amount)
                    self.wfile.write(bytes(str(images), "utf-8"))
                else:
                    self.wfile.write(bytes(str(json.dumps(["https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR-rv3poSHwWvwCAvkwR1ULT41M08oOHelrpQ&usqp=CAU"])), "utf-8"))

 
if __name__ == "__main__":        
    webServer = HTTPServer((hostName, PORT), MyServer)
    print("Server started http://%s:%s" % (hostName, PORT))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")