import amz
import flk
import sentiment
from fake import convertmyTxt
from fake import load_svm_model
import os
from bs4 import BeautifulSoup
import urllib
import requests



def mainfun(url):  
    #url=input("Enter url: ")


    df ,Title= amz.amazon(url)
    def check_csv_exists(file_name):
        return os.path.isfile(file_name)
    csv_file_name = Title+'.csv'
    if check_csv_exists(csv_file_name):
        return csv_file_name, Title
    else:
        # Load the trained pipeline from the file
        trained_pipeline = load_svm_model()

        # Test with a custom sentence lable prediction
        print("processing")
        df['label'] = trained_pipeline.predict(df['Description'])

        #prediction = trained_pipeline.predict([custom_sentence])

        #print(f"Predicted Label: {prediction[0]}")


        #sentiment analysis
        df['Sentiment'] = df['Description'].apply(sentiment.analyze_sentiment)

        print(df)
        csv_file_path=Title+'.csv'
        with open(csv_file_path, 'w') as csvfile:    
            pass

        # Use the to_csv method to convert and save the DataFrame to a CSV file
        df.to_csv(csv_file_path, index=False)
        return csv_file_name, Title

        #flk.flipkart()


