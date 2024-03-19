#python 3.9
#pip install 24

import os
from typing import List
from pathlib import Path
from pickle import FALSE
from dotenv import load_dotenv 
#pip install python-dotenv 1.0.0
from iota_sdk import MetadataFeature, SyncOptions, TimelockUnlockCondition, Client, Ed25519Address, IssuerFeature, ClientOptions, CoinType, Features, OutputParams, NativeToken, Assets, HexStr, StrongholdSecretManager, StorageDeposit, ReturnStrategy, Utils, Wallet, TransactionOptions, RegularTransactionEssence, TransactionPayload, RemainderValueStrategy, TaggedDataPayload, SendNativeTokensParams, Irc30Metadata, PreparedTransactionData, InputSigningData, utf8_to_hex
#pip install iota_sdk
import re
import shutil

import msvcrt  # For Windows keypress. For Unix-based systems, use 'input()'
import json
#Remaining imports are default installed with visual studio 2022 using windows.

# Load environment variables
load_dotenv()

#Here we get a list of the accounts and their names
base_folder_path = Path.home() / "Documents" / "Stronghold" #we use your documents folder to
def find_stronghold_folders(base_folder_path):
    """
    Searches for Stronghold files in all subfolders within the base folder path and returns their names.

    Args:
        base_folder_path (Path): Base folder where Stronghold subfolders are located.

    Returns:
        An array of folder names containing a Stronghold file.
    """
    folder_names = []

    for stronghold_folder in base_folder_path.iterdir():
        if stronghold_folder.is_dir():
            stronghold_file = stronghold_folder / "vault.stronghold"
            if stronghold_file.is_file():
                folder_names.append(stronghold_folder.name)

    return folder_names

#select the account
def get_folder_name_by_index(folder_names, index):
    """
    Retrieves the folder name corresponding to the given index from the list of folder names.

    Args:
        folder_names (list): The list of folder names.
        index (int): The index of the folder name to retrieve.

    Returns:
        The name of the folder at the given index, or None if the index is invalid.
    """
    if 0 <= index < len(folder_names):
        return folder_names[index]
    return None


def create_character_folder(character_name):
    # Convert the input string to lowercase
    character_name = character_name.lower()

    # Extract the rightmost 7 characters (or fewer if the string is shorter) and leave behind the name
    last_characters = character_name[-8::-1]
    
    # Reverse the order of characters in last_characters
    last_characters = last_characters[::-1]

    # Create a list of subfolder names for each character from the rightmost to the 8th character from the end
    subfolder_names = list(character_name[-7:])

    # Initialize the character folder
    character_folder = ""

    # Create subfolders based on the character names
    for subfolder_name in subfolder_names:
        character_folder += subfolder_name + "/"

    # Create the final folder by concatenating the character folder and last_characters
    final_folder = character_folder + last_characters

    return final_folder

#import shutil
#os.path.exists(final_folder) use this to check if the path exists.
#shutil.rmtree to delete a folder (we will actually copy it and move it to archives)
#shutil.copytree(source_folder, destination_folder, dirs_exist_ok=True)
#Note:The dirs_exist_ok=True argument allows the function to overwrite any files in the destination directory that have the same name as files in the source directory.
#Note: Modify to always go to home directory.

#sign in to existing account
def SignInToAccount(NameYourAcount, NameYourAlias, Password):
    home_directory = Path.home()
    stronghold_folder = home_directory / "Documents" / "Stronghold" / NameYourAcount #We send your data to your documents folder using home directory in windows
    stronghold_snapshot_file = stronghold_folder / "vault.stronghold"
    STRONGHOLD_SNAPSHOT_PATH = str(stronghold_snapshot_file)
    rocksdb_storage_path = stronghold_folder / "rocksdb_storage"
    rocksdbstringpath = str(rocksdb_storage_path)
    ACCOUNT_ALIAS = NameYourAlias
    node_url = os.environ.get('NODE_URL', 'https://api.shimmer.network')
    STRONGHOLD_PASSWORD = os.environ.get('STRONGHOLD_PASSWORD', Password)
    client_options = ClientOptions(nodes=[node_url])

    if stronghold_snapshot_file.is_file():
        secret_manager = StrongholdSecretManager(STRONGHOLD_SNAPSHOT_PATH, STRONGHOLD_PASSWORD)
        wallet = Wallet(client_options=client_options,
                        coin_type=CoinType.SHIMMER,
                        secret_manager=secret_manager,
                        storage_path=rocksdbstringpath)
        accounts0 = wallet.recover_accounts(0, 3, 10, None)
        return wallet, accounts0
    else:
        # Handle the case where the Stronghold file does not exist
        print("Stronghold file does not exist. Please create a wallet first.")
        return None, None

    #only sign in once! Example of use!
    #WalletExists, accountExists = SignInToAccount(NameYourAcount, NameYourAlias, Password)
    #print(json.dumps(accountExists, indent=4))
    #refresh these functions as the jason prints everything including account balance


def RecoverWallet(NameYourAcount, NameYourAlias, Password, mnemonic):
    home_directory = Path.home()
    stronghold_folder = home_directory / "Documents" / "Stronghold" / NameYourAcount
    stronghold_snapshot_file = stronghold_folder / "vault.stronghold"
    STRONGHOLD_SNAPSHOT_PATH = str(stronghold_snapshot_file)
    rocksdb_storage_path = stronghold_folder / "rocksdb_storage"
    rocksdbstringpath = str(rocksdb_storage_path)
    ACCOUNT_ALIAS = NameYourAlias
    node_url = os.environ.get('NODE_URL', 'https://api.shimmer.network')
    STRONGHOLD_PASSWORD = os.environ.get('STRONGHOLD_PASSWORD', Password)
    client_options = ClientOptions(nodes=[node_url])

    if stronghold_snapshot_file.is_file():
        # Handle the case where the Stronghold file already exists
        print("Stronghold file already exists. Use the CreateWallet function to create a new wallet.")
        return "Wallet already exists for this Account Name. Return to Login"

    # Use provided mnemonic to create a new wallet and store the mnemonic
    secret_manager = StrongholdSecretManager(STRONGHOLD_SNAPSHOT_PATH, STRONGHOLD_PASSWORD)
    wallet = Wallet(client_options=client_options, 
                    coin_type=CoinType.SHIMMER, 
                    secret_manager=secret_manager,
                    storage_path=rocksdbstringpath)
    wallet.store_mnemonic(mnemonic)
    account = wallet.create_account(ACCOUNT_ALIAS)
    print(f"Created recovery account with provided mnemonic and alias: {ACCOUNT_ALIAS}")
    
    return "Account Created. Return to Login"
#RecoverWallet(NameYourAcount, NameYourAlias, Password, mnemonic)
#returned to login and grab account balances
#WalletExists, accountExists = SignInToAccount(NameYourAcount, NameYourAlias, Password)
#print(json.dumps(accountExists, indent=4))

def CreateWallet(NameYourAcount, NameYourAlias, Password):
    home_directory = Path.home()
    stronghold_folder = home_directory / "Documents" / "Stronghold" / NameYourAcount
    stronghold_snapshot_file = stronghold_folder / "vault.stronghold"
    STRONGHOLD_SNAPSHOT_PATH = str(stronghold_snapshot_file)
    rocksdb_storage_path = stronghold_folder / "rocksdb_storage"
    rocksdbstringpath = str(rocksdb_storage_path)
    ACCOUNT_ALIAS = NameYourAlias
    node_url = os.environ.get('NODE_URL', 'https://api.shimmer.network')
    STRONGHOLD_PASSWORD = os.environ.get('STRONGHOLD_PASSWORD', Password)
    client_options = ClientOptions(nodes=[node_url])

    if stronghold_snapshot_file.is_file():
        # Handle the case where the Stronghold file already exists
        print("Wallet already exists for this Account Name. Return to Login")
        return "Wallet already exists for this Account Name. Return to Login"

    # Create a new Stronghold file, wallet, and store a new mnemonic
    secret_manager = StrongholdSecretManager(STRONGHOLD_SNAPSHOT_PATH, STRONGHOLD_PASSWORD)
    wallet = Wallet(client_options=client_options, 
                    coin_type=CoinType.SHIMMER, 
                    secret_manager=secret_manager,
                    storage_path=rocksdbstringpath)
    mnemonic = Utils.generate_mnemonic()
    wallet.store_mnemonic(mnemonic)
    
    # Create a new account with the specified alias
    account = wallet.create_account(ACCOUNT_ALIAS)
    print("Successfully Created Account: Last Chance to Save private key before logging out:" + str(mnemonic))
    return f"Successfully Created Account: Last Chance to Save private key before logging out:" + str(mnemonic)
#Example use
    #CreateWallet(NameYourAcount, NameYourAlias, Password)
    #returned to login and grab account balances
    #WalletExists, accountExists = SignInToAccount(NameYourAcount, NameYourAlias, Password)
    #print(json.dumps(accountExists, indent=4)) Note: This is our Wallet variable


#Conditionally sends a transaction to a recipient's address, either as a primary network token
def send_transaction(wallet, NameYourAlias, recipient_address_str, custom_amount, token_id=None, custom_metadata_str=None):
    try:
        account = wallet.get_account(NameYourAlias)



        if token_id is None:
            
            # Method for sending primary network token
            output = account.prepare_output(OutputParams(
                recipientAddress=recipient_address_str, amount=str(custom_amount), features=Features(metadata=HexStr(utf8_to_hex(utf8_data=custom_metadata_str)))))
            transaction = account.send_outputs([output])
        else:
            # Define storage deposit options with the Gift strategy
            storage_deposit_options = StorageDeposit(
                returnStrategy=ReturnStrategy.Gift,
                useExcessIfLow=True   # Assuming you want to use excess deposit if the provided amount is low
            )
            # Method for sending specified native token
            output = account.prepare_output(OutputParams(
                recipientAddress=recipient_address_str,
                amount=str(0),
                assets=Assets(nativeTokens=[NativeToken(token_id, hex(custom_amount))]), 
                features=Features(metadata=HexStr(utf8_to_hex(utf8_data=custom_metadata_str))), storageDeposit=storage_deposit_options
                ))
            transaction = account.send_outputs([output])
            # Optionally, wait for transaction to get included or handle as needed
            
        # Assuming the transaction variable includes transaction ID and other details
        print(transaction)
        return transaction
    except Exception as e:
        # Return a dictionary with 'amount' and 'timestamp' as '0' in case of an error
        return {"amount": "0", "timestamp": "0", "error": str(e)}
    """
    Remember to syncronize the account!

    Args:
        wallet (Wallet): The wallet instance.
        account_alias (str): The alias of the account to synchronize.
    """
#Example use transaction_result = send_transaction(WalletExists, NameYourAlias, recipient_address, amount, "0x0879ead286b33e6520219d7b7690d27c0778d33f01cab14280e96de007784cad820200000000", custom_metadata_str)
    #recipient_address = "smr...231j"
    #amount = smr units * 1000000 #(otherwise we get decimals)
    #Remember wallet is one of the two returned variables here! WalletExists, accountExists = SignInToAccount(NameYourAcount, NameYourAlias, Password)

#seperate parse to just grab the transaction amount and timestamp. Address will be sent seperately
def parse_transaction_data(transaction_data):
    """
    Parse the 'amount' and 'timestamp' values from transaction data.

    Args:
        transaction_data (dict): The transaction data.

    Returns:
        tuple: A tuple containing the 'amount' (int) and 'timestamp' (int) values.
    """
    try:
        # Extract the 'amount' value using regex
        amount_pattern = r"'amount': '(\d+)'"
        amount_match = re.search(amount_pattern, str(transaction_data))
        amount = int(amount_match.group(1)) if amount_match else None

        # Extract the 'timestamp' value using regex
        timestamp_pattern = r"timestamp='(\d+)'"
        timestamp_match = re.search(timestamp_pattern, str(transaction_data))
        timestamp = int(timestamp_match.group(1)) if timestamp_match else None

        return amount, timestamp
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None, None

def sync_account(wallet, NameYourAlias):
    """
    Synchronize an account in the wallet.

    Args:
        wallet (Wallet): The wallet instance.
        account_alias (str): The alias of the account to synchronize.
    """
    # Retrieve the account by alias
    account = wallet.get_account(NameYourAlias)
   

    if account:
        # Synchronize the account
        account.sync(None)  # You can pass specific sync options if needed
        print(f"Account '{NameYourAlias}' synchronized successfully.")
    else:
        print(f"Account '{NameYourAlias}' not found in the wallet.")

def get_transactions(wallet, NameYourAlias):
    try:
        # Get the specified account from the wallet
        account = wallet.get_account(NameYourAlias)

        # Fetch all transactions for the account
        all_transactions = account.get_transaction()

        # Get the last n transactions (assuming the list is sorted by timestamp)
        return all_transactions

    except Exception as e:
        return str(e)

def get_my_balance(wallet, NameYourAlias):
    """
    Get the balance associated with an account using an alias.

    Args:
        wallet (Wallet): The wallet object.
        alias (str): The alias for the account.

    Returns:
        int: The account balance in IOTA tokens, or 0 if the account is not found.
    """
    try:
        account = wallet.get_account(NameYourAlias)

        if account:
            # Synchronize the account to ensure the balance is up to date
            balance = account.sync(SyncOptions(sync_only_most_basic_outputs=True))
            return balance
        else:
            print(f"Account '{NameYourAlias}' not found in the wallet.")
            return 0
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return 0

def check_native_token_balance(wallet, NameYourAlias):
    """
    Check the balance of native tokens for a specified account.

    Args:
        wallet (Wallet): The wallet instance.
        account_name (str): The name of the account to check the balance for.

    Returns:
        dict: A dictionary of token balances with token IDs as keys and available balances as values.
    """
    account = wallet.get_account(NameYourAlias)
    balance = account.sync()  # Sync account with the node
    token_balances = {token.tokenId: int(token.available, 0) for token in balance.nativeTokens}
    return token_balances

def parse_available_balance(balance_str):
    """
    Parse the available balance from the account balance string.

    Args:
        balance_str (str): The account balance string.

    Returns:
        int: The available account balance in IOTA tokens, or 0 if not found.
    """
    try:
        # Define a regular expression pattern to find 'available' value
        pattern = r"available='(\d+)'"

        # Use regex to find 'available' value in the balance string
        match = re.search(pattern, balance_str)

        if match:
            available_balance = int(match.group(1))
            return available_balance
        else:
            print("Available balance not found in the balance string.")
            return 0
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return 0

    #CreateWallet(NameYourAcount, NameYourAlias, Password)
