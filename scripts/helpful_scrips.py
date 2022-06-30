from brownie import accounts, network, config, VRFConsumerV2, Contract, interface, web3
# from Web3 import web3
import time

LOCAL_BLOCKCHAIN_ENVIRONMENTS = [
    "development",
    "ganache",
    "hardhat",
    "local-ganache",
    "mainnet-fork",
]
Opensea_URL = "https://testnets.opensea.io/assets/{}/{}"


def deploy_vrf_consumer():
    subscriptionId = 5666
    vrfCoordinator_address = '0x6168499c0cFfCaCD319c818142124B7A15E857ab'
    link = '0x01BE23585060835E02B77ef475b0Cc51aA1e0709'
    keyHash = '0xd89b2bf150e3b9e13446986e571fb9cab24b13cea0a43ea20a6049a85cc807cc'
    account = get_account()
    vrf_consumer = VRFConsumerV2.deploy(
        subscriptionId, vrfCoordinator_address, link, keyHash, {"from": account}, publish_source=True)
    print("VRF Consumer created...")
    print(vrf_consumer.address)
    # We need an vrf_coordinator contract
    vrfCoordinator_contract = interface.VRFCoordinatorV2Interface(
        vrfCoordinator_address)
    # subscription_details = vrfCoordinator_contract.getSubscription(
    #    subscriptionId)
    # print(subscription_details)
    tx = vrfCoordinator_contract.addConsumer.transact(
        subscriptionId, vrf_consumer.address, {"from": account}
    )
    tx.wait(1)

    print("Consumer added to subscription!")
    # tx = vrf_consumer.requestRandomWords({"from": account})
    # tx.wait(1)
    return vrf_consumer


SONG_MAPPING = {0: "Color_and_Scilense", 1: "Meltdown", 2: "Farnah"}


def get_song(id):
    return SONG_MAPPING[id]


def attach_vrf_cousumer():
    vrf_abi = VRFConsumerV2.abi
    vrf_address = "0xc4C97376EAdA508764d194F33d153D4971eC2C15"
    vrf_contract = Contract.from_abi("VRFConsumerV2", vrf_address, vrf_abi)
    print("VRF consumer attached!")

    return vrf_contract


def get_random_number(vrf_consumer):
    account = get_account()
    tx_rnd = vrf_consumer.requestRandomWords({"from": account})
    tx_rnd.wait(1)
    account = get_account()
    poll_interval = 2
    timeout = 200
    web3_contract = web3.eth.contract(
        address=vrf_consumer.address, abi=vrf_consumer.abi
    )
    start_time = time.time()
    current_time = time.time()
    event_filter = web3_contract.events["ReturnedRandomness"].createFilter(
        fromBlock="latest")
    while current_time - start_time < timeout:
        for event_response in event_filter.get_new_entries():
            if "ReturnedRandomness" in event_response.event:
                print("Found event!")
                rand = vrf_consumer.s_randomWords(0)
                # print(rand)
                return rand
        time.sleep(poll_interval)
        current_time = time.time()
    print("Timeout reached, no event found.")
    return {"event": None}


def get_account(index=None, id=None):
    # network.gas_limit(100000000000)
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if id:
        return accounts.load(id)
    if network.show_active() in config["networks"]:
        return accounts.add(config["wallets"]["from_key"])
    return None
