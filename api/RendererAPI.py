from flask import Flask, json, request, redirect, url_for, flash, jsonify, send_from_directory, send_file
from RendererClient import RendererClient
import os, tempfile

UPLOAD_FOLDER = '/var/sbgn-rest-renderer/static'
ALLOWED_EXTENSIONS = {'xml'}

api = Flask(__name__, static_url_path='', static_folder=UPLOAD_FOLDER)
api.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@api.route('/', methods=['GET'])
def home():
    return jsonify(success=True)

@api.route('/render', methods=['POST'])
def render():
    client = RendererClient()
  
    # check if the post request has the file part
    if 'file' not in request.files:
        raise Exception("NO FILES")
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        raise Exception("EMPTY FILE")
        
    if file:
        filename = file.filename
        folder = tempfile.mkdtemp(dir=api.config['UPLOAD_FOLDER'])
        file.save(os.path.join(folder, filename))
        print(" FILE SAVED !! SUCCESS !")
        url = "http://localhost/%s" % os.path.join(os.path.basename(folder), filename)
        client.render(url, os.path.join(folder, "output.png"))
        print("FILE RENDERER !!!")
        return send_file(os.path.join(folder, "output.png"), mimetype='image/png')
    else:
        raise Exception("DISALLOWED_FILE_TYPE")

    # return jsonify(success=True)

# @app.route('/static/<path:path>')
# def send_static(path):
#     return send_from_directory('upload_dir', path)
    
if __name__ == '__main__':
    api.run(host="0.0.0.0")