import threading
import random
import json
import time

transactions = []
transaction_index = 0
index_lock = threading.Lock()  

def buy_shares(start_time, end_time):
    global transaction_index
    while time.time() < end_time:
        amount = random.randint(1, 100)
        with index_lock:
            transaction = {
                'index': transaction_index,
                'type': 'buy',
                'amount': amount,
                'time': time.time()
            }
            transactions.append(transaction)
            transaction_index += 1
        print(f"Bought {amount} shares. Total Transactions: {len(transactions)}")
        time.sleep(random.uniform(0.1, 1))

def sell_shares(start_time, end_time):
    global transaction_index
    while time.time() < end_time:
        amount = random.randint(1, 100)
        with index_lock:
            transaction = {
                'index': transaction_index,
                'type': 'sell',
                'amount': amount,
                'time': time.time()
            }
            transactions.append(transaction)
            transaction_index += 1
        print(f"Sold {amount} shares. Total Transactions: {len(transactions)}")
        time.sleep(random.uniform(0.1, 1))
def save_to_json(start_time, end_time):
    while time.time() < end_time:
        try:
            try:
                with open('Data.json', 'r+') as json_file:
                    try:
                        existing_data = json.load(json_file)
                    except json.JSONDecodeError:
                        existing_data = []  
                    if not isinstance(existing_data, list):
                        existing_data = []
            except FileNotFoundError:
                existing_data = []

            existing_data.extend(transactions)
            with open('Data.json', 'w') as json_file:
                json.dump(existing_data, json_file, indent=4)  

            print("Data saved to Data.json.")
            

        except Exception as e:
            print(f"An error occurred: {e}")

        time.sleep(5)

# Set the duration for the threads to run (in seconds)
Total_transactions = 10 
start_time = time.time()
end_time = start_time + Total_transactions

# Create and start threads
buy_thread = threading.Thread(target=buy_shares, args=(start_time, end_time))
save_thread = threading.Thread(target=save_to_json, args=(start_time, end_time))
sell_thread = threading.Thread(target= sell_shares, args=(start_time, end_time))
buy_thread.start()
sell_thread.start()
save_thread.start()

