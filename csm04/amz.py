# Import packages
print("importing lib")
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
#from transformers import AutoTokenizer, AutoModelForSequenceClassification
import os
def check_csv_exists(file_name):
    return os.path.isfile(file_name)


def amazon(url):
    headers = {
        'authority': 'www.amazon.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-US,en;q=0.9,bn;q=0.8',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
    }
    print ("inpuut:")
    #url=input()


    # Replace "dp" with "product-reviews"
    url = url.replace("/dp/", "/product-reviews/")

    # Remove all characters after the 3rd "/"
    url_parts = url.split("/")
    Title = url_parts[3]
    csv_file_name = Title+'.csv'
    if check_csv_exists(csv_file_name):
        df = pd.read_csv(csv_file_name)
        return df,Title
    url_parts = url_parts[:6]

    modified_url = "/".join(url_parts)
    reviews_url=modified_url+'/'
    print(reviews_url)

    #storing product name for flipkart
    path = "p_name.txt"
    with open(path, 'w') as file:
        file.write("")
        Title=Title.replace(" ","+")
        file.write(Title)

    # Define Page No
    len_page = 1

    # Extra Data as Html object from amazon Review page
    def reviewsHtml(url, len_page):
        
        # Empty List define to store all pages html data
        soups = []
        
        # Loop for gather all 3000 reviews from 300 pages via range
        for page_no in range(1, len_page + 1):
            print(page_no)
            
            # parameter set as page no to the requests body
            params = {
                'ie': 'UTF8',
                'reviewerType': 'all_reviews',
                'filterByStar': 'critical',
                'pageNumber': page_no,
            }
            
            # Request make for each page
            response = requests.get(url, headers=headers)
            
            # Save Html object by using BeautifulSoup4 and lxml parser
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Add single Html page data in master soups list
            soups.append(soup)
            
        return soups
    # Grab Reviews name, description, date, stars, title from HTML 
    def getReviews(html_data):

        # Create Empty list to Hold all data
        data_dicts = []
        
        # Select all Reviews BOX html using css selector
        boxes = html_data.select('div[data-hook="review"]')
        
        # Iterate all Reviews BOX 
        for box in boxes:
            # Select Name using css selector and cleaning text using strip()
            # If Value is empty define value with 'N/A' for all.

            try:
                stars = box.select_one('[data-hook="review-star-rating"]').text.strip().split(' out')[0]
            except Exception as e:
                stars = 'N/A'   

            try:
                title = box.select_one('[data-hook="review-title"]').text.strip()
            except Exception as e:
                title = 'N/A'

            try:
                description = box.select_one('[data-hook="review-body"]').text.strip()
            except Exception as e:
                description = 'N/A'

            # create Dictionary with al review data 
            data_dict = {
                'Stars' : stars,
                'Title' : title,
                'Description' : description
            }

            # Add Dictionary in master empty List
            data_dicts.append(data_dict)
        
        return data_dicts

    # Grab all HTML
    html_datas = reviewsHtml(reviews_url, len_page)

    # Empty List to Hold all reviews data
    reviews = []

    # Iterate all Html page 
    for html_data in html_datas:
        
        # Grab review data
        review = getReviews(html_data)
        
        # add review data in reviews empty list
        reviews += review

    # Create a dataframe with reviews Data
    df_reviews = pd.DataFrame(reviews)

    #print(df_reviews)

 

    # Apply the sentiment analysis function to the 'description' column and create a new 'sentiment' column
    #df_reviews['Sentiment'] = df_reviews['Description'].apply(analyze_sentiment)

    # Save the updated DataFrame to a new CSV file
    # Replace 'output_file.csv' with the desired output file name

    #print(df_reviews)
    return df_reviews,Title




