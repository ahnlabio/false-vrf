# 🎲 False VRF - Transparent Pseudo-Random Lottery on Blockchain
A smart contract and Python script utilizing pseudo-random number generation to fairly select winners from a pool of participants. The number of random numbers and winners can be customized by the user.

## 🎯 Preview
```plaintext
🔑 Using account: 0x33bf89ac0576BB926Aa930323bCC6b59fb828102
💰 Account balance: 2.172671625 KAIA
👥 Loaded 39 participants from participants.txt
Do you want to deploy a new contract? (y/N) (default: N): y
📄 Compiling contract...
🚀 Deploying contract...
⏳ Waiting for transaction 0xe1aacc9fb1eafb69c8bd0c3bf3c25ef409aa3f8efc13d5aa37795b46ab593808 to be mined...
✅ Contract deployed at: 0x36F7d2C7a78310F18D7d323B29D3e546201B4074
⏳ Waiting 10 seconds for the contract to be fully deployed...
Enter the number of winners to select (max: 39) (default: 20): 
Do you want to generate new random numbers? (y/N) (default: N): y
Enter a custom seed (default: 1741251744): 
🎲 Generating random numbers...
Using seed: 1741251744
Generating 20 random numbers
⏳ Waiting for transaction 0xd77ee4f6aef85c02f3b5634fa0ee3574a3a8a80ea047651e2d743e7e5eca67d2 to be mined...
Transaction was successful
✅ Random numbers generated successfully!
⏳ Waiting 10 seconds for the random numbers to be generated...
🔍 Getting random numbers...
✅ Random numbers received: [23959960709822575028829945558139379771414400391176049451337761515280757182103, 55591727595253910201147905451893129822388687478976247621040078033528256872067, 34402083271013339371509171286711798136784693851620534894189774123119728836578, 39214867064043950394819540768719572682590080277190849205683562874933257083750, 82830546322517185270212891637252749939310956268925971407320260505694009683087, 109513008148546751360088397035914750903123622805658890384866902411002282068558, 25055228348703521598420027933017593324616419260630794599529333972683682347789, 53247800669329708223982835196458611313299924891221669193231989556536352812455, 55087087394660666157887333559957248958838383143613389578601753561279571973004, 74694770516135962622489098859519906592579555262453705280229387355413891577005, 5544840770427018105939842873217994480910164021651146054224279230812213177166, 22111774883914338318814770214088074525953716087924179609123776286233741179889, 2257899528950699093334179125589381436233756402527374766195223588558845305641, 76428991881079630561696048231148299149772292642168426263451444300736166831197, 68540357468200980153638803750946681644294545020266945840250473169762191684365, 82085791472935704737915351037289075036617894895093982588227902319218376735881, 6217750190138994543495006248157012978907049178668858696944730610872082554126, 57492432962403278209663054092041310489657651122676739997854749567942934205194, 78330930400239961909806467598494015194089969768467157520327369713940262143591, 1463729842414765798047584242928182756701509661628552783949787182702150104658]
Number of random numbers: 20
🔍 Trying winner index: 0
✅ Selected winner: Bob
🔍 Trying winner index: 20
✅ Selected winner: Alice
🔍 Trying winner index: 27
🔍 Modified random value: 44695302811237950703790405104255522877374341086773656327321363557075553381592
🔍 Trying winner index: 4
✅ Selected winner: Charlie
🔍 Trying winner index: 7
✅ Selected winner: Tyanne
🔍 Trying winner index: 27
🔍 Modified random value: 55868895016254007297450042765769153130858339811733206839693923705212376058694
🔍 Trying winner index: 16
🔍 Modified random value: 31543099787404922325424645902871543581538509558688304679275504120282110923419
🔍 Trying winner index: 8
✅ Selected winner: Mickey
🔍 Trying winner index: 8
🔍 Modified random value: 2935269387635908
...
🏆 Selected 20 winners:
  1. Bob
  2. Alice
  ...
  15. Charlie
✅ Winners saved to report.md for verification
✨ Lottery completed!
```


## 📚 Background

### Why Not a True VRF?

Verifiable Random Functions (VRFs) are the gold standard for generating provably fair random numbers on blockchain. External VRF Solutions provide cryptographically secure randomness that is:
- Unpredictable (cannot be known in advance)
- Unbiased (cannot be manipulated by any party)
- Verifiable (can be proven to be generated correctly)

However, implementing a true VRF comes with challenges:
- Requires integration with specialized oracle networks
- Often involves subscription fees or token requirements
- Adds complexity to smart contract development
- May be overkill for small-scale or educational projects

### Our Approach

This project offers a simpler alternative that prioritizes:
- **Transparency**: All random number generation happens on-chain and is visible to everyone
- **Reproducibility**: Anyone can verify the results by using the same seed
- **Simplicity**: No external dependencies or complex cryptographic proofs
- **Educational value**: Easy to understand how randomness is generated and used

While **not suitable** for **high-stakes applications**, this approach is perfect for community giveaways, educational demonstrations, and low-value lotteries where complete unpredictability is less critical than transparency and ease of verification.


## 🚀 Features
- **Interactive CLI** for deployment and verification for lottery.
- Uses **pseudo-random number generation**.
- Secure **.env-based private key management**.
- Option to **deploy** a new contract **or reuse** an existing one.
- **Anyone** can **generate** random numbers on the contract.
- **Same random numbers for the same seed** regardless of caller.
- **Variable number of random numbers and winners** can be specified by the user.
- **Loads participants from a text file**.
- **Supports multiple identifier formats** including names, addresses, or any text.
- **Saves detailed report** with complete verification information.
- **Custom seed input** or automatic timestamp-based seed.
- **Compatible on any EVM-compatible chains**. 


## 📌 Prerequisites
For the sake of simplicity and accessibility, we're using [KAIA Kairos Testnet](https://kairos.kaiascan.io) in this document. However, you may use different any other EVM-compatible chains.

- Python **>=3.10**
- Private key of Wallet
- **Native** funds in the wallet. You can get from [Kaia Kairos Faucet](https://www.kaia.io/faucet)

---
## 🔧 Setup & Run

#### 1️⃣ Install Dependencies
Install [Poetry](https://python-poetry.org/docs/#installation) if you don't have it. 
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

#### 2️⃣ Clone the Repo
```bash
git clone https://github.com/ahnlabio/false-vrf.git && cd false-vrf
```

#### 3️⃣ Install dependencies
```bash
poetry install
```

#### 4️⃣ Create `.env` File
Please create **`.env`** file to store `PRIVATE_KEY`. This is required to deploy and execute smartcontract. 
```plaintext
PRIVATE_KEY=your_wallet_private_key
```

#### 5️⃣ Create `participants.txt` Files
You must create **`participants.txt`** file with Participant's identifiers (eg. name, uuid, etc).
The script will first try to load participants from `participants.txt`. If the file doesn't exist, the script will exit with an error.

```plaintext
Alice
Bob
...
Zetta
```

#### 6️⃣ Run the Script
```bash
poetry run python lottery.py
```
---
## 🔍 Verify

The lottery results can be verified using the following steps:

#### 1️⃣ Check the Report File
The `report.md` file contains all the information needed for verification:
```
# LOTTERY VERIFICATION INFORMATION
- 📆 Date: 2023-06-15 14:30:45
- 🌐 Network: Kaia Kairos Testnet
- 🔗 RPC URL: https://public-en-kairos.node.kaia.io
- 🔗 Chain ID: 1001
- 📄 Contract Address: 0x36F7d2C7a78310F18D7d323B29D3e546201B4074
- 🔑 Seed: 12345

## RESULTS
- 🎲 Random Numbers (Total: 39): [34782109024670728339275626588312815753907165073157573742582851640136195104572, ...]
- 📄 Total Participants: 39
- 🎉 Number of Winners: 15

## VERIFICATION MAPPING
| # | Random Number | Index (mod 39) | Winner |
|---|---------------|----------------|--------|
| 1 | 3478210...    | 24             | Alice  |
...

# WINNERS
1. Bob
2. Alice
...
```

This file includes all the information needed to reproduce and verify the lottery results:
- Network details (name, RPC URL, chain ID)
- Contract address
- Seed used for random number generation
- Complete list of random numbers generated
- Total number of participants and winners

#### 2️⃣ Check the Smart Contract
The deployed smart contract address is saved in `contract_address.txt`. You can verify the contract on the Kaia Network explorer:
```
https://kairos.kaiascan.io/address/YOUR_CONTRACT_ADDRESS
```

#### 3️⃣ Verify Random Numbers
The random numbers are generated on-chain using given seed (default: timestamp). You can verify them by:
1. Calling the `getRandomNumbers()` function on the deployed contract
2. Checking the transaction that called `generateRandomNumbers(seed)`

**Note:** The contract will produce the same random numbers for the same seed value, regardless of which wallet calls the function. This makes verification easier as anyone can reproduce the exact same random numbers by using the same seed.

#### 4️⃣ Verify Winner Selection
The winners are selected using the following algorithm:
1. Each random number is used to select a winner: `winner_index = random_number % total_addresses`
2. The script avoids duplicate winners by tracking used indices
3. The mapping of this indices is in the section `VERIFICATION MAPPING` in  `report.md`

You can manually verify that:
- Each winner is from the original address list
- The selection follows the algorithm above
- No winner appears twice in the list

#### 5️⃣ Cross-check with Transaction Data
All transactions are recorded on the blockchain. You can verify:
- Contract deployment transaction
- Random number generation transaction
- The timestamp used as the seed


## 🛠 How It Works
1. **Deploys Smart Contract** to Kaia Network (or uses an existing one).
2. **Generates random numbers** on-chain (optional if using existing contract).
   - User can specify how many random numbers to generate (default: 20).
   - User can provide a custom seed or use the current timestamp.
3. **Retrieves the random numbers** from the contract.
4. **Loads participants** from `participants.txt`.
5. **Randomly selects winners** from the pool of participants.
   - User can specify how many winners to select (default: 20).
6. **Saves detailed report** for verification to `report.md`.
7. **Prints the winners**.


## 📜 Smart Contract Overview
The Smart Contract is located in `/contracts/SimpleLottery.sol`
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

contract SimpleLottery {
    // Anyone can call this function
    function generateRandomNumbers(uint256 seed, uint256 count) external;
    function getRandomNumbers() external view returns (uint256[] memory);
}
```
- **Deploys the SimpleLottery contract**.
- **Anyone can generate random numbers** based on a seed and count.
- **Retrieves the generated random numbers**.


## 🔢 Understanding the Randomness

### How This Differs From True VRF

| Feature | False VRF (This Implementation) | True VRF (e.g., Chainlink) |
|---------|:--------------------:|:-----------------------------:|
| **Unpredictability** | Limited <br>_Anyone who knows the seed can predict the outcome_ | **High** <br>_Random numbers cannot be predicted in advance_ |
| **Manipulation Resistance** | Medium <br>_On-chain but potentially influenced by miners_ | **High** <br>_External randomness sources prevent manipulation_ |
| **Verification** | Simple - Anyone can reproduce with the same seed | **Cryptographic** - Includes mathematical proof of fairness |
| **Cost** | Low - Standard transaction fees only | **Higher** - Requires oracle fees/subscriptions |
| **Complexity** | Low _Simple implementation_ | **Higher** _Requires integration with oracle networks_ |
| **Transparency** | **High**<br> _Fully visible on-chain_ | Medium<br> _Depends on trust in the oracle network_ |

### Mathematical Properties

The randomness in this lottery system is based on Keccak-256 (SHA-3) cryptographic hash function, which has the following properties:

1. **Deterministic**: The same input always produces the same output, allowing for verification.
2. **Uniform Distribution**: The output bits are uniformly distributed, meaning each bit has an equal probability of being 0 or 1.
3. **Avalanche Effect**: A small change in the input produces a completely different output.
4. **Pre-image Resistance**: Given an output, it's computationally infeasible to find an input that produces that output.

### Randomness Generation Process

The random numbers are generated using the following formula:
```solidity
randomNumbers[i] = uint256(keccak256(abi.encode(seed, i)));
```

Where:
- `seed` is either a user-provided value or the current timestamp
- `i` is the index of the random number (0 to count-1)

This approach ensures:
1. **Reproducibility**: Anyone with the same seed can generate the same random numbers
2. **Fairness**: Each number has an equal probability of being selected
3. **Transparency**: The entire process can be verified on-chain

### Statistical Properties

The random numbers generated have a uniform distribution across the entire uint256 range (0 to 2^256-1). When used to select winners (by taking modulo with the number of addresses), this provides a fair selection process where each address has an equal probability of being selected.

## ⚠️ Disclaimers

### Not a True VRF

This implementation should not be confused with a true Verifiable Random Function (VRF) as used in production blockchain applications:

1. **Predictability**: If the seed is known in advance, the outcome can be predicted.
2. **No Cryptographic Proofs**: Unlike true VRFs, this implementation doesn't provide cryptographic proofs of correct generation.
3. **Potential for Manipulation**: In theory, miners or validators could influence the outcome if using block-related values as seeds.

### Security Considerations

1. **Not Cryptographically Secure for High-Value Applications**: 
   - This implementation uses pseudo-random number generation that is deterministic and predictable if the seed is known.
   - It is NOT suitable for high-value applications where true unpredictability is required.
   - Miners or validators could potentially manipulate block timestamps if they have sufficient incentive.

2. **Seed Visibility**:
   - The seed used for random number generation is visible on the blockchain.
   - Anyone can see the seed and reproduce the random numbers.

3. **Gas Limitations**:
   - The contract limits the number of random numbers to 100 to prevent excessive gas consumption.
   - Attempting to generate more numbers may result in transaction failure.

### Recommended Use Cases

This lottery system is suitable for:
- Community giveaways
- Low-stakes raffles
- Transparent selection processes
- Educational purposes

It is NOT recommended for:
- High-value lotteries
- Gambling applications
- Security-critical random number generation
- Applications requiring unpredictable outcomes

### Legal Considerations

Before using this system for any lottery or raffle:
1. Ensure compliance with local laws and regulations regarding lotteries and raffles
2. Consider whether a license is required in your jurisdiction
3. Be transparent with participants about how winners are selected


### Author and Liability Disclaimer

This code was created as an educational and demonstration tool.

**NO WARRANTY OR SUPPORT:**
- This code is provided "AS IS" without warranty of any kind, express or implied.
- The authors and contributors do not provide maintenance or support for this code.
- No guarantee is made regarding the functionality, security, or reliability of this implementation.

**LIABILITY WAIVER:**
- By using this code, you agree that the authors and contributors are not liable for any direct, indirect, incidental, special, exemplary, or consequential damages.
- This includes, but is not limited to: loss of profits, data, or funds; business interruption; or any other commercial or financial losses.
- Users assume all risks associated with the use of this code in any environment.

**USAGE RESPONSIBILITY:**
- It is the user's responsibility to thoroughly test and verify the code before using it in any production environment.
- Users should conduct their own security audits and risk assessments before implementation.
  

## 📜 License
MIT License © 2025

