import traceback

import brownie.project as project
from brownie import chain, network, accounts


class Blockchain:
    def __init__(self):
        try:
            blockchain_project = project.load('./storages/token/', name='BlockchainProject')
            blockchain_project.load_config()
            network.connect('development')
            self.contract = blockchain_project.DocFlow.deploy({'from': accounts[0]})
        except Exception as e:
            blockchain_project = project.get_loaded_projects()[0]
            self.contract = blockchain_project.DocFlow._contracts[0]


    def get_transactions_list(self):
        txs = []
        for i in range(0, chain.height + 1):
            if len(chain[i]['transactions']) > 0:
                txs.append(chain[i]['transactions'][0].hex())

        print(f'txs: {txs}')
        return txs

    def match_txs_uri(self):
        txs = self.get_transactions_list()
        uri_list = []

        for i in range(0, len(txs)):
            try:
                uri = self.contract.tokenURI(i)
                uri_list.append({
                    'tx': txs[i],
                    'uri': uri
                })
            except Exception as e:
                print(traceback.print_exc())

        print(f'uri_list: {uri_list}')
        return uri_list

    def add(self, uri):
        print(self.contract.add(accounts[1], uri))
