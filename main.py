import os
import subprocess
import signal
import pathlib
import shutil

from flask import Flask, send_from_directory, request, jsonify
from flask_restful import reqparse
from flask_cors import CORS

from cmd import create_command
from schema import schema
from jsonschema import validate

parser = reqparse.RequestParser()
app = Flask(__name__)

CORS(app)
RECORDINGS = {}
CONTENT_PATH = "records"


def record_path(rid):
    return os.path.join(app.root_path, CONTENT_PATH) + "/" + rid


@app.route('/record/<path:rid>/stop', methods=['POST'])
def stop_recording(rid):
    if rid in RECORDINGS:
        process = RECORDINGS[rid]["process"]
        if process:
            process.send_signal(signal.SIGINT)
            process.wait()
            # process.kill()
            RECORDINGS[rid]["status"] = 'stopped'
            return jsonify({'status': 'ok'})
        else:
            return jsonify({'status': 'error', 'msg': 'Process already died'})
    else:
        return jsonify({'status': 'error', 'msg': 'No process found in process list'})


@app.route('/record/<path:rid>', methods=['DELETE'])
def delete_record(rid):
    try:
        shutil.rmtree(pathlib.Path(record_path(rid)))
    except FileNotFoundError:
        return jsonify({'status': 'error', 'msg': 'Directory not found'})

    if hasattr(RECORDINGS, rid):
        del RECORDINGS[rid]

    return jsonify({'status': 'ok'})


@app.route('/record/<path:rid>', methods=['POST'])
def create_record(rid):
    data = request.get_json()
    validate(instance=data, schema=schema)

    path = record_path(rid)
    os.makedirs(path, mode=0o775, exist_ok=True)
    command = create_command(data, path)

    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    RECORDINGS[rid] = {
        "status": "new",
        "process": process
    }

    return jsonify({'status': 'ok'})


@app.route('/record/<path:dir_name>/<path:filename>', methods=['GET'])
def download(dir_name, filename):
    d = os.path.join(app.root_path, CONTENT_PATH, dir_name)

    return send_from_directory(
        directory=d,
        path=filename)


if __name__ == "__main__":
    # app.run(debug=True)
    from waitress import serve
    serve(app, host="127.0.0.1", port=5000)
