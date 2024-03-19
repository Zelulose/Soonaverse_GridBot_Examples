from IotaWallet import SignInToAccount, RecoverWallet, CreateWallet, get_my_balance, check_native_token_balance, parse_available_balance, sync_account, send_transaction, parse_transaction_data
#this is from our header file IotaWallet

#This is to get our soonaverse account data and address to send to
from Soonaverse_Address import get_otrAddress, fetch_all_trades, reset_ids, generate_request, find_matching_token

#These are default imports from Visual Studio
import json
from pathlib import Path
import time
#Global Variable for execution between trades



# Function to get price input
def get_price_input(transaction_type):
    """
    Prompts the user for a comma-separated list of prices for either buy or sell orders.
    Validates the input for numeric values and the number of inputs (1-50).

    Example usage:
        buy_prices = get_price_input("buy")
        sell_prices = get_price_input("sell")
    """
    while True:  # Keep asking until valid input is received
        input_str = input(f"Enter comma-separated prices for {transaction_type} orders: ").strip()
        
        # Handle no input
        if not input_str:
            print("No input received. Please enter at least one price.")
            continue
        
        # Split input string into a list, strip spaces, and filter out empty strings
        prices_str_list = [price.strip() for price in input_str.split(',') if price.strip()]
        
        # Validate number of prices
        if len(prices_str_list) > 50:
            print("Error: Too many prices entered. Please enter between 1 and 50 prices.")
            continue
        
        # Convert to float and validate numeric input
        try:
            prices = [round(float(price), 3) for price in prices_str_list]
            return prices  # Successfully processed and validated prices
        except ValueError:
            print("Error: Non-numeric value detected. Please enter valid numbers.")
            # The loop continues asking for input again



# Example usage
#buy_prices = get_price_input("buy")
#sell_prices = get_price_input("sell")
#____________________________________Token Logic starts here____________________________________________________

#Note: There are a lot of inputs. Once you get one working being sure the csv pasted values are more than 2 buys and 2 sell orders in the grid, ... 
#...you should save to a seperate csv for copy pasting!
class Token:
    def __init__(self, id):
        self.id = id
        self.symbol_name = 0  #example SOON or FEE in all caps
        self.count = 0
        self.price_buy = []
        self.price_sell = []
        self.order_price_buy = []
        self.order_price_sell = []
        self.anchor_price = 0
        self.matching_orders_buy = 0  # Counter for matching buy orders
        self.matching_orders_sell = 0  # Counter for matching sell orders

def check_matching_orders(token):
    if not token.order_price_buy or not token.order_price_sell:
        return 0, 0
    
    matching_buy_orders = len(set(token.price_buy) & set(token.order_price_buy))
    matching_sell_orders = len(set(token.price_sell) & set(token.order_price_sell))
    return matching_buy_orders, matching_sell_orders

#Example usage
#matching_buy, matching_sell = check_matching_orders(token)
#print(f"Matching Buy Orders: {matching_buy}")
#print(f"Matching Sell Orders: {matching_sell}")

def input_token_data():
    tokens = []
    while True:
        id_input = input("Enter token ID (or leave empty to finish): ").strip()
        if not id_input:  # Empty input, finish entering data
            break

        # Create a new Token instance with the exact string ID
        token = Token(id_input)

        # Input symbol name for the token
        symbol_name_input = input(f"Enter symbol name for token {id_input} (e.g., SOON, FEE): ").strip().upper()
        token.symbol_name = symbol_name_input

        # Input count for the token
        count_input = input(f"Enter count for token {id_input}: ").strip()
        try:
            token.count = round(float(count_input), 3)
        except ValueError:
            print("Invalid count input. Please enter a number.")
            continue

        # Input price arrays for the token
        price_buy_input = input(f"Enter comma-separated buy prices for token {id_input}: ").strip()
        try:
            prices_buy = [round(float(price.strip()), 3) for price in price_buy_input.split(',')]
            prices_buy.sort()  # Sort buy prices
            token.price_buy = prices_buy
        except ValueError:
            print("Invalid buy price input. Please enter valid numbers.")
            continue

        price_sell_input = input(f"Enter comma-separated sell prices for token {id_input}: ").strip()
        try:
            prices_sell = [round(float(price.strip()), 3) for price in price_sell_input.split(',')]
            prices_sell.sort()  # Sort sell prices
            token.price_sell = prices_sell
        except ValueError:
            print("Invalid sell price input. Please enter valid numbers.")
            continue
        
        # Remove sell prices lower or equal to the maximum buy price
        min_buy_price = max(token.price_buy)
        token.price_sell = [price for price in token.price_sell if price > min_buy_price]

        # Fetch trades for the token
        trades = fetch_all_trades(token.id)

        # Extract buy and sell prices from trades and populate order_price_buy and order_price_sell
        token.order_price_buy = [round(trade[1], 3) for trade in trades if trade[4] == 0]  # Type 0 is for Buy
        token.order_price_sell = [round(trade[1], 3) for trade in trades if trade[4] == 1]  # Type 1 is for Sell

        # Sort order_price_buy and order_price_sell
        token.order_price_buy.sort()
        token.order_price_sell.sort()

        tokens.append(token)

    return tokens

    

def print_token_data(tokens):
    print("\nToken Data:")
    for token in tokens:
        print(f"Token ID: {token.id}")
        print(f"Count: {token.count}")
        print(f"Buy Prices: {token.price_buy}")
        print(f"Sell Prices: {token.price_sell}")
        print(f"Order Buy Prices: {token.order_price_buy}")
        print(f"Order Sell Prices: {token.order_price_sell}")


def fetch_order_sql_buy(token):
    # Save the previous order prices
    previous_order_prices = token.order_price_buy.copy()  # Make a copy to preserve the previous values
    
    # Fetch trades for the token
    trades = fetch_all_trades(token.id)

    # Extract buy prices from trades and populate order_price_buy
    token.order_price_buy = [round(trade[1], 3) for trade in trades if trade[4] == 0]  # Type 0 is for Buy

    # Sort the updated order_price_buy
    token.order_price_buy.sort()
    
    # Calculate the difference in buy orders
    difference_buy = len(token.order_price_buy) - len(previous_order_prices)
    
    return difference_buy


def fetch_order_sql_sell(token):
    # Save the previous order prices
    previous_order_prices = token.order_price_sell.copy()  # Make a copy to preserve the previous values
    
    # Fetch trades for the token
    trades = fetch_all_trades(token.id)

    # Extract sell prices from trades and populate order_price_sell
    token.order_price_sell = [round(trade[1], 3) for trade in trades if trade[4] == 1]  # Type 1 is for Sell

    # Sort the updated order_price_sell
    token.order_price_sell.sort()

    # Calculate the difference in sell orders
    difference_sell = len(token.order_price_sell) - len(previous_order_prices)
    
    return difference_sell

def monitor_buy_orders(token):
    print("Warning: Pending buy order!")
    while True:
        difference_buy = fetch_order_sql_buy(token)
        #adjust_prices_both_sides(token) 
        if difference_buy > 0:
            print("Warning:  buy order completed!")
            print(difference_buy)  # Print the number of new buy orders detected
            break
        time.sleep(0.1)  # Adjust sleep duration as needed

def monitor_sell_orders(token):
    print("Warning: Pending sell order!")
    while True:
        difference_sell = fetch_order_sql_sell(token)
        #adjust_prices_both_sides(token)
        if difference_sell > 0:
            print("Warning:  sell order completed!")
            print(difference_sell)  # Print the number of new sell orders detected
            break
        
        time.sleep(0.1)  # Adjust sleep duration as needed

def adjust_prices_both_sides(token):
    matching_difference_buy = fetch_order_sql_buy(token)
    matching_difference_sell = fetch_order_sql_sell(token)
    if abs(matching_difference_buy) > abs(matching_difference_sell):
        for _ in range((abs(matching_difference_buy) - abs(matching_difference_sell)) - 1):
            max_buy_price = max(token.price_buy)
            token.price_sell.append(max_buy_price)
            token.price_buy.remove(max_buy_price)
        token.anchor_price = max(token.price_buy)
    elif abs(matching_difference_buy) < abs(matching_difference_sell):
        for _ in range((abs(matching_difference_sell) - abs(matching_difference_buy)) - 1):
            min_sell_price = min(token.price_sell)
            token.price_buy.append(min_sell_price)
            token.price_sell.remove(min_sell_price)
        token.anchor_price = max(token.price_buy)
        
#This has logic for when we prace orders the names of the functions make the process self explanatory but we shift orders up and down and place buy or sell orders as needed based on what is filled.
def adjust_prices(tokens, WalletExists, NameYourAlias):
    for token in tokens:
        matching_difference_buy = fetch_order_sql_buy(token)
        matching_difference_sell = fetch_order_sql_sell(token)
        
        if not token.price_buy or not token.price_sell:
            print("Gridbot has completed its task.")
            print(token.price_buy)
            print(token.price_sell)
            time.sleep(2)
            return

        elif max(token.price_buy) not in token.order_price_buy and min(token.price_sell) not in token.order_price_sell:
            print("Buy both!")
            # Check which side has a greater absolute difference and adjust accordingly
            if abs(matching_difference_buy) > abs(matching_difference_sell):
                # Loop through the buy side
                for _ in range((abs(matching_difference_buy)-abs(matching_difference_sell)) - 1):
                    max_buy_price = max(token.price_buy)
                    token.price_sell.append(max_buy_price)
                    token.price_buy.remove(max_buy_price)
                token.anchor_price = max(token.price_buy)  # Set anchor price to the new maximum buy price
            elif abs(matching_difference_buy) < abs(matching_difference_sell):
                # Loop through the sell side
                for _ in range((abs(matching_difference_sell)-abs(matching_difference_buy)) - 1):
                    min_sell_price = min(token.price_sell)
                    token.price_buy.append(min_sell_price)
                    token.price_sell.remove(min_sell_price)
                token.anchor_price = max(token.price_buy)  # Set anchor price to the new maximum buy price
            #place orders now that variables are set!
            if max(token.price_buy) not in token.order_price_buy:
                sync_account(WalletExists, NameYourAlias)
                metadata_buy, amount_buy = generate_request(token.symbol_name,"BUY_TOKEN",max(token.price_buy),token.count)
                soon_address = get_otrAddress()
                trade_buy = send_transaction(WalletExists, NameYourAlias, str(soon_address), amount_buy, None, str(metadata_buy)) #buy orders have token ID set to none! this is from the IotaWallet.py
                time.sleep(1)
                monitor_buy_orders(token)
                
            if min(token.price_sell) not in token.order_price_sell:
                sync_account(WalletExists, NameYourAlias)        
                metadata_sell, amount_sell = generate_request(token.symbol_name,"SELL_TOKEN",min(token.price_sell),token.count)
                #print(metadata_sell)
                #print(amount_sell)
                soon_address = get_otrAddress()
                foundry_token_id = find_matching_token(token.id)
                #print(foundry_token_id)
                trade_sell = send_transaction(WalletExists, NameYourAlias, str(soon_address), amount_sell, foundry_token_id, str(metadata_sell)) #buy orders have token ID set to none! this is from the IotaWallet.py
                #print(trade_sell)
                time.sleep(1)
                monitor_sell_orders(token)
            print(f"Buy Prices: {token.price_buy}")
            print(f"Sell Prices: {token.price_sell}")

        elif max(token.price_buy) not in token.order_price_buy:
            print("Highest bid is missing. Need to move highest bid to sell list.")
            for _ in range(abs(matching_difference_buy)-1):
                max_buy_price = max(token.price_buy)
                token.price_sell.append(max_buy_price)
                token.price_buy.remove(max_buy_price)
                token.anchor_price = max(token.price_buy)  # Set anchor price to the new maximum buy price
            #run it once based on states outside of the loop conditions
            max_buy_price = max(token.price_buy)
            token.price_sell.append(max_buy_price)
            token.price_buy.remove(max_buy_price)
            token.anchor_price = max(token.price_buy) 
            time.sleep(2)
            #place orders now that variables are set!
            if max(token.price_buy) not in token.order_price_buy:
                sync_account(WalletExists, NameYourAlias)
                metadata_buy, amount_buy = generate_request(token.symbol_name,"BUY_TOKEN",max(token.price_buy),token.count)
                soon_address = get_otrAddress()
                trade_buy = send_transaction(WalletExists, NameYourAlias, str(soon_address), amount_buy, None, str(metadata_buy)) #buy orders have token ID set to none! this is from the IotaWallet.py
                time.sleep(1)
                monitor_buy_orders(token)
                
            if min(token.price_sell) not in token.order_price_sell:
                sync_account(WalletExists, NameYourAlias)        
                metadata_sell, amount_sell = generate_request(token.symbol_name,"SELL_TOKEN",min(token.price_sell),token.count)
                soon_address = get_otrAddress()
                foundry_token_id = find_matching_token(token.id)
                trade_sell = send_transaction(WalletExists, NameYourAlias, str(soon_address), amount_sell, foundry_token_id, str(metadata_sell)) #buy orders have token ID set to none! this is from the IotaWallet.py
                time.sleep(1)
                monitor_sell_orders(token)
            print("Sold! Raise the bid!")
            print(f"Buy Prices: {token.price_buy}")
            print(f"Sell Prices: {token.price_sell}")

        elif min(token.price_sell) not in token.order_price_sell:
            print("Lowest ask is missing. Need to move Lowest ask to bid list.")
            for _ in range(abs(matching_difference_sell)-1):
                min_sell_price = min(token.price_sell)
                token.price_buy.append(min_sell_price)
                token.price_sell.remove(min_sell_price)
                token.anchor_price = max(token.price_buy)  # Set anchor price to the new maximum buy price always
            #run it once based on bid states outside of the loop conditions
            min_sell_price = min(token.price_sell)
            token.price_buy.append(min_sell_price)
            token.price_sell.remove(min_sell_price)
            token.anchor_price = max(token.price_buy)  # Set anchor price to the new maximum buy price always
            time.sleep(2)
            #place orders now that variables are set!
            if max(token.price_buy) not in token.order_price_buy:
                sync_account(WalletExists, NameYourAlias)
                metadata_buy, amount_buy = generate_request(token.symbol_name,"BUY_TOKEN",max(token.price_buy),token.count)
                soon_address = get_otrAddress()
                trade_buy = send_transaction(WalletExists, NameYourAlias, str(soon_address), amount_buy, None, str(metadata_buy)) #buy orders have token ID set to none! this is from the IotaWallet.py
                time.sleep(1)
                monitor_buy_orders(token)
                
            if min(token.price_sell) not in token.order_price_sell:
                sync_account(WalletExists, NameYourAlias)        
                metadata_sell, amount_sell = generate_request(token.symbol_name,"SELL_TOKEN",min(token.price_sell),token.count)
                soon_address = get_otrAddress()
                foundry_token_id = find_matching_token(token.id)
                trade_sell = send_transaction(WalletExists, NameYourAlias, str(soon_address), amount_sell, foundry_token_id, str(metadata_sell)) #buy orders have token ID set to none! this is from the IotaWallet.py
                time.sleep(1)
                monitor_sell_orders(token)
            print("Bought! Lower the ask!")
            print(f"Buy Prices: {token.price_buy}")
            print(f"Sell Prices: {token.price_sell}")

        if max(token.price_buy) in token.order_price_buy and min(token.price_sell) in token.order_price_sell:
            print("Hodl!")
            time.sleep(2)
            print(f"Buy Prices: {token.price_buy}")
            print(f"Sell Prices: {token.price_sell}")
        
    
    # Example usage
    # Input token data
    #tokens = input_token_data()

    # Print token data
    #print_token_data(tokens)
    #adjust_prices(tokens)
#______________________________________________________________________________ end default input for global variables________________________________________



def main():
    NameYourAccount = input("Enter your account name: ")
    Password = input("Enter your password: ")
    NameYourAlias = NameYourAccount  # To keep it simple, account name is the Alias
    
    WalletExists, accountExists = SignInToAccount(NameYourAccount, NameYourAlias, Password)

    if WalletExists is None or accountExists is None:
        # Decide to create or recover wallet
        user_choice = input("Use existing wallet? Y/N: ").lower()
        
        if user_choice == "y":
            mnemonic = input("Enter your mnemonic: ")
            NameYourAccount = input("Enter your account name: ")
            Password = input("Enter your password: ")
            NameYourAlias = NameYourAccount
            RecoverWallet(NameYourAccount, NameYourAlias, Password, mnemonic)
        else:
            NameYourAccount = input("Enter your account name: ")
            Password = input("Enter your password: ")
            NameYourAlias = NameYourAccount
            CreateWallet(NameYourAccount, NameYourAlias, Password)

        # Attempt to sign in again to grab account balances
        WalletExists, accountExists = SignInToAccount(NameYourAccount, NameYourAlias, Password)
        if accountExists:
            print(json.dumps(accountExists, indent=4))
        else:
            print("Failed to create or recover the account. Please check your inputs and try again.")
    else:
        # If wallet and account exist, print account details
        print(json.dumps(accountExists, indent=4))
        
    NameYourAlias = NameYourAccount
    #CreateWallet(NameYourAcount, NameYourPin, Password)
    if WalletExists is None or accountExists is None:
        WalletExists, accountExists = SignInToAccount(NameYourAccount, NameYourAlias, Password)
    #print(json.dumps(accountExists, indent=4))
    sync_account(WalletExists,NameYourAlias)
    balance = get_my_balance(WalletExists, NameYourAlias)
    available_balance = parse_available_balance(str(balance))
    print(f"Account Balance: {available_balance} SMR")


    nbalance = check_native_token_balance(WalletExists, NameYourAlias)
    print(f"Native Balance: {nbalance} SMR")
    
    #Ok we checked the account and the balances. So we should be able to send tokens now!
    # Example usage
    # Input token data
    tokens = input_token_data()

    # Print token data
    print_token_data(tokens)
    
        



    try:
        while True: #the sleeping functions are in the adjust function to save your pc!
            adjust_prices(tokens, WalletExists, NameYourAlias)
    except KeyboardInterrupt:
        print("Loop interrupted. Exiting...")

#we use oursend function so we will need to pass data through this function!
#send_transaction(wallet, NameYourAlias, recipient_address_str, custom_amount, token_id=None, custom_metadata_str=None)

    #Finished loging in and checking balance and trading logic: end!
    #____________________________________________________________________________________________________________________________________________________



if __name__ == "__main__":
    main()  #be sure to run your ts soonaverse api program so it updates your sql database. Otherwise, you wont have data to trade with! 
            #You can always add your own sql database functions using our Soonaverse_Address.py which also has a fetch function
