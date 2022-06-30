// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
//import "@chainlink/contracts/src/VRFConsumerBase.sol";
import "./VRFConsumerV2.sol";

contract AdvancedCollectible is ERC721, VRFConsumerV2 {
    using Strings for uint256;
    uint32 public tokenCounter;
    bytes32 public keyhash;
    uint256 public fee;
    VRFConsumerV2 public vrfconsumer;
    uint64 subscriptionId = 5666;
    address vrfCoordinator = 0x6168499c0cFfCaCD319c818142124B7A15E857ab;
    address link = 0x01BE23585060835E02B77ef475b0Cc51aA1e0709;
    bytes32 keyHash =
        0xd89b2bf150e3b9e13446986e571fb9cab24b13cea0a43ea20a6049a85cc807cc;

    enum Breed {
        Color,
        Melt,
        Farn
    }
    mapping(uint256 => Breed) public tokenIdToBreed;
    mapping(uint256 => address) public requestIdToSender;
    mapping(uint256 => string) private _tokenURIs;
    // emit event after mapping update
    event requestedCollectible(uint256 indexed requestId, address requested);
    event breedAssigned(uint256 indexed requestId, Breed breed);

    constructor() public ERC721("Khazaar", "KHZR") {
        tokenCounter = 0;
        vrfconsumer = VRFConsumerV2(
            subscriptionId,
            vrfCoordinator,
            link,
            keyHash
        );
    }

    function _setTokenURI(uint256 tokenId, string memory _tokenURI)
        internal
        virtual
    {
        require(
            _exists(tokenId),
            "ERC721Metadata: URI set of nonexistent token"
        );

        require(_isApprovedOrOwner(_msgSender(), tokenId));
        _tokenURIs[tokenId] = _tokenURI;
    }

    // Base URI
    string private _baseURIextended;

    function setBaseURI(string memory baseURI_) external {
        _baseURIextended = baseURI_;
    }

    function _baseURI() internal view virtual override returns (string memory) {
        return _baseURIextended;
    }

    function tokenURI(uint256 tokenId)
        public
        view
        virtual
        override
        returns (string memory)
    {
        require(
            _exists(tokenId),
            "ERC721Metadata: URI query for nonexistent token"
        );

        string memory _tokenURI = _tokenURIs[tokenId];
        string memory base = _baseURI();

        // If there is no base URI, return the token URI.
        if (bytes(base).length == 0) {
            return _tokenURI;
        }
        // If both are set, concatenate the baseURI and tokenURI (via abi.encodePacked).
        if (bytes(_tokenURI).length > 0) {
            return string(abi.encodePacked(base, _tokenURI));
        }
        // If there is a baseURI but no tokenURI, concatenate the tokenID to the baseURI.
        return string(abi.encodePacked(base, tokenId.toString()));
    }

    function createCollectible(string memory tokenURI_) public {
        uint256 requestId;
        requestId = requestRandomWords();
        requestIdToSender[requestId] = msg.sender;
        emit requestedCollectible(requestId, msg.sender);
    }

    //function fulfillRandomWords() internal override {

    //}
    function fulfillRandomWords(
        uint256 requestId,
        uint256[] memory randomNumber
    ) internal override {
        Breed breed = Breed(randomNumber[0] % 3);
        uint256 newTokenId = tokenCounter;
        tokenIdToBreed[newTokenId] = breed;
        emit breedAssigned(newTokenId, breed);
        address owner = requestIdToSender[requestId];
        _safeMint(owner, newTokenId);
        tokenCounter = tokenCounter + 1;
    }
}
