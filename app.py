from flask import Flask, jsonify
from app.app_configuration import AppConfiguration

from model.redis_model import DataModel

app = Flask(__name__)

conn = ""

#decorator to give json response with count and status
def convert(func):
    def convert_to_json():
        data = func()
        return jsonify(status="ok", count=len(data), data=data)
    convert_to_json.func_name = func.func_name
    return convert_to_json


@app.route("/records", methods = ['GET'])
@convert
def get_records():
    return conn.get_records()


@app.route("/response_time", methods = ['GET'])
@convert
def get_response_time():
    return conn.get_response_time_records()


@app.route("/response_time/min", methods = ['GET'])
@convert
def get_min():
    return conn.get_response_time_min()


@app.route("/response_time/max", methods = ['GET'])
@convert
def get_max():
    return conn.get_response_time_max()


@app.route("/response_time/average", methods = ['GET'])
@convert
def get_average():
    return conn.get_response_time_average()

#return json of array with tuple of min, max and average

@app.route("/response_time/all_stats", methods = ['GET'])
@convert
def get_response_time_stats():
    return conn.get_response_time_all_stats()


if __name__ == '__main__':
    conn = DataModel()
    config = AppConfiguration()
    print(config)
    app.run(port=config.port, host=config.host)