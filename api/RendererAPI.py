from flask import Flask, request, send_file
from sbgnrender.RendererClient import renderSBGN, SBGNNotParsedException, SBGNNotFoundException, SBGNRenderException
from flask_cors import CORS

import os, tempfile, io, shutil, threading

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
ALLOWED_EXTENSIONS = {'xml', 'sbgnml'}

api = Flask(__name__)
api.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(api, resources={r"/*": {"origins": "*"}})

# @api.route('/', methods=['GET'])
# def home():
#     return send_file('index.html')

def _render(folder, filename, format, scale, bg, max_width, max_height, quality, layout):
    
    extension = format if format is not None else "png"
    try :
        renderSBGN(
            os.path.join(api.config['UPLOAD_FOLDER'], os.path.basename(folder), filename), 
            os.path.join(folder, "output.%s" % extension),
            format = format,
            scale = scale,
            bg = bg,
            max_width = max_width,
            max_height = max_height,
            quality = quality,
            layout = layout
        )
        
        print("Thread done")
        # return os.path.basename(folder)
        
    except SBGNNotParsedException as e:
        with open(os.path.join(folder, "error"), 'w+') as error_file:
            error_file.write("could not parse SBGN file")
        
    except SBGNNotFoundException as e:
        with open(os.path.join(folder, "error"), 'w+') as error_file:
            error_file.write("could not find SBGN file")
        
    except SBGNRenderException as e:
        with open(os.path.join(folder, "error"), 'w+') as error_file:
            error_file.write("unknown error")

class RenderingThread (threading.Thread):
    def __init__(self, folder, filename, format, scale, bg, max_width, max_height, quality, layout):
        threading.Thread.__init__(self)
        self.request = request
        self.filename = filename
        self.format = format
        self.scale = scale
        self.bg = bg
        self.max_width = max_width
        self.max_height = max_height
        self.quality = quality
        self.layout = layout
        self.folder = folder

    def run(self):
        _render(self.folder, self.filename, self.format, self.scale, self.bg, self.max_width, self.max_height, self.quality, self.layout)
        return os.path.basename(self.folder)
    
@api.route('/status/<path>')
def status(path):
    if os.path.exists(os.path.join(api.config['UPLOAD_FOLDER'], path)):
        if any([file.startswith("output.") for file in os.listdir(os.path.join(api.config['UPLOAD_FOLDER'], path))]):
            return {'status': 'ready'}, 200
        else:
            return {'status': 'processing'}, 200
    else:
        return {'status': 'not found'}, 200
    
@api.route('/rendered/<path>')
def rendered(path):
    folder = os.path.join(api.config['UPLOAD_FOLDER'], path)
    if not os.path.exists(folder):
        return {'error': 'no_path'}, 400
    outputs = [file for file in os.listdir(folder) if file.startswith("output.")]

    if len(outputs) == 1:
            
        binary = io.BytesIO(open(os.path.join(folder, outputs[0]), 'rb').read())
        extension = outputs[0].split(".")[-1]
        mimetype = "image/svg+xml" if extension == "svg" else "image/%s" % extension
        return send_file(binary, attachment_filename=outputs[0], mimetype=mimetype)

    else:
        return {'error': 'multiple_output'}, 400
        
        
@api.route('/render', methods=['POST'])
def render():

    if request.values.get("async") is not None and request.values.get("async").lower() == "true":
        
        if 'file' not in request.files:
            raise Exception("NO FILES")
        file = request.files['file']
        
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            raise Exception("EMPTY FILE")
            
        if file:
            folder = tempfile.mkdtemp(dir=api.config['UPLOAD_FOLDER'])
            filename = file.filename
            file.save(os.path.join(folder, filename))
            print(os.path.join(folder, filename))
            print(os.path.exists(os.path.join(folder, filename)))
            thread = RenderingThread(
                folder, filename, request.values.get("format"), 
                request.values.get("scale"), request.values.get("bg"), 
                request.values.get("max_width"), request.values.get("max_height"), 
                request.values.get("quality"), request.values.get("layout")
            ) 
            thread.start()
            # print(" Thread returned")
            return {'id': os.path.basename(folder)}, 200
  
    else:
        # print("SYNC rendering")
        # binary = _render(request)
        # extension = request.values.get("format") if request.values.get("format") is not None else "png"
    
        # mimetype = ('image/%s' % ("svg+xml" if extension == "svg" else extension))
        # # if shutil.rmtree(folder)
    
        
        # return send_file(binary, attachment_filename=('output.%s' % extension), mimetype=mimetype)
        
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