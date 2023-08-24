from selenium import webdriver
from bs4 import BeautifulSoup as bs
import os
import requests
import time

# Stating the search query and creating the associated directory.
search_query = "orchids"
save_directory = os.path.join("./", search_query.replace(" ", "_"))
os.makedirs(save_directory, exist_ok=True)

# Performing a search on DuckDuckGo images.
url = f"https://duckduckgo.com/?q={search_query}&t=h_&iar=images&iax=images&ia=images"
driver = webdriver.Edge()
driver.get(url)

# Waiting for the page to load.
time.sleep(2)

# Initializing variables.
length = 0
max_empty_loop = 30
loop_count = 0

# Scraping loop.
while loop_count< max_empty_loop: 

    # Loading the html laoded piece of page into a soup.
    html = driver.page_source
    soup = bs(html, 'html.parser')

    # Making a list of all corresponding elements in the soup.
    elements = soup.find_all('img', 'tile--img__img js-lazyload') 

    # Going through the list.
    for item in elements[length:]:
        try: 
            src= item["src"]
            alt= item["alt"]
        except:
            pass

        # Downloading each image.
        img = requests.get("https:" + src)
        if img.status_code == 200:
            img_name = f"/{src[-16:-11]}-" + time.strftime("%Y%m%d-%H%M%S") + ".jpg"
            open(save_directory + img_name, 'wb').write(img.content)
            print(f"Downloaded: {img_name}")
    
    # Scrolling down the page to load more content.  
    driver.execute_script(f"window.scrollTo(0, {1080 *(len(elements)//20)})")  

    # Setting the length of elements found in this round to start from than rank the next round.
    length = len(elements)

    # Incrementing the loop count.
    loop_count += 1
 
