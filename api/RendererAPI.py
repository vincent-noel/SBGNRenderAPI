from flask import Flask, request, send_file
from RendererClient import renderSBGN
import os, tempfile, io

UPLOAD_FOLDER = '/var/sbgn-rest-renderer/static'
ALLOWED_EXTENSIONS = {'xml'}

api = Flask(__name__)
api.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@api.route('/render', methods=['POST'])
def render():
  
    # check if the post request has the file part
    if 'file' not in request.files:
        raise Exception("NO FILES")
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        raise Exception("EMPTY FILE")
        
    if file:
        with tempfile.TemporaryDirectory(dir=api.config['UPLOAD_FOLDER']) as folder:
            filename = file.filename
            file.save(os.path.join(folder, filename))
      
            renderSBGN(os.path.join("static", os.path.basename(folder), filename), os.path.join(folder, "output.png"))
      
            binary = io.BytesIO(open(os.path.join(folder, "output.png"), 'rb').read())
      
            return send_file(binary, attachment_filename='output.png', mimetype='image/png')
        
    else:
        raise Exception("DISALLOWED_FILE_TYPE")
    
if __name__ == '__main__':
    api.run(host="0.0.0.0")