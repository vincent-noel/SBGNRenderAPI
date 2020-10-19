import requests, json, time
from unittest import TestCase

class TestModes(TestCase):
    
    def test_synchronous(self):

        # Synchronous request
        with open('Reaction_Species.xml','rb') as sbgn_file:
            files = {'file': sbgn_file}
            values = {}

            r = requests.post("http://localhost:8082/render", files=files, data=values)
            with open('network.png', 'wb') as f:
                f.write(r.content)

    def test_asynchronous(self):
        
        # Asynchronous request
        # Launching the rendering as asynchronous, and getting the id to check its status/requesting the renderer image
        with open('Reaction_Species.xml','rb') as sbgn_file:
            files = {'file': sbgn_file}
            values = {'async': True}

            r = requests.post("http://localhost:8082/render", files=files, data=values)
            result = r.json()

            # Checking it's status to see if it's rendered
            finished = False
            while not finished:
                r = requests.get("http://localhost:8082/status/%s" % result['id'])
                t_result = r.json()
                finished = (t_result['status'] == 'ready')
                time.sleep(1)
                
            # Then requesting the renderered image
            r = requests.get("http://localhost:8082/rendered/%s" % result['id'])
            with open('network_async.png', 'wb') as f:
                f.write(r.content)
