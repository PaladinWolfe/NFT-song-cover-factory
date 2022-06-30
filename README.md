**General description**

This project uses Brownie framework to deploy NFT smart contract, generate random cover of song tokens from predefined enumeration (Meltdown, Farnag and Color_and_Scilense) and sets metadata to tokens.
To utilize this project you need a testnet Rinkeby wallet with some ETH.

**Contracts description:**

*NFTSongCoverFactory.sol*/
This contract inharits standart NFT contract ERC721. It can create cottectibles for music release of 3 songs:     Color_and_Scilense, Meltdown and Farnah. Token instance is created by createCollectible function with random number and token URI arguments. Function setTokenURI allows to set token URI with metadata.

**Scripts description**

Run scripts in following sequence:/
*deploy_NFT_song_contract.py*
- deploy NFT contract with verified code

*create_collectible.py*
- deploy new VRF coordinator or attach to existing VRF coordinator
- generate random number
- create numberOfTokens tokens of random song type

*create_metadata.py*
- upload image from /img folder to Piniata according to song type
- generate *.JSON file with metadata for each token in NFT contract with link to image
- upload metadata file to Piniata
- set URI to each created token in NFTSongFactory contract

*upload_to_pinata.py*
- upload file to Piniata and return file URI

*Service*

*helpful_scrips.py*
- deploy new VRF consumer
- attach to existing VRF consumer
- generate random number

*fund_link_token.py*

You can fund VRF subscription with some test LINK if necessary


**.env structure**\
export WEB3_INFURA_PROJECT_ID = ''\
export PRIVATE_KEY = ''\
export ETHERSCAN_TOKEN = ''\
export PINATA_API_KEY = ''\
export PINATA_API_SECRET = ''