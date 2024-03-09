import pandas as pd
import string
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import nltk
from nltk.corpus import stopwords
from joblib import dump, load

def convertmyTxt(rv):
    np = [c for c in rv if c not in string.punctuation]
    np = ''.join(np)
    return [w for w in np.split() if w.lower() not in stopwords.words('english')]

def train_svm_model():
    dataframe = pd.read_csv('fake reviews dataset.csv')  # Replace with your actual dataset filename
    dataframe.dropna(inplace=True)
    dataframe['length'] = dataframe['text_'].apply(len)

    x_train, x_test, y_train, y_test = train_test_split(dataframe['text_'], dataframe['label'], test_size=0.25)

    pip = Pipeline([
        ('bow', CountVectorizer(analyzer=convertmyTxt)),
        ('tfidf', TfidfTransformer()),
        ('classifier', SVC())
    ])

    nltk.download('stopwords')

    pip.fit(x_train, y_train)
    supportVectorClassifier = pip.predict(x_test)
    accuracy = accuracy_score(y_test, supportVectorClassifier)
    print(f"Accuracy: {accuracy}")

    # Save the trained pipeline to a file
    dump(pip, 'svm_model.joblib')

    return pip

def load_svm_model():
    # Load the trained pipeline from the file
    return load('svm_model.joblib')

if __name__ == "__main__":
    trained_pipeline = train_svm_model()
