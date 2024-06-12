import pandas as pd
import random
import hashlib
import os
from datetime import datetime
import pytz
from atm import ATM

ist = pytz.timezone('Asia/Kolkata')

# Initial data setup
indian_names = [
    "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Ayaan",
    "Krishna", "Ishaan", "Shaurya", "Atharv", "Dhanush", "Aaditya", "Veer",
    "Laksh", "Arnav", "Yash", "Moksh", "Dhruv", "Ananya", "Aadhya", "Diya",
    "Myra", "Aarohi", "Ira", "Anaya", "Sara", "Saanvi", "Aadhira", "Avni",
    "Jiya", "Prisha", "Riya", "Kiara", "Ishita", "Aanya", "Navya", "Pari",
    "Aaradhya", "Swara", "Misha", "Eva", "Khushi", "Anvi", "Nisha", "Arya",
    "Ridhi", "Tanvi"
]

def generate_card_number():
    return "".join([str(random.randint(0, 9)) for _ in range(16)])
list1=[]
def generate_pin():
    pin = random.randint(1000, 9999)
    list1.append(pin)
    pin_str = str(pin)
    return hashlib.sha256(pin_str.encode()).hexdigest()

def generate_balance():
    return round(random.uniform(1000, 1000000), 2)

def generate_card_status():
    return 'Unblocked'

def generate_withdraw_limit():
    return random.choice([20000, 40000, 100000])

def generate_blocked_time():
    return None

def generate_transaction_history():
    return []

num_records = 10000
data = {
    "CustomerName": [random.choice(indian_names) for _ in range(num_records)],
    "Card Number": [generate_card_number() for _ in range(num_records)],
    "PIN": [generate_pin() for _ in range(num_records)],
    "Status": [generate_card_status() for _ in range(num_records)],
    "Balance": [generate_balance() for _ in range(num_records)],
    "DailyWithdrawLimit": [generate_withdraw_limit() for _ in range(num_records)],
    "Blocked Time": [generate_blocked_time() for _ in range(num_records)],
    "Transaction History": [generate_transaction_history() for _ in range(num_records)]
}
print(list1[:5])
df = pd.DataFrame(data)
file_path = "FinalData1.1.csv"
print(df)
# Ensure the directory exists
output_dir = os.path.dirname(file_path)
if output_dir and not os.path.exists(output_dir):
    os.makedirs(output_dir)

df.to_csv(file_path, index=False)

bank_worker_credentials = {
    'worker_id': 'bank123',
    'password': 'bank@2024'
}

atm_notes = {
    '100': {'count': 2000, 'limit': 4000},
    '200': {'count': 1500, 'limit': 3000},
    '500': {'count': 1000, 'limit': 2000}
}

# Start the ATM simulation
atm = ATM(df, file_path, ist, bank_worker_credentials, atm_notes)
atm.simulate()
