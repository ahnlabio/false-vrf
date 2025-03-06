// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

contract SimpleLottery {
    address public owner;
    uint256[] public randomNumbers;
    
    event RandomNumbersGenerated(uint256[] numbers, address caller, uint256 count);
    
    constructor() {
        owner = msg.sender;
        // Initialize with some default random numbers in case generateRandomNumbers fails
        randomNumbers = new uint256[](5);
        for (uint256 i = 0; i < 5; i++) {
            randomNumbers[i] = uint256(keccak256(abi.encode(block.timestamp, i)));
        }
    }
    
    modifier onlyOwner() {
        require(msg.sender == owner, "Not the contract owner");
        _;
    }
    
    // Generate random numbers based on the seed and count
    // Anyone can call this function
    function generateRandomNumbers(uint256 seed, uint256 count) external {
        require(count > 0, "Count must be greater than zero");
        require(count <= 100, "Count cannot exceed 100 for gas limit reasons");
        
        // Generate count pseudo-random numbers based on the seed
        // This is NOT secure for production use, just for demonstration
        delete randomNumbers; // Clear existing numbers
        randomNumbers = new uint256[](count);
        for (uint256 i = 0; i < count; i++) {
            // Removed msg.sender to ensure same results regardless of caller
            randomNumbers[i] = uint256(keccak256(abi.encode(seed, i)));
        }
        
        emit RandomNumbersGenerated(randomNumbers, msg.sender, count);
    }
    
    // Get the random numbers
    function getRandomNumbers() external view returns (uint256[] memory) {
        return randomNumbers;
    }
} 