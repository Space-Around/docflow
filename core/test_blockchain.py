import brownie.project as project
from brownie import chain, network, accounts, history


blockchain_project = project.load('./storages/token/', name="BlockhainProject")
blockchain_project.load_config()
network.connect('development')

# print(dir(dict(blockchain_project)['DocFlow']))

# import brownie.project.BlockhainProject as bp
# print(bp == blockchain_project)
# from brownie.project.BlockhainProject import *

# blockchain_project.DocFlow.network.connect('development')
# print(dict(blockchain_project))
df = blockchain_project.DocFlow.deploy({'from': accounts[0]})
df.add(accounts[1], 'https://0.0.0.0:8080/data/doc1.json')

# print(chain[12])
# print(history.copy())

