import requests
from mnemonic import Mnemonic
from bip32utils import BIP32Key

# Generate mnemonic seed
print("Generating mnemonic seed...")
mnemo = Mnemonic("english")
mn = "vault appear distance recipe decorate crawl aunt polar grit inject obey ribbon"  # Replace with your mnemonic
print(f"Mnemonic: {mn}")

# Derive seed from mnemonic
seed = mnemo.to_seed(mn)
root_key = BIP32Key.fromEntropy(seed)
# Use testnet network
root_key = BIP32Key.fromEntropy(seed, testnet=True)  # Set testnet=True
# BIP84 (SegWit) Derivation for Testnet
child_node = root_key.ChildKey(84 + 0x80000000).ChildKey(1 + 0x80000000).ChildKey(0 + 0x80000000).ChildKey(0).ChildKey(0)
segwit_address = child_node.Address()
print(f"Generated SegWit Address: {segwit_address}")

# BIP44 (P2PKH) Derivation for Testnet
child_node_bip44 = root_key.ChildKey(44 + 0x80000000).ChildKey(1 + 0x80000000).ChildKey(0 + 0x80000000).ChildKey(0).ChildKey(0)
p2pkh_address = child_node_bip44.Address()
print(f"Generated P2PKH Address: {p2pkh_address}")

# Fetch balance
def get_balance(address):
    try:
        response = requests.get(f"https://blockstream.info/testnet/api/address/{address}", timeout=30)
        if response.status_code == 200:
            print("Balance Information:", response.json())
        else:
            print(f"Error: Received status code {response.status_code}")
    except Exception as e:
        print(f"Error fetching balance: {e}")

# Retrieve transaction history
def get_transaction_history(address):
    try:
        response = requests.get(f"https://blockstream.info/testnet/api/address/{address}/txs", timeout=30)
        if response.status_code == 200:
            transactions = response.json()
            if not transactions:
                print("No transactions found.")
            else:
                print("Transaction History:")
                for index, tx in enumerate(transactions):
                    print(f"TX {index + 1}: ID: {tx['txid']}, Confirmed: {tx['status']['confirmed']}")
        else:
            print(f"Error: Received status code {response.status_code}")
    except Exception as e:
        print(f"Error fetching transactions: {e}")

# Example usage
if __name__ == "__main__":
    get_balance(segwit_address)
    get_transaction_history(segwit_address)
