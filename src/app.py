from flask import Flask, jsonify, request
from fbprophet import Prophet
import pandas as pd
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

app = Flask(__name__)

@app.route('/')
def hello():
    return "Finance ML Service Running!"

@app.route('/predict', methods=['POST'])
def predict_savings():
    data = request.get_json(force=True)
    df = pd.DataFrame(data)
    
    model = Prophet()
    model.fit(df)

    future = model.make_future_dataframe(periods=6, freq='M')
    forecast = model.predict(future)

    return jsonify(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(6).to_dict())

@app.route('/detect_anomalies', methods=['POST'])
def detect_anomalies():
    data = request.get_json(force=True)
    df = pd.DataFrame(data)
    
    model = IsolationForest(contamination=0.05) 
    model.fit(df[['amount']])  

    df['anomaly'] = model.predict(df[['amount']])
    
    return jsonify(df[df['anomaly'] == -1].to_dict())  

@app.route('/categorize_expenses', methods=['POST'])
def categorize_expenses():
    data = request.get_json(force=True)
    df = pd.DataFrame(data)
    vectorizer = TfidfVectorizer(max_features=1000)
    X_train = vectorizer.fit_transform(train_df['description'])
    X_test = vectorizer.transform(df['description'])
    
    clf = RandomForestClassifier()
    clf.fit(X_train, train_df['category'])
    
    df['predicted_category'] = clf.predict(X_test)
    
    return jsonify(df.to_dict())



if __name__ == '__main__':
    app.run(port=5001)  
