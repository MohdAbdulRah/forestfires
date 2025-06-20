import pickle
import os
from flask import Flask,request,jsonify,render_template
import numpy as np 
import pandas as pd 
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

ridge = pickle.load(open("models/ridge.pkl","rb"))
scaler = pickle.load(open("models/scaler.pkl","rb"))



@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/predict",methods=["GET","POST"])
def predict_datapoint():
    if(request.method == "POST"):
        Temperature = float(request.form.get("Temperature"))
        RH = float(request.form.get("RH"))
        Ws = float(request.form.get("Ws"))
        Rain = float(request.form.get("Rain"))
        FFMC = float(request.form.get("FFMC"))
        DMC = float(request.form.get("DMC"))
        ISI = float(request.form.get("ISI"))
        Classes = float(request.form.get("Classes"))
        Region = float(request.form.get("Region"))

        new_dataScaled = scaler.transform([[Temperature,RH,Ws,Rain,FFMC,DMC,ISI,Classes,Region]])
        result = ridge.predict(new_dataScaled)

        return render_template("home.html",result=result[0])
    else:
        return render_template("home.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # use the PORT environment variable
    app.run(host='0.0.0.0', port=port)
