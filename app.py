from flask import Flask, make_response, jsonify, request
import json
# Datas
from model.data import Dataset

app = Flask(__name__)

app.config['SECRET_KEY'] = 'UHGx14#&17NoPRQS#12'
app.config['JWT_SECRET_KEY'] = app.config['SECRET_KEY']

@app.route("/", methods=['GET', 'POST'])
def root_data():
    if request.method == 'POST':
        data_raw = request.data.decode("utf-8")
        json_data = json.loads(data_raw)

        filtro = json_data['filtro']
        valor = json_data['valor']

        # result es el nuevo df dado un filtro y un valor
        result = 0

        return make_response(jsonify(result), 200)
    dataset = Dataset("www.datos.gov.co", "gt2j-8ykr")
    df = dataset.__getitem__()
    return make_response(jsonify(df), 200)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')