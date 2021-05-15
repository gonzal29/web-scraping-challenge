from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    executable_path = {"executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    soup = bs(browser.html, 'html.parser')
    type(soup)
    news_title = soup.title.text.strip()
    news_p = soup.body.find_all('p')[0].text
    data = {
        "news_title": news_title, 
        "news_paragraph": news_p,
        "img_source":news_mars(browser),
        "mars_table":mars_facts(browser),
        "mars_hemispheres": mars_images(browser)
        }
    return data


def news_mars(browser):
        url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
        browser.visit(url)
        img_soup = bs(browser.html, 'html.parser')
        img_url_rel = img_soup.find('img', class_='headerimage fade-in').get('src')
        # Use the base url to create an absolute url
        img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
        return img_url

import pandas as pd
def mars_facts(browser):
    url_table = 'https://space-facts.com/mars/'
    browser.visit(url_table)
    tables = pd.read_html(url_table)
    df = tables[0]
    df = df.rename(columns={0:'Description',1:'Mars'})
    df = df.set_index("Description")
    return df.to_html(classes="table table-striped")
def mars_images(browser):
    url_hemispheres = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hemispheres)
    hemisphere_image_urls = []
    links = browser.find_by_css("a.product-item h3")
    for item in range(len(links)):
        hemisphere = {}
        browser.find_by_css("a.product-item h3")[item].click()
        sample_element = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]
        hemisphere["title"] = browser.find_by_css("h2.title").text
        hemisphere_image_urls.append(hemisphere)
        browser.back()
    return hemisphere_image_urls



# import requests
# from os.path  import basename


# In[ ]:

# def scrape():
#     executable_path = {'executable_path': ChromeDriverManager().install()}
#     browser = Browser('chrome', **executable_path, headless=False)



