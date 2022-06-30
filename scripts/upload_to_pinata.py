import os
import requests
PINATA_API_KEY = os.getenv("PINATA_API_KEY")
PINATA_API_SECRET = os.getenv("PINATA_API_SECRET")


def main_upload_to_pinata(filepath):
    PINIATA_BASE_URL = "https://api.pinata.cloud/"
    endpoint = "pinning/pinFileToIPFS"
    filename = filepath.split("/")[-1:][0]
    headers = {"pinata_api_key": PINATA_API_KEY,
               "pinata_secret_api_key": PINATA_API_SECRET}
    file_binary = open(filepath, "rb")
    response = requests.post(
        PINIATA_BASE_URL+endpoint, files={"file": (filename, file_binary)}, headers=headers)
    file_uri = "https://gateway.pinata.cloud/ipfs/" + \
        response.json()["IpfsHash"]
    print(file_uri)
    return file_uri
