from nltk.sentiment import SentimentIntensityAnalyzer

def analyze_sentiment(text):
    sia = SentimentIntensityAnalyzer()
    scores = sia.polarity_scores(text)
    com = scores['compound']
    neg = scores['neg']
    pos = scores['pos']
    neu = scores['neu']
    if com < 0 :
        return 'Negative'
    else:
        if pos >= neu:
            return 'Positive'
        else:
            return 'Neutral'
