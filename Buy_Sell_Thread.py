import threading
import random
import json
import time

transactions = []
transaction_index = 0
index_lock = threading.Lock()

names = [
    "Model_A", "Model_B", "Model_C", "Model_D", "Model_E",
    "Model_F", "Model_G", "Model_H", "Model_I", "Model_J"
]

total_energy_saved = 0
total_cost_saved = 0
savings_lock = threading.Lock()

# Constants for environmental impact and efficiency rating
CO2_EMISSION_PER_ENERGY = 0.5  # Example: 0.5 kg CO2 per energy unit saved
EFFICIENT_THRESHOLD = 100  # Threshold for efficiency rating
total_energy_used = 0  # Total energy used for efficiency calculation

def calculate_cost(energy):
    return energy * 10

def calculate_environmental_impact(energy):
    return energy * CO2_EMISSION_PER_ENERGY

def calculate_efficiency_rating(total_energy_saved):
    if total_energy_saved >= EFFICIENT_THRESHOLD:
        return "Highly Efficient"
    elif total_energy_saved >= EFFICIENT_THRESHOLD / 2:
        return "Moderately Efficient"
    elif total_energy_saved < EFFICIENT_THRESHOLD and total_energy_saved > 0:
        return "Needs Improvement"
    else:
        return "CRITICAL SITUATION!"

def buy_shares(start_time, end_time):
    global transaction_index, total_energy_saved, total_cost_saved
    while time.time() < end_time:
        amount = random.randint(1, 100)
        name = random.choice(names)
        with index_lock:
            cost = calculate_cost(amount)
            transaction = {
                'index': transaction_index,
                'Name': name,
                'Energy': amount,
                'Cost': cost
            }
            transactions.append(transaction)
            transaction_index += 1
            
            with savings_lock:
                total_energy_saved += amount
                total_cost_saved += cost

        print(f"Bought {amount} shares at cost {cost}. Total Transactions: {len(transactions)}")
        print(f"Total Energy Saved: {total_energy_saved}, Total Cost Saved: {total_cost_saved}")
        time.sleep(random.uniform(0.1, 1))

def sell_shares(start_time, end_time):
    global transaction_index, total_energy_saved, total_cost_saved, total_energy_used
    while time.time() < end_time:
        amount = random.randint(1, 100)
        name = random.choice(names)
        with index_lock:
            cost = calculate_cost(amount)
            transaction = {
                'index': transaction_index,
                'Name': name,
                'Energy': amount,
                'Cost': cost
            }
            transactions.append(transaction)
            transaction_index += 1
            
            with savings_lock:
                total_energy_used += amount  # Track energy used for efficiency rating
                total_energy_saved += amount
                total_cost_saved += cost

        print(f"Sold {amount} shares using {name} at cost {cost}. Total Transactions: {len(transactions)}")
        print(f"Total Energy Saved: {total_energy_saved}, Total Cost Saved: {total_cost_saved}")
        time.sleep(random.uniform(0.1, 1))

def save_to_json(start_time, end_time):
    while time.time() < end_time:
        time.sleep(5)

    try:
        # Calculate summary data
        average_money_saved = total_cost_saved / transaction_index if transaction_index > 0 else 0
        total_environmental_impact = calculate_environmental_impact(total_energy_saved)
        efficiency_rating = calculate_efficiency_rating(total_energy_saved)

        # Prepare the summary data
        summary_data = {
            "transactions": transactions,
            "average_money_saved": average_money_saved,
            "total_environmental_impact": total_environmental_impact,
            "efficiency_rating": efficiency_rating
        }

        with open('Data.json', 'w') as json_file:
            json.dump(summary_data, json_file, indent=4)

        print("Data saved to Data.json.")
        
    except Exception as e:
        print(f"An error occurred: {e}")

Total_transactions = 10 
start_time = time.time()
end_time = start_time + Total_transactions

buy_thread = threading.Thread(target=buy_shares, args=(start_time, end_time))
save_thread = threading.Thread(target=save_to_json, args=(start_time, end_time))
sell_thread = threading.Thread(target=sell_shares, args=(start_time, end_time))

buy_thread.start()
sell_thread.start()
save_thread.start()

buy_thread.join()
sell_thread.join()
save_thread.join()

average_money_saved = total_cost_saved / transaction_index if transaction_index > 0 else 0
total_environmental_impact = calculate_environmental_impact(total_energy_saved)
efficiency_rating = calculate_efficiency_rating(total_energy_saved)

print(f"\nAverage Money Saved: {average_money_saved:.2f}")
print(f"Total Environmental Impact Reduced (CO2 kg): {total_environmental_impact:.2f}")
print(f"Energy Efficiency Rating: {efficiency_rating}")
