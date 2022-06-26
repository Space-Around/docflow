import json
import config
import ipfshttpclient


class IPFS:
    @classmethod
    def add(cls, data):
        json_data = json.dumps(data)

        with ipfshttpclient.connect(config.IPFS_ADRR) as client:
            return client.add_json(json_data)

    @classmethod
    def cat(cls, hash):
        with ipfshttpclient.connect(config.IPFS_ADRR) as client:
            client.cat(hash)