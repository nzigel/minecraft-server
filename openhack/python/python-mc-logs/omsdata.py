import yaml
import os
import json
import requests
import datetime
import hashlib
import hmac
import base64
from mcstatus import MinecraftServer

"""
Create a file config.yml in the python folder containing your keys

credentials:
    workspace_id:
    workspace_key: 
    minecraft_server:
    minecraft_port:
    log_type:
"""

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"config.yml"), 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

credentials = cfg['credentials']
# Update the customer ID to your Log Analytics workspace ID
customer_id = credentials['workspace_id']
# For the shared key, use either the primary or the secondary Connected Sources client authentication key   
shared_key = credentials['workspace_key']

# The log type is the name of the event that is being submitted
log_type = credentials['log_type']

def get_body():
    server = MinecraftServer.lookup("{}:{}".format(credentials['minecraft_server'],credentials['minecraft_port']))

    # 'status' is supported by all Minecraft servers that are version 1.7 or higher.
    status = server.status()
    #print("The server has {0} players and replied in {1} ms".format(status.players.online, status.latency))

    # https://mcapi.us/server/status?ip=13.75.217.120&port=25565
    json_data = [{
        "status": "success",
        "online": True,
        "motd": status.description['text'],
        "latency": status.latency,
        "maxplayers": status.players.max,
        "activeplayers": status.players.online,
        "servername": status.version.name
    }]
    return json.dumps(json_data)

# Build the API signature
def build_signature(customer_id, shared_key, date, content_length, method, content_type, resource):
    x_headers = 'x-ms-date:' + date
    string_to_hash = method + "\n" + str(content_length) + "\n" + content_type + "\n" + x_headers + "\n" + resource
    bytes_to_hash = bytes(string_to_hash,"utf-8") 
    decoded_key = base64.b64decode(shared_key)
    encoded_hash = base64.b64encode(hmac.new(decoded_key, bytes_to_hash, digestmod=hashlib.sha256).digest())
    authorization = "SharedKey {}:{}".format(customer_id,encoded_hash.decode('utf-8'))
    return authorization

# Build and send a request to the POST API
def post_data(customer_id, shared_key, log_type):
    body = get_body()

    method = 'POST'
    content_type = 'application/json'
    resource = '/api/logs'
    rfc1123date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    content_length = len(body)
    signature = build_signature(customer_id, shared_key, rfc1123date, content_length, method, content_type, resource)
    uri = 'https://' + customer_id + '.ods.opinsights.azure.com' + resource + '?api-version=2016-04-01'

    headers = {
        'content-type': content_type,
        'Authorization': signature,
        'Log-Type': log_type,
        'x-ms-date': rfc1123date
    }
    
    response = requests.post(uri,data=body, headers=headers)
    if (response.status_code >= 200 and response.status_code <= 299):
        print("Accepted {}".format(rfc1123date))
    else:
        print("Response code: {}".format(response.status_code))

import sched, time
s = sched.scheduler(time.time, time.sleep)
def do_something(sc): 
    post_data(customer_id, shared_key, log_type) 
    s.enter(60, 1, do_something, (sc,))

s.enter(60, 1, do_something, (s,))
s.run()