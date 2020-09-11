import requests

files = {'file': open('Reaction_Species.xml','rb')}
values = {}

r = requests.post("http://localhost:8082/render", files=files, data=values)
with open('network.png', 'wb') as f:
    f.write(r.content)
