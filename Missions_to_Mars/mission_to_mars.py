
#Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time
import requests

executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

# # Step 1 - Scraping

# NASA Mars News

#URL of NASA Mars News Site
url1 = '''https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=
19%2C165%2C184%2C204&blank_scope=Latest'''

browser.visit(url1)

#HTML object
html1 = browser.html

#Parse HTML with BeautifulSoup
soup1 = BeautifulSoup(html1, 'html.parser')

#Retrieve first article
first_art = soup1.find('div', class_= 'list_text')
print(first_art)

#Use Beautiful Soup's find() method to navigate and retrieve attributes

news_title = first_art.find('a').text
print(news_title)

print('-----')

news_p = soup1.find('div', class_= 'article_teaser_body').text
print(news_p)

# JPL Mars Space Images - Featured Image


#URL of JPL Mars Space Images Site
url2 = '''https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'''

browser.visit(url2)

browser.click_link_by_partial_text('FULL IMAGE')
time.sleep(3)

browser.click_link_by_partial_text('more info')
time.sleep(3)

#HTML object
html2 = browser.html

#Parse HTML with BeautifulSoup
soup2 = BeautifulSoup(html2, 'html.parser')

soup2

image_url = soup2.find('figure', class_="lede").a['href']
image_url

featured_image_url = 'https://www.jpl.nasa.gov' + image_url
featured_image_url

# Mars Facts

#URL of Space Facts Site
url3 = 'https://space-facts.com/mars/'

#Read in table
mars_table = pd.read_html(url3)
mars_table

#Create a DataFrame with the 1st table available on the site
df = mars_table[0]
df

#Convert the DataFrame table to HTML
html_table = df.to_html()
html_table

#Remove escape sequences
html_table = html_table.replace('\n', '')
html_table

# Mars Hemispheres

# URL of page to be scraped
url4 = '''https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'''

browser.visit(url4)

#HTML object
html4 = browser.html

# Find titles and image urls and build the dictionary
titles = browser.find_by_css('a.product-item h3')    

hemi_list = []

for i in range(len(titles)):
    hemi_dict = {}
    browser.find_by_css('a.product-item h3')[i].click()
    sample = browser.find_by_text('Sample').first
    image_url = sample['href']
    title = titles[i]
    hemi_dict['Title'] = title
    hemi_dict['ImageURL'] = image_url
    hemi_list.append(hemi_dict)
    browser.back()
    print("---")
    print(title)
    print(image_url)
    print(hemi_dict)

