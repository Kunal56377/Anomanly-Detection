
from flask.helpers import url_for
from preprocessing import Preprocessor
from os import path
from Predict import Predict
from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask import Response,render_template,redirect
from Parameter import paremeter

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET', 'POST'])
@cross_origin()
def anomaly_detection():
    if request.method=='POST':
        Accountid = request.form["Accountid"]
        transction= request.form["Transaction"]
        return redirect(url_for('predict',accid = Accountid,trans = transction))
    else:
        return render_template('index.html')

@app.route("/<accid>/<trans>")
@cross_origin()
def predict(accid,trans):
    Predict_obj = Predict()
    result = Predict_obj.predict_anomaly(int(accid),int(trans))
    return f"<h1>Transction seems to fraud : {result}<h1>"
    

if __name__ == "__main__":
    if path.isfile('Processed_Data\\ProcessedData.csv'):
        pass    
    else:
        Preprocessor_obj = Preprocessor()
        Preprocessor_obj.load_data()

    app.run(debug=True,port=8000)
    

    

