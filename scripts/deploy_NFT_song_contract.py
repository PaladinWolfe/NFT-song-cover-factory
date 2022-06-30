from brownie import NFTSongCoverFactory
from scripts.helpful_scrips import get_account


def deploy_collectible():
    account = get_account()
    nft_contract = NFTSongCoverFactory.deploy(
        {"from": account}, publish_source=True)


def main():
    deploy_collectible()
