from flask import Flask, redirect, render_template, request, url_for
from main import mainfun as mf
from fake import convertmyTxt
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new_page', methods=['POST', 'GET'])
def new_page():
    input_text = request.form['keyword']
    csv_path, Title= mf(input_text)
    df = pd.read_csv(csv_path)
    return render_template('new_page.html', submitted_text=input_text, csv_data=df.to_html(), Name=Title)

@app.route('/topics_detail')
def topics_detail():
    return render_template('topics_detail.html')



if __name__ == '__main__':
    app.run(debug=True)
