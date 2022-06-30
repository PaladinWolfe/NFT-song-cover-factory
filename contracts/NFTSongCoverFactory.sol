// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "./VRFConsumerV2.sol";

contract NFTSongCoverFactory is ERC721 {
    using Strings for uint256;
    uint32 public tokenCounter;
    bytes32 public keyhash;
    uint256 public fee;
    enum Song {
        Color_and_Scilense,
        Meltdown,
        Farnah
    }
    mapping(uint256 => Song) public tokenIdToSong;
    mapping(uint256 => address) public requestIdToSender;
    mapping(uint256 => string) private _tokenURIs;
    // emit event after mapping update
    event requestedCollectible(uint256 indexed requestId, address requested);
    event songAssigned(uint256 indexed requestId, Song song);
    address owner;

    constructor() public ERC721("Khazaar", "KHZR") {
        tokenCounter = 0;
        owner = msg.sender;
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI)
        external
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

    function createCollectible(uint256 randomNumber, string memory tokenURI_)
        public
    {
        Song song = Song(randomNumber % 3);
        uint256 newTokenId = tokenCounter;
        tokenIdToSong[newTokenId] = song;
        emit songAssigned(newTokenId, song);
        //address owner = requestIdToSender[requestId];
        _safeMint(owner, newTokenId);
        tokenCounter = tokenCounter + 1;
    }

    //function fulfillRandomWords() internal override {

    //}
    function createToken() public {}
}
