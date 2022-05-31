from flask import Flask, make_response, jsonify

# Datas
from model.data import Dataset

app = Flask(__name__)

app.config['SECRET_KEY'] = 'UHGx14#&17NoPRQS#12'
app.config['JWT_SECRET_KEY'] = app.config['SECRET_KEY']

@app.route("/")
def hello_world():
    dataset = Dataset("www.datos.gov.co", "gt2j-8ykr")
    df = dataset.__getitem__()
    return make_response(jsonify(df), 200)

if __name__ == "__main__":
    app.run(debug=True)