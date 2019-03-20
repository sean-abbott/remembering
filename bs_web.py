import bs_interface_lib as bs_lib

import json

from flask import Flask
from flask import request
from flask import Response

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Flask Dockerized'

@app.route('/queue', methods=['POST'])
def queue():
    if request.method == 'POST':
        data = request.form
        if "job" not in data or "period" not in data:
            message = "Queue requires a job name and a period"
            resp = Response(message, status=400)
            return resp
        task_id = bs_lib.queue(data["job"], data["period"])
        message = {"task_id": task_id}
        resp = Response(json.dumps(message), status=201)
        return resp

@app.route('/status/<int:task_id>')
def status(task_id):
    if request.method != 'GET':
        resp = Response(status=400)
        return resp
    task_id_status = bs_lib.status(task_id)
    if task_id_status is None:
        resp = Response(status=404)
        return resp
    for dt in ['start', 'end']:
        if task_id_status[dt] is not None:
            task_id_status[dt] = task_id_status[dt].strftime("%Y-%m-%d %H:%M:%S")
    resp = Response(json.dumps(task_id_status), status=200)
    return resp

@app.route('/delete/<int:task_id>', methods=['DELETE'])
def delete(task_id):
    if request.method != 'DELETE':
        resp = Response(status=400)
        return resp
    try:
        bs_lib.delete(task_id)
    except:
        resp = Response(status=500)
        return resp

    resp = Response(status=200)
    return resp

    

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
