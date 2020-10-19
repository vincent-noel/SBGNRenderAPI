import requests, json, time, os
from PIL import Image
import xml.etree.ElementTree as ET
from unittest import TestCase

def read_image_size(format, file):
    if format != "svg":
        with Image.open(file) as im:
            return im.size
        
    else:
        tree = ET.parse(file)
        root = tree.getroot()
        return int(float(root.attrib['width'])), int(float(root.attrib['height']))

class TestSize(TestCase):
    
    def test_size(self):
        
        result_scale_1 = 1752, 1168
        result_scale_2 = 3504, 2336
        result_scale_3 = 5256, 3504
        result_maxwidth_2000 = 2000, 1333
        result_maxwidth_4000 = 4000, 2666
        sbgn_filename = os.path.join(os.path.basename(os.path.dirname(__file__)), "Reaction_Species.xml")

        formats = ["png", "jpg", "svg"]
    
        for format in formats:
            # Default

            with open(sbgn_filename,'rb') as sbgn_file:
                files = {'file': sbgn_file}
                values = {'format': format}
                r = requests.post("http://localhost:8082/render", files=files, data=values)
                
                with open('network_default.' + format, 'wb') as f:
                    f.write(r.content)

            if format != "svg":
                self.assertEqual(result_scale_3, read_image_size(format, 'network_default.' + format))
            else:
                self.assertEqual(result_scale_1, read_image_size(format, 'network_default.' + format))
                
            # With scale
            with open(sbgn_filename,'rb') as sbgn_file:
                files = {'file': sbgn_file}
                values = {
                    'scale': 1, 'format': format
                }

                r = requests.post("http://localhost:8082/render", files=files, data=values)
                with open('network_scale_1.' + format, 'wb') as f:
                    f.write(r.content)

            self.assertEqual(result_scale_1, read_image_size(format, 'network_scale_1.' + format))

            with open(sbgn_filename,'rb') as sbgn_file:
                files = {'file': sbgn_file}
                values = {
                    'scale': 2, 'format': format
                }

                r = requests.post("http://localhost:8082/render", files=files, data=values)
                with open('network_scale_2.' + format, 'wb') as f:
                    f.write(r.content)

            self.assertEqual(result_scale_2, read_image_size(format, 'network_scale_2.' + format))

            # With maxWidth
            with open(sbgn_filename,'rb') as sbgn_file:
                files = {'file': sbgn_file}
                values = {
                    'max_width': 2000, 'max_height': 2000, 'format': format
                }

                r = requests.post("http://localhost:8082/render", files=files, data=values)
                with open('network_maxwidth_2000.' + format, 'wb') as f:
                    f.write(r.content)

            self.assertEqual(result_maxwidth_2000, read_image_size(format, 'network_maxwidth_2000.' + format))


            with open(sbgn_filename,'rb') as sbgn_file:
                files = {'file': sbgn_file}
                values = {
                    'max_width': 4000, 'max_height': 4000, 'format': format
                }

                r = requests.post("http://localhost:8082/render", files=files, data=values)
                with open('network_maxwidth_4000.' + format, 'wb') as f:
                    f.write(r.content)

            self.assertEqual(result_maxwidth_4000, read_image_size(format, 'network_maxwidth_4000.' + format))

            # With both
            with open(sbgn_filename,'rb') as sbgn_file:
                files = {'file': sbgn_file}
                values = {
                    'max_width': 2000, 'max_height': 2000, 'scale': 3,'format': format
                }

                r = requests.post("http://localhost:8082/render", files=files, data=values)
                with open('network_maxwidth_2000_scale_3.' + format, 'wb') as f:
                    f.write(r.content)

            self.assertEqual(result_maxwidth_2000, read_image_size(format, 'network_maxwidth_2000_scale_3.' + format))

            with open(sbgn_filename,'rb') as sbgn_file:
                files = {'file': sbgn_file}
                values = {
                    'max_width': 4000, 'max_height': 4000, 'scale': 3,'format': format
                }

                r = requests.post("http://localhost:8082/render", files=files, data=values)
                with open('network_maxwidth_4000_scale_3.' + format, 'wb') as f:
                    f.write(r.content)
                    
            self.assertEqual(result_maxwidth_4000, read_image_size(format, 'network_maxwidth_4000_scale_3.' + format))