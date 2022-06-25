# import ipfsapi
# api = ipfsapi.connect('127.0.0.1', 8080)
import ipfshttpclient
client = ipfshttpclient.connect('/dns/127.0.0.1/tcp/5001/http')