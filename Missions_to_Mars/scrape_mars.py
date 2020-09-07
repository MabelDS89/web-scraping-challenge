#!/usr/bin/env python
# coding: utf-8

#Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time
import requests

# In[1]:

def scrape():

    # In[2]:


    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)


    # # Step 1 - Scraping

    # NASA Mars News

    # In[9]:

    mars_dict = {}

    #URL of NASA Mars News Site
    url1 = '''https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=
    19%2C165%2C184%2C204&blank_scope=Latest'''

    browser.visit(url1)


    # In[10]:


    #HTML object
    html1 = browser.html

    #Parse HTML with BeautifulSoup
    soup1 = BeautifulSoup(html1, 'html.parser')


    # In[11]:


    #Retrieve first article
    # first_art = soup1.find('li', class_= 'slide')

    # In[12]:


    #Use Beautiful Soup's find() method to navigate and retrieve attributes

    # step1 = soup1.find('div', class_='image_and_description_container')
    # step2 = step1.find('div', class_='list_text')
    # news_title = step2.find('div', class_='content_title').get_text

    try:
        step1 = soup1.select_one('div.image_and_description_container div.list_text')
        #find news title
        news_title = step1.find("div", class_="content_title").text
        #find news paragraph
        news_p= step1.find("div", class_="article_teaser_body").text
    except:
        return None, None

    #Add news_title to the mars_dict dictionary
    mars_dict['News Title'] = news_title

    # news_p = soup1.find('div', class_= 'article_teaser_body').get_text

    #Add news_p to the mars_dict dictionary
    mars_dict["News Para."] = news_p


    # JPL Mars Space Images - Featured Image

    # In[17]:


    #URL of JPL Mars Space Images Site
    url2 = '''https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'''

    browser.visit(url2)


    # In[18]:


    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(3)


    # In[19]:


    browser.click_link_by_partial_text('more info')
    time.sleep(3)

    #HTML object
    html2 = browser.html

    #Parse HTML with BeautifulSoup
    soup2 = BeautifulSoup(html2, 'html.parser')

    # In[24]:


    image_url = soup2.find('figure', class_="lede").a['href']
    image_url


    # In[25]:


    featured_image_url = 'https://www.jpl.nasa.gov' + image_url

    #Add featured_image_url to the mars_dict dictionary
    mars_dict['Featured Image URL']= featured_image_url


    # Mars Facts

    # In[28]:


    #URL of Space Facts Site
    url3 = 'https://space-facts.com/mars/'


    # In[29]:


    #Read in table
    mars_table = pd.read_html(url3)
    mars_table


    # In[32]:


    #Create a DataFrame with the 1st table available on the site
    df = mars_table[0]
    df


    # In[33]:


    #Convert the DataFrame table to HTML
    html_table = df.to_html()
    html_table


    # In[38]:


    #Remove escape sequences
    html_table = html_table.replace('\n', '')

    #Add html_table to the mars_dict dictionary
    mars_dict['Mars Table'] = html_table


    # Mars Hemispheres

    # In[3]:


    # URL of page to be scraped
    url4 = '''https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'''

    browser.visit(url4)

    #HTML object
    html4 = browser.html


    # In[8]:


    # Find titles and image urls and build the dictionary
    titles = browser.find_by_css('a.product-item h3')    

    hemi_list = []

    for i in range(len(titles)):
        hemi_dict = {}
        browser.find_by_css('a.product-item h3')[i].click()
        sample = browser.find_by_text('Sample')
        image_url = sample['href']
        hemi_dict['Title'] = browser.find_by_css('h2.title').text
        hemi_dict['ImageURL'] = image_url
        hemi_list.append(hemi_dict)
        browser.back()
        print("---")
        print(hemi_dict['Title'])
        print(image_url)


    # In[9]:

    #Add hemi_list to the mars_dict dictionary
    mars_dict['Hemispheres'] = hemi_list

    return mars_dict



