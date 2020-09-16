from flask import Flask, request, send_file
from sbgnrender.RendererClient import renderSBGN

import os, tempfile, io

UPLOAD_FOLDER = '/var/sbgn-rest-renderer/static'
ALLOWED_EXTENSIONS = {'xml'}

api = Flask(__name__)
api.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# A method to access stored pngs (add store option in API, returns an id to access later)
# @api.route('/store')

# @api.route('/', methods=['GET'])
# def home():
#     return send_file('index.html')
    
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
      
            renderSBGN(
                os.path.join(api.config['UPLOAD_FOLDER'], os.path.basename(folder), filename), 
                os.path.join(folder, "output.png"),
                format = request.values.get("format"),
                scale = request.values.get("scale"),
                bg = request.values.get("bg"),
                max_width = request.values.get("max_width"),
                max_height = request.values.get("max_height"),
                quality = request.values.get("quality"),
                layout = request.values.get("layout")
            )
      
            binary = io.BytesIO(open(os.path.join(folder, "output.png"), 'rb').read())
      
            return send_file(binary, attachment_filename='output.png', mimetype='image/png')
        
    else:
        raise Exception("DISALLOWED_FILE_TYPE")
    
if __name__ == '__main__':
    api.run(host="0.0.0.0", port=8082)