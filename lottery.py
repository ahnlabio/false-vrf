#! /usr/bin/env python3

import time
import os
import json
from dotenv import load_dotenv
from web3 import Web3
from eth_account import Account
from solcx import compile_files, install_solc

# Install Solidity compiler
install_solc("0.8.7")

# Network configuration
NETWORK = {
    "name": "Kaia Kairos Testnet",
    "rpc_url": "https://public-en-kairos.node.kaia.io",
    "chain_id": 1001,
    "currency_symbol": "KAIA",
    "gas_price": 25,  # in gwei
    "gas_limit": {"deploy": 2000000, "generate_random": 2000000},
    "wait_time": 10,  # seconds to wait between transactions
}

PARTICIPANTS_FILE = "participants.txt"
REPORT_FILE = "report.md"
# Load environment variables
load_dotenv()
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

if not PRIVATE_KEY:
    raise ValueError("❌ PRIVATE_KEY not found in .env file!")

# Web3 setup
web3 = Web3(Web3.HTTPProvider(NETWORK["rpc_url"]))
ACCOUNT = Account.from_key(PRIVATE_KEY)
web3.eth.default_account = ACCOUNT.address

print(f"🔑 Using account: {ACCOUNT.address}")
print(
    f"💰 Account balance: {web3.from_wei(web3.eth.get_balance(ACCOUNT.address), 'ether')} {NETWORK['currency_symbol']}"
)


def get_input(prompt: str, default=None):
    """Get input from the user with a default value"""
    if default:
        prompt = f"{prompt} (default: {default}): "
    else:
        prompt = f"{prompt}: "

    response = input(prompt)
    return response if response.strip() else default


def deploy_contract():
    """Deploy the SimpleLottery contract"""
    print("📄 Compiling contract...")

    compiled_sol = compile_files(["contracts/SimpleLottery.sol"], solc_version="0.8.7")

    contract_id = "contracts/SimpleLottery.sol:SimpleLottery"
    contract_interface = compiled_sol[contract_id]

    # Save ABI for later use
    with open("contract_abi.json", "w") as f:
        json.dump(contract_interface["abi"], f)

    print("🚀 Deploying contract...")
    contract = web3.eth.contract(
        abi=contract_interface["abi"], bytecode=contract_interface["bin"]
    )

    # Build transaction
    nonce = web3.eth.get_transaction_count(ACCOUNT.address)
    transaction = contract.constructor().build_transaction({
        "chainId": NETWORK["chain_id"],
        "gas": NETWORK["gas_limit"]["deploy"],
        "gasPrice": web3.to_wei(NETWORK["gas_price"], "gwei"),
        "nonce": nonce,
    })

    # Sign and send transaction
    signed_txn = web3.eth.account.sign_transaction(transaction, PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

    print(f"⏳ Waiting for transaction {web3.to_hex(tx_hash)} to be mined...")
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    contract_address = tx_receipt.contractAddress
    print(f"✅ Contract deployed at: {contract_address}")

    # Save contract address for later use
    with open("contract_address.txt", "w") as f:
        f.write(contract_address)

    # Return contract instance
    return web3.eth.contract(address=contract_address, abi=contract_interface["abi"])


def generate_random_numbers(
    contract, account_address=None, private_key=None, custom_seed=None, num_random=20
):
    """Generate random numbers in the contract

    This function can be called by anyone, not just the contract owner.
    Args:
        contract: The contract instance.
        account_address: The address of the account to use. If not provided, it uses the default account.
        private_key: The private key of the account to use. If not provided, it uses the private key from the environment variables.
        custom_seed: The seed to use for the random numbers. If not provided, it uses the current timestamp.
        num_random: The number of random numbers to generate. If not provided, it defaults to 20.
    """
    print("🎲 Generating random numbers...")

    # Use default account if not provided
    account_address = account_address or ACCOUNT.address
    private_key = private_key or PRIVATE_KEY

    try:
        # Use custom seed if provided, otherwise use current timestamp
        seed = custom_seed if custom_seed is not None else int(time.time())
        print(f"Using seed: {seed}")
        print(f"Generating {num_random} random numbers")

        # Build transaction
        nonce = web3.eth.get_transaction_count(account_address)
        transaction = contract.functions.generateRandomNumbers(
            seed, num_random
        ).build_transaction({
            "chainId": NETWORK["chain_id"],
            "gas": NETWORK["gas_limit"]["generate_random"],
            "gasPrice": web3.to_wei(NETWORK["gas_price"], "gwei"),
            "nonce": nonce,
            "from": account_address,
        })

        # Sign and send transaction
        signed_txn = web3.eth.account.sign_transaction(transaction, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

        print(f"⏳ Waiting for transaction {web3.to_hex(tx_hash)} to be mined...")
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

        # Check transaction status
        if receipt.status == 1:
            print("Transaction was successful")
        else:
            print("Transaction failed")
            print(f"Transaction receipt: {receipt}")

        print("✅ Random numbers generated successfully!")
        return web3.to_hex(tx_hash)
    except Exception as e:
        print(f"❌ Error generating random numbers: {str(e)}")
        return False


def get_random_numbers(contract):
    """Get random numbers from the contract"""
    print("🔍 Getting random numbers...")

    try:
        random_numbers = contract.functions.getRandomNumbers().call()
        print(f"✅ Random numbers received: {random_numbers}")
        print(f"Number of random numbers: {len(random_numbers)}")

        if len(random_numbers) == 0:
            print("⚠️ Warning: No random numbers were generated!")

        return random_numbers
    except Exception as e:
        print(f"❌ Error getting random numbers: {str(e)}")
        return []


def load_participants_from_file(filename="participants.txt"):
    """Load participants from a text file

    The file should contain one address per line (any format).
    If the file doesn't exist or is empty, try participants.txt.
    """
    try:
        # Try load file
        if os.path.exists(filename):
            with open(filename, "r") as f:
                participants = [line.strip() for line in f if line.strip()]

            if participants:
                print(f"👥 Loaded {len(participants)} participants from {filename}")
                return participants

        # If no files with participants are found, raise an error
        raise FileNotFoundError(
            f"No address files found. Please create {filename} with participants."
        )

    except Exception as e:
        print(f"❌ Error loading participants: {str(e)}")
        exit(1)


def select_winners(random_numbers, participants, num_winners=20):
    """Select winners from the pool of participants using the random numbers"""
    if not random_numbers:
        print("❌ No random numbers available to select winners")
        return []

    # Use the random numbers to select winners
    winners = []
    used_indices = set()  # Track used indices to avoid duplicates

    # Try to select unique winners
    for i in range(min(num_winners, len(participants))):
        # If we have fewer random numbers than winners, we'll reuse them
        random_index = i % len(random_numbers)
        random_value = random_numbers[random_index]

        # Try up to 5 times to find a unique winner
        for _ in range(5):
            winner_index = random_value % len(participants)
            print(f"🔍 Trying winner index: {winner_index}")
            if winner_index not in used_indices:
                used_indices.add(winner_index)
                winners.append(participants[winner_index])
                print(f"✅ Selected winner: {participants[winner_index]}")
                break
            # If we couldn't find a unique winner, modify the random value slightly
            random_value = (random_value * 13 + 7) % (2**256 - 1)
            print(f"🔍 Modified random value: {random_value}")
        else:
            # If we still couldn't find a unique winner after 5 tries, just use the last one
            winner_index = random_value % len(participants)
            winners.append(participants[winner_index])
            print(f"🔍 Selected winner: {participants[winner_index]}")

    print(f"🏆 Selected {len(winners)} winners:")
    for i, winner in enumerate(winners):
        print(f"  {i + 1}. {winner}")

    return winners


# Main execution
if __name__ == "__main__":
    # Load participants from file
    if os.path.exists(PARTICIPANTS_FILE):
        participants = load_participants_from_file(PARTICIPANTS_FILE)
    else:
        print(f"❌ No '{PARTICIPANTS_FILE}' file found. Exiting.")
        exit(1)

    # Ask user if they want to deploy a new contract or use an existing one
    deploy_new = get_input(
        "Do you want to deploy a new contract? (y/N)", default="N"
    ).lower()

    if deploy_new == "y":
        # Deploy the contract
        contract = deploy_contract()

        # Wait for the contract to be fully deployed
        print(
            f"⏳ Waiting {NETWORK['wait_time']} seconds for the contract to be fully deployed..."
        )
        time.sleep(NETWORK["wait_time"])
    else:
        # Try to read contract address from file
        contract_address = None
        if os.path.exists("contract_address.txt"):
            with open("contract_address.txt", "r") as f:
                contract_address = f.read().strip()

        # If not found in file, ask user to input it
        if not contract_address:
            contract_address = get_input("Enter the deployed contract address")

        if not contract_address:
            print("❌ No contract address provided. Exiting.")
            exit(1)

        # Validate the address format
        if not web3.is_address(contract_address):
            print(f"❌ Invalid contract address format: {contract_address}")
            exit(1)

        print(f"🔍 Using existing contract at: {contract_address}")

        # Get the contract ABI
        if os.path.exists("contract_abi.json"):
            with open("contract_abi.json", "r") as f:
                contract_abi = json.load(f)
        else:
            # If ABI file doesn't exist, compile the contract to get the ABI
            print("📄 Compiling contract to get ABI...")
            compiled_sol = compile_files(
                ["contracts/SimpleLottery.sol"], solc_version="0.8.7"
            )
            contract_id, contract_interface = list(compiled_sol.items())[0]
            contract_abi = contract_interface["abi"]

            # Save the ABI for future use
            with open("contract_abi.json", "w") as f:
                json.dump(contract_abi, f)

        # Create contract instance
        contract = web3.eth.contract(address=contract_address, abi=contract_abi)
        print(f"✅ Contract instance created for: {contract_address}")

    # Ask for the number of random numbers to generate
    num_winners = get_input(
        f"Enter the number of winners to select (max: {len(participants)})",
        default=20,
    )
    # ensure number of winners is not greater than the number of participants
    num_winners = min(int(num_winners), len(participants))

    # Generate random numbers
    generate_new_numbers = get_input(
        "Do you want to generate new random numbers? (y/N)", default="N"
    )
    custom_seed = None
    tx_hash = None
    if generate_new_numbers == "y":
        # Ask for a custom seed
        custom_seed = get_input("Enter a custom seed", default=int(time.time()))

        # Use the default account
        tx_hash = generate_random_numbers(
            contract, custom_seed=custom_seed, num_random=num_winners
        )

        if not tx_hash:
            print("❌ Failed to generate random numbers. Exiting.")
            exit(1)

        # Wait for the random numbers to be generated
        print(
            f"⏳ Waiting {NETWORK['wait_time']} seconds for the random numbers to be generated..."
        )
        time.sleep(NETWORK["wait_time"])

    # Get the random numbers
    random_numbers = get_random_numbers(contract)

    if not random_numbers:
        print("❌ No random numbers available. Exiting.")
        exit(1)

    # Select winners
    winners = select_winners(random_numbers, participants, num_winners)

    # Create mapping table for verification
    mapping_table = ""
    for i in range(min(num_winners, len(random_numbers))):
        random_index = i % len(random_numbers)
        random_value = random_numbers[random_index]
        winner_index = random_value % len(participants)
        # Find the actual winner that was selected (accounting for duplicates)
        if i < len(winners):
            mapping_table += (
                f"| {i + 1} | {random_value} | {winner_index} | {winners[i]} |\n"
            )

    # Save winners to a file for verification
    # Write winners
    winner_list = ""
    for i, winner in enumerate(winners):
        winner_list += f"{i + 1}. {winner}\n"

    # only generate report if new numbers were generated
    if generate_new_numbers == "y":
        report = f"""
# LOTTERY VERIFICATION INFORMATION
- 📆 Date: {time.strftime("%Y-%m-%d %H:%M:%S")}
- 🌐 Network: {NETWORK["name"]}
- 🔗 RPC URL: {NETWORK["rpc_url"]}
- 🔗 Chain ID: {NETWORK["chain_id"]}
- 📄 Contract Address: {contract.address}
- 🔑 Seed: {custom_seed or "not available"}

## RESULTS
- 🧾 Transaction Hash: {tx_hash or "not available"}
- 🎲 Random Numbers (Total: {len(random_numbers)}): {random_numbers}
- 📄 Total Participants: {len(participants)}
- 🎉 Number of Winners: {num_winners}

## VERIFICATION MAPPING
| # | Random Number | Index (mod {len(participants)}) | Winner |
|---|---------------|------------|--------|
{mapping_table}

# WINNERS
{winner_list}"""
        with open(REPORT_FILE, "w") as f:
            f.write(report)

        print(f"✅ Winners saved to {REPORT_FILE} for verification")
    print("✨ Lottery completed!")
