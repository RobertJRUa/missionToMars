#!/usr/bin/env python
# coding: utf-8

# Import dependencies 
import pandas as pd 
from splinter import Browser
from bs4 import BeautifulSoup
import time 

# Set up custom path to Chrome Webdriver  
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}

# Enable Chrome browser in headless environment 
browser = Browser('chrome', **executable_path, headless=False)


# Create function for scraped data 
def scrape():
    mars_data = {}
    output = marsNews()
    mars_data["mars_news"] = output[0]
    mars_data["mars_paragraph"] = output[1]
    mars_data["mars_image"] = marsImage()
    mars_data["mars_weather"] = marsWeather()
    mars_data["mars_facts"] = marsFacts()
    mars_data["mars_hemisphere"] = marsHem()

    return mars_data


# News from Mars 
def marsNews():
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    article = soup.find("div", class_='list_text')
    news_title = article.find("div", class_="content_title").text
    news_p = article.find("div", class_ ="article_teaser_body").text
    output = [news_title, news_p]
    
    return output


# Pics from Mars 
def marsImage():
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    image = soup.find("img", class_="thumb")["src"]
    featured_image_url = "https://www.jpl.nasa.gov" + image
    return featured_image_url

# Tweets from Mars 
def marsWeather():

    try: 

        browser = init_browser()
        weather_url = 'https://twitter.com/marswxreport?lang=en'
        browser.visit(weather_url)
        html_weather = browser.html
        soup = BeautifulSoup(html_weather, 'html.parser')
        time.sleep(10)
        latest_tweets = soup.find_all('div', class_='js-tweet-text-container')
        
        for tweet in latest_tweets: 
            weather_tweet = tweet.find('p').text
            if 'Sol' and 'pressure' in weather_tweet:
                print(weather_tweet)
                break
            else: 
                pass

        mars_data["mars_weather"] = weather_tweet
        
        return mars_data    


# Facts from Mars 
def marsFacts():
    facts_url = 'http://space-facts.com/mars/'
    mars_facts = pd.read_html(facts_url)
    mars_df = mars_facts[0]
    mars_df.columns = ['Description','Value']
    mars_df.set_index('Description', inplace=True)
    data = mars_df.to_html()
    mars_data['mars_facts'] = data
    return mars_data


# Mars Hemispheres
def marsHem():

    try: 
        browser = init_browser()
        hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemispheres_url)
        html_hemispheres = browser.html
        soup = BeautifulSoup(html_hemispheres, 'html.parser')
        items = soup.find_all('div', class_='item')
        hem_urls = []
        hemispheres_main_url = 'https://astrogeology.usgs.gov' 

        for i in items: 
            
            title = i.find('h3').text
            partial_img_url = i.find('a', class_='itemLink product-item')['href']
            browser.visit(hemispheres_main_url + partial_img_url)
            partial_img_html = browser.html
            soup = BeautifulSoup( partial_img_html, 'html.parser')
            img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
            hem_urls.append({'title' : title, 'img_url' : img_url})

        mars_data['mars_hemisphere'] = hem_urls

        return mars_data
    
