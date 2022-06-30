from ast import For
from brownie import NFTSongCoverFactory
from scripts.helpful_scrips import get_account, Opensea_URL, deploy_vrf_consumer, attach_vrf_cousumer, get_random_number


def create_collectible():
    account = get_account()
    nft_contract = NFTSongCoverFactory[-1]  # Contract.from_abi(
    # "NFTSongCoverFactory", "0x4891b6D3FDF297Cc828AB4049e3336B4881750D8", NFTSongFactory.abi)
    # vrf_consumer = deploy_vrf_consumer() #deploy new VRF consumer
    vrf_consumer = attach_vrf_cousumer()  # attach to existing VRF consumer
    rnd = get_random_number(vrf_consumer)
    print("Random number is", rnd)
    tx_create = nft_contract.createCollectible(
        rnd, "", {"from": account})
    tx_create.wait(1)


def main():
    numberOfTokens = 5  # set number of tokens to randomly deploy
    for indexToken in range(numberOfTokens):
        create_collectible()
