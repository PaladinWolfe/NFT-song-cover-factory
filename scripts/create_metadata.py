from brownie import NFTSongCoverFactory, network
from scripts.helpful_scrips import get_account, Opensea_URL, get_song
from scripts.upload_to_pinata import main_upload_to_pinata
from metadata.sample_metadata import metadata_template
from pathlib import Path
import json

KEY_MAPPING = {0: "12d", 1: "10m", 2: "11d"}


def main():
    account = get_account()
    nft_contract = NFTSongCoverFactory[-1]  # Contract.from_abi(
    # "NFTSongFactory", "0x291F87e8EDde80468c288609E1f16bb4fAc7Abf5", NFTSongFactory.abi)
    numberOfTokens = nft_contract.tokenCounter()
    print(f"You've created {numberOfTokens} collectibles")
    for token_id in range(numberOfTokens):
        song = get_song(nft_contract.tokenIdToSong(token_id))
        key = KEY_MAPPING[nft_contract.tokenIdToSong(token_id)]
        metadata_file_path = (
            f"./metadata/{network.show_active()}/{token_id}-{song}.json")
        print(metadata_file_path)
        collectible_metadata = metadata_template
        if Path(metadata_file_path).exists():
            print(f"{metadata_file_path} already exists")
        else:
            print(f"Creating metadata file {metadata_file_path}")
            collectible_metadata["name"] = song
            collectible_metadata["description"] = f"Nice song {song}"
            image_file_path = "./img/"+f"{song}" + ".jpg"
            image_uri = main_upload_to_pinata(image_file_path)
            collectible_metadata["image"] = image_uri
            #collectible_metadata["attributes"]["trait_type"]["value"] = key
            print(collectible_metadata)
            with open(metadata_file_path, "w") as file:
                json.dump(collectible_metadata, file)
            metadata_uri = main_upload_to_pinata(metadata_file_path)
            # print(metadata_uri)
            setTokenURI(token_id, metadata_uri)
            print(
                f"You can view your NFT at {Opensea_URL.format(nft_contract.address, token_id)}")


def setTokenURI(token_id, token_URI):
    account = get_account()
    nft_contract = NFTSongCoverFactory[-1]  # Contract.from_abi(
    # "NFTSongFactory", "0x291F87e8EDde80468c288609E1f16bb4fAc7Abf5", NFTSongFactory.abi)
    tx = nft_contract.setTokenURI(
        token_id, token_URI, {"from": account})
