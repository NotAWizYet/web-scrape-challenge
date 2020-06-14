#create a function to scrape mars sites for required info per sites provided
#import dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time
import lxml


def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def mars_scrape():
    # create path then add splinter browser to load pages
    ##################################################################
    # initialize browser
    browser = init_browser()

    # visit nasa's mars news site (URL Provided in HW link)
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(1)
    # scrape latest article title and or description (URL Provided in HW link)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    article_list = soup.find("ul", class_="item_list")
    news_title = article_list.find("div", class_="content_title").text
    news_p = article_list.find("div", class_="article_teaser_body").text

    # visit jpl's mars images site and navigate to featured image (URL Provided in HW link)
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(1)
    browser.find_by_css('div.carousel_items a.fancybox').click()
    time.sleep(1)
    # scrape to get featured image url (this changes frequently - Roger says doesn't matter)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    featured_image = soup.find('img', class_='fancybox-image')
    featured_image_url = "https://www.jpl.nasa.gov" + \
        str(featured_image).split(" ")[2].split('"')[1]

    # scrape twitter of mars weather twitter site account
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(1)
    mars_weather = browser.find_by_css(
        'div.js-tweet-text-container p.tweet-text').text


    # scrape table from mars facts site
    url = "https://space-facts.com/mars/"

    mars_facts_df = pd.read_html(url)[0]
    mars_facts_df = mars_facts_df.rename(index=str, columns={0: "Description", 1: "Value"})
    mars_facts_html = mars_facts_df.to_html(index='False')


    # scrape Mars Hemispheres from astropedia
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    mars_hemi_df = pd.read_html(url)[0]
    mars_hemi_df = mars_hemi_df.rename(index=str, columns={0: "Description", 1: "Value"})
    mars_hemi_html = mars_hemi_df.to_html(index='False')

    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts": mars_facts_html,
        "mars_hemispheres": mars_hemi_html
    }

    return mars_data
