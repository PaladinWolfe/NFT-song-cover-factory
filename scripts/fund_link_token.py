from scripts.helpful_scrips import get_account
from brownie import NFTSongCoverFactory, Contract, interface, convert


def main():
    nft_contract = NFTSongCoverFactory[-1]
    vrfCoordinator_address = '0x6168499c0cFfCaCD319c818142124B7A15E857ab'
    link_token_address = '0x01BE23585060835E02B77ef475b0Cc51aA1e0709'
    link_token_contract = Contract.from_abi(
        "LinkToken", link_token_address, interface.LinkTokenInterface.abi)
    account = get_account()
    fund_amount = 0.1 * 1000000000000000000
    subscriptionId = 5666
    # funding_tx = link_token_contract.transfer(
    #     nft_contract.address, amount, {"from": account})
    vrfCoordinator_contract = interface.VRFCoordinatorV2Interface(
        vrfCoordinator_address)

    funding_tx = link_token_contract.transferAndCall(
        vrfCoordinator_address,
        fund_amount,
        convert.to_bytes(subscriptionId),
        {"from": account},
    )
    funding_tx.wait(1)
    print(f"Funded {nft_contract.address}")
