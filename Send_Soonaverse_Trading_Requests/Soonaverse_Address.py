#more default imports from visual studio
import os
import sqlite3
import time
import json

#format metadata to this address. Address can also be called using soonaverse documentation if production address changes to sort transactions
def get_otrAddress():
    otrAddress = 'smr1qp0248uakdvfrhyr58yk5lswhnt033vrhst2j4c77laepdv2rk0psgh4t4x'
    return otrAddress



list_of_tokens = [
    "0x0884298fe9b82504d26ddb873dbd234a344c120da3a4317d8063dbcf96d356aa9d0100000000", #1. soon
    "0x0877a4951292b80c2ef0a847a7e730b7929266ca05e3e68c28355036cac314304f0100000000", #2. fee
    "0x084fbbb31eb49ae1c2416fdd97d675d94b280cbd88ebf0c13c93a4f6f01cba5fdf0100000000", #3. ape Note: iota token
    "", #4. Shimu pending launch
    "0x08fc7819ec252ade5d3e51beee9b28a156073d9c4a1d30ba2e3f6720036abdb6430100000000", #5. house Note: iota token
    "0x083d4586fee44d68757c017ad9a5f0907ae63fec477abed602636f0db633e6b6c30100000000", #6. SMT 
    "0x08b34636effc4cd3384b5eccf2d7bcc0a0cc960424a9faaef697d18039e9f0fb8a0100000000", #7. RTO
    "0x08834ae47b5f152834fa9f56c79c0f67d027c2d7f8fb23d83f90eec6a67daa31970100000000", #8. Esta 
    "0x087a31c89dea0e0b6629e76af51c5ab10ef0b41bd4af6b0069a312361e7ee5ab470100000000", #9. charj
    "0x08da8eaf99fa57c9374e17c9824d3c677193fa071b6dddceb79bb9d2865e5ed4b60100000000", #10. gct
    "0x088ed60a6b69d58f97c52f6b43de21ab7e7ea0b65a215971524d4ee63dba7aeb970100000000", #11. mxt
    "0x089d772aff9c88de9a809e7c6f50d647a7f23a6de6228ac5e23061196c0b2ebd820100000000", #12. nati
    "0x080b8f0e1388a19e6a6307769a84385d3fa9c997799e55186c57170c759455ee5e0100000000", #13. rgl
    "0x080b3f3d3b203570a4287a519db3f7e4f3b659244f6d42ea2e2ca045cd6bd99d850100000000", #14. ist
    "0x081e6aad157f51d3d56cd470a94a2435ab5d502d17160218b10ce62c58ac371c670100000000", #15. sddt
    "0x08c877da8aad151010c2128b7b78b16613a18ef578a82e8609b0cb4f074f3e5e850100000000", #16. beast
    "", #17. audit pending launch
    "0x08b3420d742acfac6938c9334b2e3d0d9fa7b838c47d047914cbfd607c2549e22c0100000000", #18. punk
    "0x087ef85a59f63748e17c45dbbd4ad878e8e33a39c7790890dc905e1218cfd42d4a0100000000", #19. crt
    "0x088a2327a8c9340e2961b65874ab5d7610ee24f242a45bbd4f7da9e281cdc3d3a60100000000", #20. xp
    "0x08a1cf22bd5321b81f3ac37cd45c3a4478078a2d864f6cdaf27b0ab29f6c6562670100000000", #21. fuel
    "0x0879ead286b33e6520219d7b7690d27c0778d33f01cab14280e96de007784cad820200000000", #22. FISH
    "0x086fec8f849701dcf9064eec87bedc7ea49920318c525f88504fefe9c8c73fef9b0100000000", #23. BB
    "0x08ca5d979f353f5803756bb4c8db4e6407beb53766c4b413bad9bb03a04b4aca5e0100000000", #24. Hibal
    "", #25. BI pending launch
    "0x08bc057855bcc62283d0119e84de2feba6117a033e8c0e3f59eb5892a0cf0831d00100000000", #26. Maji
    "0x08667286764515d0cbe0e147361133185c76931b24e0b41d2463cad64329a4897f0100000000", #27. Digi
    "", #28. GM pending launch
    "" #29. AAP pending launch
    ]
list_of_soonaverse_tokens = [
    
    "0x9600b5afbb84f15e0d4c0f90ea60b2b8d7bd0f1e", #1. soon
    "0x55cbe228505461bf3307a4f1ed951d0a059dd6d0", #2. fee
    "0x10ba907cc33418555dd1203ede5fd2c26fef4c68", #3. ape
    "0x1e77fd61d1b0220c70af752502b8afa1f6a09f68", #4. Shimu
    "0xb00469a9f549f8126a0e1455a99e5f4cb5c887b3", #5. house
    "0x7ed8021d6a118b083281a9f78f08e8a3b3072368", #6. SMT
    "0xbe507db0f565c4b7a145f32daaed6bd6655fda7c", #7. RTO
    "0x62467a0b66953cdfca406d15e5843f627dc94b1f", #8. Esta 
    "0x741d5fab9a054ef2273ce1b84a54058268cb9ba6", #9. charj
    "0xeb7a38232dbab455a4b566dbaafb6130257d95db", #10. gct
    "0x9da087f1ff98859e468c81ce25bde6ed9139e07d", #11. mxt
    "0xdcc6a77421c6f3fba334be23a5dda1ee4740937c", #12. nati
    "0xcb6792905b9db331040e81a4d5db378cde8fd514", #13. rgl
    "0xd9555bf625676eb646a3fb259189fddfa367d506", #14. ist
    "0x3e43d11dd1a86c5a2f4f2aa39eed54c4fb5568c2", #15. sddt
    "0x701e62f301748d9443e480a53ccdf360c592257c", #16. beast
    "0xbc7e01dc6114ca05c898e251cbb62e1d491e8652", #17. audit
    "0x70a484eb9ac89a197649b9b93e6db744fdf7b28a", #18. punk
    "0x5a0414d3224611b8522422aec54fae8b8e7f5a2b", #19. crt
    "0x05a1a9b2fe190d67ad2df020f112e3e91f32d90e", #20. xp
    "0xbfcf49233766e1253c8dafee95b7e63ea1053b6b", #21. fuel
    "0x164a30a7fb6ad8f6d02a74528a29bb136298874a", #22. FISH
    "0x4426552545b5c01bc085c00fff985144ba324a2f", #23. BB
    "0x031eadb3749ed3b00d9b1f8a222c535489c8f1f1", #24. Hibal
    "0xebb5778ded8b88b97c6a64848a40add912a3605b", #25. BI
    "0x7694bc00ec19b041a6f5af16e8183060093c2cce", #26. Maji
    "0x08667286764515d0cbe0e147361133185c76931b24e0b41d2463cad64329a4897f0100000000", #27. Digi
    "0x55fc860896ce0e1d5c17379606089f420456ada6", #28. GM
    "0xf8fe9a39f9392c4bfe8e10933c1250b4aa86458b" #29. AAP
    ]

#this finds the index of our soonaverse token id and then returns our tangle foundry id 
def find_matching_token(token_string):
    try:
        index = list_of_soonaverse_tokens.index(token_string)
        return list_of_tokens[index]
    except ValueError:
        return "Token not found in Soonaverse tokens list"

def get_database_path():
    # Get the path to the user's Documents directory
    documents_path = os.path.join(os.path.expanduser('~'), 'Documents')
    
    # Construct the path to the Soonaverse Trade Data folder
    soonaverse_folder_path = os.path.join(documents_path, 'Soonaverse Trade Data')
    
    return soonaverse_folder_path

def connect_to_database(token_id: str):
    # Construct the path to the SQLite database file
    db_path = os.path.join(get_database_path(), f'{token_id}.db')
    
    # Check if the database file exists
    if os.path.exists(db_path):
        # Connect to the SQLite database
        connection = sqlite3.connect(db_path)
        return connection
    else:
        print(f"Database file {db_path} does not exist.")
        return None

def reset_ids(token_id: str):
    try:
        # Connect to the database
        conn = connect_to_database(token_id)
        if conn is None:
            # If database connection fails, return without doing anything
            print("Database connection failed.")
            return

        # Execute a SQL query to reset the IDs
        cursor = conn.cursor()
        cursor.execute('UPDATE trades SET id = id - (SELECT MIN(id) - 1 FROM trades);')

        # Commit the transaction and close the connection
        conn.commit()
        conn.close()

        #print("IDs reset successfully.")
    except Exception as e:
        print("Error resetting IDs:", e)

#note: cutting the program off will cut off part of the database so make sure to run our Shimmer_Soonaverse_Gridbot_Sample

def fetch_all_trades(token_id: str):
    reset_ids(token_id)
    # Connect to the database
    conn = connect_to_database(token_id)
    if conn is None:
        # Return default structure if database file doesn't exist
        return [(0, 0, 0, 0, 0)]  # ID, price, volume, state, type all set to 0
    
    cursor = conn.cursor()
    
    # Execute a query to fetch all records from the trades table
    cursor.execute('SELECT * FROM trades')
    trades = cursor.fetchall()
    
    # Close the connection to the database
    conn.close()
    
    # Add a delay before fetching each token
    # Note: This function queries and updates the database!
    # Do not respond to the presence of new data as it may have delays.
    # Respond to the reduction or absence of previously present data only or you will see odd interactions
    time.sleep(0.01)
    
    return trades
    #This is returns the trade list array from our typscript file
    #order is 
    #(
        #ID int
        #type Transaction = {
        #    price: number;
        #    volume: number; *1,000,000 remember the value is larger
        #    state: number; // 1 for Active, 0 for Not Active
        #    type: number; // 0 for Buy, 1 for Sell
        #};
    #)

# Example usage
#token_id = '0x55cbe228505461bf3307a4f1ed951d0a059dd6d0'  # Replace with the actual token ID
#trades = fetch_all_trades(token_id)
#for trade in trades:
#    print(trade)




def generate_request(symbol, request_type, price, counts):
# Create the request dictionary
    count = int(counts * 1000000)
    request_dict = {
        "request": {
            "symbol": symbol,
            "requestType": request_type,
            "price": price,
            "count": count
        }
    }
        # Calculate the amount based on request type
    if request_type == "BUY_TOKEN":
        amount = int(price * count)
    elif request_type == "SELL_TOKEN":
        amount = int(count)
    else:
        raise ValueError("Invalid request type")
    # Convert the dictionary to JSON string
    metadata = json.dumps(request_dict, indent=2)

    # Remove newline characters from the string
    metadata = metadata.replace('\n', '')

    return metadata, amount

#Example usage:
#symbol = "FEE" #must be all caps
#request_type = "BUY_TOKEN" #request_type = "SELL_TOKEN" is an alternative for the order type
#price = 0.131
#count = 10 #this is the ammount of native token not smr

#metadata, amount = generate_request(symbol, request_type, price, count)
#print("metadata JSON:")
#print(metadata)
#print("Amount:", amount)


