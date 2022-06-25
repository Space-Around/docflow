import brownie.project as project
from brownie import chain, network, accounts
import requests, json


def deploy_contract():
    blockchain_project = project.load('./storages/token/', name="BlockhainProject")
    blockchain_project.load_config()
    network.connect('development')

    return blockchain_project.DocFlow.deploy({'from': accounts[0]})


def get_transactions_list():
    txs = []
    for i in range(0, chain.height + 1):
        if len(chain[i]['transactions']) > 0:
            txs.append(chain[i]['transactions'][0].hex())
    return txs


def match_txs_uri(contract):
    txs = get_transactions_list()
    uri_list = []

    for i in range(0, len(txs)):
        uri = contract.tokenURI(i)
        uri_list.append({
            'tx': txs[i],
            'uri': uri
        })

    return uri_list


def get_info_by_uri(uri):
    data = None

    try:
        response = requests.get(uri)
        data = json.loads(response.text)
    except Exception as e:
        pass

    return data


def get_extended_info():
    info_list = match_txs_uri()
    extended_info = info_list

    for info in info_list:
        extended_info['info'] = get_info_by_uri(info['uri'])

    return extended_info