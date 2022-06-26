import ipfshttpclient
import json

client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001')

json_data = {
    'hello': 'world',
    'count': 12
}

# res = client.add('test_ipfs.py')

res = client.add_json(json.dumps(json_data))

print(client.cat(res))

# print(res)