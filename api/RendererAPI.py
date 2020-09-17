from flask import Flask, request, send_file
from sbgnrender.RendererClient import renderSBGN, SBGNNotParsedException, SBGNNotFoundException, SBGNRenderException
from flask_cors import CORS

import os, tempfile, io

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
ALLOWED_EXTENSIONS = {'xml', 'sbgnml'}

api = Flask(__name__)
api.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(api, resources={r"/*": {"origins": "*"}})

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
            
            extension = request.values.get("format") if request.values.get("format") is not None else "png"
            try :
                renderSBGN(
                    os.path.join(api.config['UPLOAD_FOLDER'], os.path.basename(folder), filename), 
                    os.path.join(folder, "output.%s" % extension),
                    format = request.values.get("format"),
                    scale = request.values.get("scale"),
                    bg = request.values.get("bg"),
                    max_width = request.values.get("max_width"),
                    max_height = request.values.get("max_height"),
                    quality = request.values.get("quality"),
                    layout = request.values.get("layout")
                )
            except SBGNNotParsedException as e:
                return {'error': 'could not parse SBGN file'}, 400
            except SBGNNotFoundException as e:
                return {'error': 'could not find SBGN file'}, 400
            except SBGNRenderException as e:
                return {'error': 'unknown error'}, 400
                
            binary = io.BytesIO(open(os.path.join(folder, "output.%s" % extension), 'rb').read())
      
            return send_file(binary, attachment_filename=('output.%s' % extension), mimetype=('image/%s' % ("svg+xml" if extension == "svg" else extension)))
        
    else:
        return {'error': 'file type is not allowed'}, 400
    
if __name__ == '__main__':
    api.run(host="0.0.0.0", port=8082)