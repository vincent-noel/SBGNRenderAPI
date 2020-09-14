import requests

files = {'file': open('Reaction_Species.xml','rb')}
values = {}

r = requests.post("http://localhost:8082/render", files=files, data=values)
with open('network.png', 'wb') as f:
    f.write(r.content)



files = {'file': open('Reaction_Species.xml','rb')}
values = {
    'bg': '#f00'
}

r = requests.post("http://localhost:8082/render", files=files, data=values)
with open('network2.png', 'wb') as f:
    f.write(r.content)


files = {'file': open('Reaction_Species.xml','rb')}
values = {
    'format': 'svg'
}

r = requests.post("http://localhost:8082/render", files=files, data=values)
with open('network.svg', 'wb') as f:
    f.write(r.content)

files = {'file': open('Reaction_Species.xml','rb')}
values = {
    'format': 'jpg',
    'bg': '#00f',
    'scale': 1
}

r = requests.post("http://localhost:8082/render", files=files, data=values)
with open('network.jpg', 'wb') as f:
    f.write(r.content)
