import os
import time
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver 
from selenium.webdriver.common.by import By # This needs to be used 
import pandas as pd

def flipkart():
    file_path = "p_name.txt" 
    with open(file_path, 'r') as file:
        searchString = file.read()
    searchString=searchString.replace('-','+')

    from selenium import webdriver

    # Define the path to the Chrome WebDriver executable
    #DRIVER_PATH = r"C:\Users\Tarak\OneDrive\Desktop\classer\FlipKart_Selenium-main\chromedriver.exe"

    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome()
    #searchString = "motorola+G84"
    flipkart_url = "https://www.flipkart.com/search?q=" + searchString 
    print(flipkart_url)
    # Open the Flipkart URL
    driver.get(flipkart_url)

    page_text = driver.page_source


    flipkart_html = bs(page_text, 'html.parser')

    bigboxes =flipkart_html.findAll("div", {"class": "_1AtVbE col-12-12"})
    del bigboxes[0:3]
    box = bigboxes[0]

    productLink = "https://www.flipkart.com" + box.div.div.div.a['href']
    # Open the Flipkart URL
    driver.get(productLink)
    prodRes= driver.page_source
    driver.quit()
    prod_html = bs(prodRes, "html.parser")
    commentboxes = prod_html.find_all('div', {'class': "_16PBlm"})

    reviews = []

    for commentbox in commentboxes:
        try:
            price_element = flipkart_html.select('div._25b18c ._30jeq3')[0]
            price = price_element.text
        except Exception as e:    
            price = 'Price not found: ' + str(e)

        try:
            name = commentbox.div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text
        except Exception as e:
            name = 'Name not found: ' + str(e)

        try:
            rating = commentbox.div.div.div.div.text
        except Exception as e:
            rating = 'Rating not found: ' + str(e)

        try:
            commentHead = commentbox.div.div.div.p.text
        except Exception as e:
            commentHead = 'Comment Head not found: ' + str(e)

        try:
            comtag = commentbox.div.div.find_all('div', {'class': ''})
            custComment = comtag[0].div.text
        except Exception as e:
            custComment = 'Comment not found: ' + str(e)

        mydict = {"Price": price, "Product": searchString, "Rating": rating, "Heading": commentHead, "Comment": custComment}
        reviews.append(mydict)


    # Create a dataframe with reviews Data
    df_reviews = pd.DataFrame(reviews)
    print(df_reviews)



