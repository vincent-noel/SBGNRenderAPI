import requests, json, time

# Synchronous request example

files = {'file': open('Reaction_Species.xml','rb')}
values = {}

r = requests.post("http://localhost:8082/render", files=files, data=values)
with open('network.png', 'wb') as f:
    f.write(r.content)


# Asynchronous request example

# Launching the rendering as asynchronous, and getting the id to check its status/requesting the renderer image
files = {'file': open('Reaction_Species.xml','rb')}
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
