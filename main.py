import os
import subprocess
import signal
import pathlib
import shutil
import re

from flask import Flask, send_from_directory, request, jsonify
from flask_restful import reqparse
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from pathvalidate import sanitize_filename

import argparse

from cmd import create_command
from schema import schema
from jsonschema import validate

parser = reqparse.RequestParser()
app = Flask(__name__)
auth = HTTPBasicAuth()

argParser = argparse.ArgumentParser()
argParser.add_argument("-u", "--username", help="Username")
argParser.add_argument("-p", "--password", help="Password")
argParser.add_argument("-c", "--path", help="Content path", default="/var/www/static")
argParser.add_argument("-s", "--host", help="Host to run", default="127.0.0.1")
argParser.add_argument("-r", "--port", help="Port to run", default=5000)

CORS(app)
RECORDINGS = {}

args = argParser.parse_args()
CONTENT_PATH = args.path


def record_path(rid):
    return CONTENT_PATH + "/" + rid


@app.route('/record/<path:rid>/stop', methods=['POST'])
@auth.login_required
def stop_recording(rid):
    if rid in RECORDINGS:
        process = RECORDINGS[rid]["process"]
        if process:
            process.send_signal(signal.SIGINT)
            process.wait()
            # RECORDINGS[rid]['logfile'].flush()
            # process.kill()
            RECORDINGS[rid]["cmd"] = 'STOP'
            return jsonify({'status': 200})
        else:
            return jsonify({'status': 400, 'msg': 'Process already died'})
    else:
        return jsonify({'status': 404, 'msg': 'No process found in process list'})


@app.route('/record/<path:rid>', methods=['DELETE'])
@auth.login_required
def delete_record(rid):
    try:
        shutil.rmtree(pathlib.Path(record_path(rid)))
    except FileNotFoundError:
        return jsonify({'status': 404, 'msg': 'Directory not found'})

    if hasattr(RECORDINGS, rid):
        del RECORDINGS[rid]

    return jsonify({'status': 204})


@app.route('/record/<path:rid>', methods=['POST'])
@auth.login_required
def create_record(rid):
    if rid in RECORDINGS:
        process = RECORDINGS[rid]['process']
        poll = process.poll()
        if poll is None:
            return jsonify({'status': 400, 'msg': 'In progress'})

    data = request.get_json()
    validate(instance=data, schema=schema)

    path = record_path(rid)
    os.makedirs(path, mode=0o775, exist_ok=True)
    command = create_command(data, path)

    logfile = open(path + '/logfile.txt', "w")
    process = subprocess.Popen(command,
                               stdin=subprocess.PIPE,
                               stdout=logfile,
                               stderr=logfile)
    RECORDINGS[rid] = {
        "cmd": "RECORD",
        "source_url": data['source_url'],
        "process": process,
        # "logfile": logfile,
    }

    return jsonify({'status': 201})


@app.route('/record/<path:dir_name>/<path:filename>', methods=['GET'])
def download(dir_name, filename):
    dir_name = re.sub(r"[^A-Fa-f0-9\-]+", '', dir_name)
    filename = sanitize_filename(filename=filename, replacement_text=":", max_len=28)

    return send_from_directory(
        directory=os.path.join(CONTENT_PATH, dir_name),
        path=filename)


@app.route('/record/<path:rid>', methods=['GET'])
@auth.login_required
def status(rid):
    if rid not in RECORDINGS:
        return jsonify({'status': 404})

    rec = RECORDINGS[rid]
    poll = rec['process'].poll()

    alive = False
    if poll is None:
        alive = True

    res = {
        'id': rid,
        'cmd': rec['cmd'],
        'source_url': rec['source_url'],
        'alive': alive,
        'poll': str(rec['process'].stdout.read())
    }

    return jsonify(res)


@auth.verify_password
def verify_password(username, password):
    args = argParser.parse_args()

    return username == args.username and password == args.password


if __name__ == "__main__":
    # app.run(debug=True)
    from waitress import serve

    args = argParser.parse_args()
    serve(app, host=args.host, port=args.port)
