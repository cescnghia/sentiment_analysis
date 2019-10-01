from flask import Flask, jsonify, request, render_template
import pickle
import requests
from utils import processing_text
from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer

PATH_SVM_PRETRAINED_MODEL = 'models/cls.pickle'
PATH_TFIDF_PRETRAINED_MODEL = 'models/tfidf.pickle'

app = Flask(__name__)


###########
### APP ###
###########
@app.route('/', methods=['GET', 'POST'])
def index():
    errors = []
    results = {}
    if request.method == 'POST':
        try:
            review = request.form['review']
        except:
            errors.append("Unable to get review. Please make sure it's valid and try again.")
            return render_template('index.html', errors=errors)
        
        if review:
            "Preprocessing text"
            review = processing_text(review)
            "Load trained models"
            cls = pickle.load(open(PATH_SVM_PRETRAINED_MODEL, 'rb'))
            tfidf_vectorizer = pickle.load(open(PATH_TFIDF_PRETRAINED_MODEL, 'rb'))
            tfidf = tfidf_vectorizer.transform([review])
            "Get prediction"
            prediction = cls.predict(tfidf)[0]
            
            results['positive'] = 'True' if prediction == 1 else 'False'

    return render_template('index.html', errors=errors, results=results)




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)