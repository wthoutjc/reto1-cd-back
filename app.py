from flask import Flask, make_response, jsonify, request
from decouple import config

# Tools
import json

# Datas
from model.data import Dataset

app = Flask(__name__)

app.config['SECRET_KEY'] = config('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = app.config['SECRET_KEY']

dataset = Dataset("www.datos.gov.co", "gt2j-8ykr")

@app.route("/", methods=['GET', 'POST'])
def root_data():
    if request.method == 'POST':
        data_raw = request.data.decode("utf-8")
        json_data = json.loads(data_raw)

        filtro = json_data['filtro']
        valor = json_data['valor']

        print(filtro, valor)

        filtro = dataset.normalize_column(filtro)
        # valor = dataset.normalize_value(filtro, valor)

        # result es el nuevo df dado un filtro y un valor
        result = dataset.query(filtro, valor)

        return make_response(jsonify(result), 200)
    records = dataset.__getitem__()
    return make_response(jsonify(records), 200)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')