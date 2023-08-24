from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from selenium.common import NoSuchElementException, ElementNotInteractableException

from bs4 import BeautifulSoup as bs
import os
import requests
import time

search_query = "orchids"
save_directory = os.path.join("./", search_query.replace(" ", "_"))
os.makedirs(save_directory, exist_ok=True)

# Perform a search on DuckDuckGo images
url = f"https://duckduckgo.com/?q={search_query}&t=h_&iar=images&iax=images&ia=images"
#url = 'https://www.nasa.gov/'
driver = webdriver.Edge()
driver.get(url)


# Set the maximum time (in seconds) to wait for the search results to appear

#results_container_xpath = "//div[@id='links_wrapper']"
#WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, results_container_xpath)))    #visibility_of_all_elements_located((By.XPATH, results_container_xpath))) #presence_of_all_elements_located((By.XPATH, results_container_xpath)))

time.sleep(2)


length = 0


while True: 
    html = driver.page_source
    soup = bs(html, 'html.parser')
    i = 0
    id = 0
    elements = soup.find_all('img', 'tile--img__img js-lazyload') 
    for item in elements[length:]:
        try: 
            src= item["src"]
            alt= item["alt"]
        except:
            src = r"//th.bing.com/th/id/R.f9729bedc77984d0037d7a1e3c31f213?rik=7BYCyuf2IMuBsA&riu=http%3a%2f%2fcliparts.co%2fcliparts%2fLcd%2fdjE%2fLcddjEBxi.png&ehk=5WvCOtqXXV9MVj1lSxqqJSfU4dYEAVuyUaIRFvVRoBw%3d&risl=&pid=ImgRaw&r=0"
            alt= "defect"
            pass
        # Construct an XPath based on attributes
        xpath = f"//img[@src='{src}' and @alt='{alt}']"
        # Download the image
        img = requests.get("https:" + src)

        if img.status_code == 200:
            open(save_directory + f"/{id}-" + time.strftime("%Y%m%d-%H%M%S") + ".jpg", 'wb').write(img.content)
            print(f"Downloaded: {i}")
            i+=1
            id +=1
            if i == 10:
                height = 1080 + id * 100
                driver.execute_script(f"window.scrollTo(0, {height})")
                i = 0
    length = len(elements)
            # element = driver.find_element(By.XPATH, xpath)    
            
            # driver.execute_script("arguments[0].scrollIntoView();", element)
            # time.sleep(2)


