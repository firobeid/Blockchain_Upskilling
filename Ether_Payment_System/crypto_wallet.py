# Cryptocurrency Wallet
################################################################################

# This file contains the Ethereum transaction functions that you have created throughout this module’s lessons. By using import statements, you will integrate this `crypto_wallet.py` Python script into the Fintech Finder interface program that is found in the `fintech_finder.py` file.

################################################################################
# Imports
import os
import requests
from dotenv import load_dotenv
load_dotenv()
from bip44 import Wallet
from mnemonic import Mnemonic
from web3 import Account
from web3 import middleware
from web3.gas_strategies.time_based import medium_gas_price_strategy

################################################################################
# Wallet functionality

#Generate new mnemomic address if needed
def write_env(mnemonic, f):
    f.write(str(mnemonic))

def generate_account(address_index = 0):
    """Create a digital wallet and Ethereum account from a mnemonic seed phrase."""
    
    # Fetch mnemonic from environment variable.
    mnemonic = os.getenv("MNEMONIC")
    if mnemonic is None:
        mnemo = Mnemonic("english")
        mnemonic = mnemo.generate(strength=128)
        with open(".env","w") as f:
            write_env(mnemonic, f)
    
    elif type(mnemonic) == str:

        # Create Wallet Object
        wallet = Wallet(mnemonic)

        # Derive Ethereum Private Key
        private, public = wallet.derive_account("eth",address_index = int(address_index))

        # Convert private key into an Ethereum account
        account = Account.privateKeyToAccount(private)
    # Extra procedure to make sure the private key matches hashed private key
    if account.privateKey == private:
        return account

def get_balance(w3, address):
    """Using an Ethereum account address access the balance of Ether"""
    # Get balance of address in Wei
    wei_balance = w3.eth.get_balance(address)

    # Convert Wei value to ether
    ether = w3.fromWei(wei_balance, "ether")

    # Return the value in ether
    return ether


def send_transaction(w3, account, to, wage):
    """Send an authorized transaction to the Ganache blockchain."""
    # Set gas price strategy
    w3.eth.setGasPriceStrategy(medium_gas_price_strategy)

    # Convert eth amount to Wei
    value = w3.toWei(wage, "ether")

    # Calculate gas estimate
    gasEstimate = w3.eth.estimateGas({"to": to, "from": account.address, "value": value})

    # Construct a raw transaction
    raw_tx = {
        "to": to,
        "from": account.address,
        "value": value,
        "gas": gasEstimate,
        "gasPrice": 0,
        "nonce": w3.eth.getTransactionCount(account.address)
    }

    # Sign the raw transaction with ethereum account
    signed_tx = account.signTransaction(raw_tx)

    # Send the signed transactions
    return w3.eth.sendRawTransaction(signed_tx.rawTransaction)
