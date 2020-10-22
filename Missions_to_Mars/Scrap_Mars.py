#!/usr/bin/env python
# coding: utf-8

# ## NASA Mars News

# In[70]:


# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
import time

executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[13]:
def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

# URL of NASA Mars News Site to be scraped
    url = 'https://mars.nasa.gov/news/'


    # In[14]:


    # Retrieve page with the requests module
    browser.visit(url)


    # In[16]:


    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


    # In[17]:


    html = browser.html


    # In[19]:


    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')


    # In[20]:


    # Examine the results, then determine element that contains sought info
    print(soup.prettify())


    # In[23]:


    element = soup.select_one("ul.item_list li.slide")
    title = element.find("div", class_="content_title").get_text()
    title


    # In[24]:


    paragraph = element.find("div", class_='article_teaser_body').get_text()
    paragraph


    # In[21]:


    # # Extract title text
    # news_title = soup.find('div', class_='content_title').text
    # news_p = soup.find('div', class_='article_teaser_body')
    # print(news_title)
    # print(news_p)


    # ## JPL Mars Space Images - Featured Image

    # In[26]:


    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)


    # In[27]:


    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)


    # ### featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA16225_hires.jpg'

    # In[36]:


    element = browser.find_by_id("full_image")
    element.click()


    # In[37]:


    browser.is_element_present_by_css("more info", wait_time=1)
    findElement = browser.find_link_by_partial_text("more info")
    findElement.click()


    # In[38]:


    html = browser.html
    imagesoup = BeautifulSoup(html, 'html.parser')


    # In[39]:


    image = imagesoup.select_one("figure.lede a img")
    imagesource = image.get("src")


    # In[41]:


    featured_image_url = 'https://www.jpl.nasa.gov' + imagesource
    featured_image_url


    # ## Mars Facts

    # In[64]:


    url = 'https://space-facts.com/mars/'


    # In[65]:


    tables = pd.read_html(url)
    tables


    # In[66]:


    fact_df = tables[0]
    fact_df.columns = ["Description", "value"]
    mars_table = fact_df.set_index("Description", inplace=True)


    # In[67]:


    fact_df.to_html(classes = "table table-striped")


    # In[68]:


    #print(fact_df)


    # ## Mars Hemispheres

    # In[83]:


    # hemurl = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    # browser.visit(url)


    # # In[84]:


    # html = browser.html
    # hemsoup = BeautifulSoup(html, "html.parser")
    # item = hemsoup.find("div", class_="item")
    # item


    # # In[85]:


    # # hem = []
    # # for image in item:
    # #     imageurl = item.find_all("a")["href"]
    # #     title = item.find("div", class_="description").find("a").find("h3").text
    # #     image_url = "https://astrogeology.usgs.gov" + imageurl
    # #     browser.visit(image_url)
    # #     html = browser.html
    # #     imagesoup = BeautifulSoup(html, "html.parser")
    # #     finalimage = imagesoup.find("div", class_="downloads").find("ul").find("li").find("a")["href"]
    # #     hem.append({"title": title, "img_url": finalimage})
    # # hem


    # # In[91]:


    hemurl = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response = requests.get(hemurl)
    hemsoup = BeautifulSoup(response.text, "html.parser")
    item = hemsoup.find_all(class_="itemLink product-item")
    item


    # In[92]:


    hem = []
    for image in item:

        image_url = "https://astrogeology.usgs.gov" + image.get("href")
        hem.append(image_url)
    hem


    # In[ ]:


    hemurl = []
    for url in hem:
        response = requests.get(url)
        imgsoup = BeautifulSoup(response.text, "html.parser")
        #time.sleep(2)
        imageurl = imgsoup.find("a", href=True, text="Sample")
        href = imageurl["href"]
        title = imgsoup.find(class_="title").text.strip().replace(' Enhanced', '')

        hemurl.append({"title": title, "img_url": href})
    hemurl


    # In[ ]:
    data = {
        "news_title": title, 
        "news_p": paragraph,
        "image": featured_image_url,
        "mars_df": mars_table,
        "mars_hem": hemurl
    }

    return data



