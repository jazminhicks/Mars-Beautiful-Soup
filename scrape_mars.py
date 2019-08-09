# import dependencies
from flask import Flask, render_template
from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import pymongo
import pandas as pd
import time

# establish connection 
def init_browser():
    executable_path = {"executable_path": "C:\Drivers\chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    mars_data = {}

    #------NASA Mars News
    # scrape latest mars news article and title
    nasa_url = 'https://mars.nasa.gov/news/'
    
    #visit page
    browser.visit(nasa_url)

    time.sleep(1)

    news_html = browser.html
    news_soup = bs(news_html, "html.parser")

    #scrape first news title and paragraph
    news_title = news_soup.find("div",class_="content_title").text
    news_paragraph = news_soup.find("div", class_="article_teaser_body").text

    # add news data to dictionary
    mars_data["news_title"] = news_title
    mars_data["news_paragraph"] = news_paragraph



    #--------JPL Mars Space Images - Featured Image
    # scrape featured space image from site
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    #visit page
    browser.visit(jpl_url)

    time.sleep(1)

    img_html = browser.html
    img_soup = bs(img_html, "html.parser")

    base_path = "https://www.jpl.nasa.gov"
    image_path = img_soup.find("article")['style'].replace("background-image: url('", "").replace("');", "")

    featured_image_url = base_path + image_path

    # add featured image data to dictionary
    mars_data["featured_image_url"] = featured_image_url



    #--------Mars Weather
    # scrape weather data from Mars twitter page
    twitter_url = 'https://twitter.com/marswxreport?lang=en'

    #visit page
    browser.visit(twitter_url)

    time.sleep(1)

    weather_html = browser.html
    weather_soup = bs(weather_html, "html.parser")

    tweets = weather_soup.find_all("div", class_="js-tweet-text-container")
    for tweet in tweets:
        if 'InSight' in tweet.text:
            weather = tweet.text
            break

    
    weather_n = weather.replace('\n','')
    mars_weather = weather_n[:weather_n.find("pic")]

    # add weather data from twitter to dictionary
    mars_data["mars_weather"] = mars_weather



    #----------Mars Facts
    # scrape a table with facts about mars using pandas
    facts_url = 'https://space-facts.com/mars/'

    table = pd.read_html(facts_url)
    mars_table = table[1].rename(columns = {0:"", 1: "value"})
    mars_table.set_index("", inplace = True)

    mars_html = mars_table.to_html(index=True)
    facts_html = mars_html.replace('\n', '') #clean up data

    mars_data["facts_html"] = facts_html



    #------------Mars Hemispheres
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    
    #visit page
    browser.visit(hemisphere_url)
    
    html = browser.html
    soup = bs(html, "html.parser")
    
    hemi_base = "https://astrogeology.usgs.gov"
    
    links = []
    results = soup.find_all("div", class_="item")
    for result in results:
        link = result.find('a')
        hemi_link = link['href']
        hemi_url_2 = hemi_base + hemi_link
        links.append(hemi_url_2)



    hemisphere_image_urls = []
     
    for link in links:
            img_dict = {}
            browser.visit(link)
            html = browser.html
            soup = bs(html, "html.parser")
            
            img = soup.find("img", class_="wide-image")
            #print(img['src'])
            img_link = hemi_base + img['src']
            
            img_title = soup.find("h2", class_="title")
            #print(img_title.text)
            img_dict["title"] = img_title.text
            img_dict["img_url"] = img_link
            hemisphere_image_urls.append(img_dict)
            
    
    mars_data["hemisphere_image_urls"] = hemisphere_image_urls
    
    browser.quit()
    
    print(mars_data)
    
    #return dictionary with scraped data
    return mars_data