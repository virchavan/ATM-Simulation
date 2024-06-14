import pandas as pd
import hashlib
from datetime import datetime, timedelta
import random
import pytz
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
list2 = []
def generate_pin():
    
    pin = random.randint(1000, 9999)
    pin_str = str(pin)
    list2.append(pin_str)
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
print(list2)
print(len(list2))
df = pd.DataFrame(data)
file_path = "/content/FinalData1.1.csv"
print(df)

bank_worker_credentials = {
    'worker_id': 'bank123',
    'password': 'bank@2024'
}

atm_notes = {
    '100': {'count': 2000, 'limit': 4000},
    '200': {'count': 1500, 'limit': 3000},
    '500': {'count': 1000, 'limit': 2000}
}

class ATM:
    def __init__(self, df, file_path,ist):
        self.df = df.sort_values('Card Number').reset_index(drop=True)
        self.file_path = file_path
        self.ist=ist

    def unblock_card_if_needed(self, card_index):
        if self.df.at[card_index, 'Status'] == 'Blocked':
            blocked_time = self.df.at[card_index, 'Blocked Time']
            if blocked_time and datetime.now() >= blocked_time + timedelta(hours=24):
                self.df.at[card_index, 'Status'] = 'Unblocked'
                self.df.at[card_index, 'Blocked Time'] = None
                print("Your card has been unblocked after 24 hours.")

    def hash_pin(self, pin):
        return hashlib.sha256(pin.encode()).hexdigest()

    def pin_verification(self, card_index):
        attempts = 3
        while attempts > 0:
            entered_pin = input("Enter your PIN: ")
            hashed_pin = self.hash_pin(entered_pin)
            if hashed_pin == self.df.at[card_index, 'PIN']:
                print("PIN verified successfully.")
                return True
            else:
                attempts -= 1
                print(f"Incorrect PIN. You have {attempts} attempts left.")
        else:
            print("Your card has been blocked due to 3 incorrect PIN attempts.")
            self.df.at[card_index, 'Status'] = 'Blocked'
            self.df.at[card_index, 'Blocked Time'] = datetime.now()
            return False

    def binary_search_card_number(self, card_number):
        left, right = 0, len(self.df) - 1
        while left <= right:
            mid = (left + right) // 2
            if self.df.at[mid, 'Card Number'] == card_number:
                return mid
            elif self.df.at[mid, 'Card Number'] < card_number:
                left = mid + 1
            else:
                right = mid - 1
        return None

    def simulate(self):
        while True:
            card_number = input("Enter your card number: ")
            card_index = self.binary_search_card_number(card_number)
            if card_index is None:
                print("Card not found!")
                continue

            self.unblock_card_if_needed(card_index)

            if self.df.at[card_index, 'Status'] == 'Blocked':
                print("This card is blocked.")
                continue

            if self.pin_verification(card_index):
                atm_operations = ATMOperations(self.df, card_index, self.file_path,self.ist)
                atm_operations.perform_operations()

class ATMOperations(ATM):
    def __init__(self, df, card_index, file_path,ist):
        super().__init__(df, file_path,ist)
        self.card_index = card_index
        self.ist=ist
    def perform_operations(self):
        while True:
            print("\nATM Menu:")
            print("1. Change PIN")
            print("2. Withdraw Money")
            print("3. Deposit Money")
            print("4. Check Available Balance")
            print("5. See Last Transaction")
            print("6. Bank Worker Access")
            print("7. Exit")
            choice = int(input("Enter your choice: "))

            if choice == 1:
                self.change_pin()
                break
            elif choice == 2:
                self.withdraw_money()
                break
            elif choice == 3:
                self.deposit_money()
                break
            elif choice == 4:
                self.check_balance()
                break
            elif choice == 5:
                self.view_last_transaction()
                break
            elif choice == 6:
                self.bank_worker_access()
                break
            elif choice == 7:
                print("Thank you for using the ATM.")
                return
            else:
                print("Invalid choice. Please try again.")
    def update_transaction_history(self, transaction_type, amount):
        transaction_time = datetime.now(self.ist).strftime('%Y-%m-%d %H:%M:%S')
        transaction = f"{transaction_type} of {amount} Rs at {transaction_time}"
        self.df.at[self.card_index, 'Transaction History'].append(transaction)

    def view_last_transaction(self):
        history = self.df.at[self.card_index, 'Transaction History']
        if history:
            print(f"Last transaction: {history[-1]}")
        else:
            print("No transactions yet.")

    def change_pin(self):
        pin = input('Enter your existing PIN: ')
        hash_pin = hashlib.sha256(pin.encode()).hexdigest()
        if hash_pin == self.df.at[self.card_index, 'PIN']:
            new_pin = input("Enter new PIN: ")
            if len(new_pin) == 4 and new_pin.isdigit():
                hashed_new_pin = self.hash_pin(new_pin)
                re_new_pin = input("Re-enter new PIN: ")
                hashed_re_new_pin = self.hash_pin(re_new_pin)
                if hashed_new_pin == hashed_re_new_pin:
                    self.df.at[self.card_index, 'PIN'] = hashed_new_pin
                    self.df.to_csv(self.file_path, index=False)
                    print("PIN changed successfully.")
                    self.update_transaction_history("PIN Change", 0)
                else:
                    print("New PIN and re-entered PIN do not match.")
            else:
                print("Invalid entry. New PIN must be 4 digits.")
        else:
            print("Invalid PIN")

    def withdraw_money(self):
        amount = float(input("Enter amount to withdraw: "))
        if amount % 100 != 0:
            print("Invalid entry. Amount should be a multiple of 100.")
            return

        e_pin = input('Enter your PIN: ')
        hashed_e_pin = hashlib.sha256(e_pin.encode()).hexdigest()
        if hashed_e_pin == self.df.at[self.card_index, 'PIN']:
            if amount > self.df.at[self.card_index, 'Balance']:
                print("Insufficient balance.")
            elif amount > self.df.at[self.card_index, 'DailyWithdrawLimit']:
                print("Daily withdrawal limit exceeded.")
            else:
                self.df.at[self.card_index, 'Balance'] -= amount
                print(f"Withdrawn {amount} Rs. New balance: {self.df.at[self.card_index, 'Balance']} Rs.")
                self.update_transaction_history("Withdrawal", amount)
                self.df.to_csv(self.file_path, index=False)
        else:
            print("Invalid PIN")

    def deposit_money(self):
        amount = float(input("Enter amount to deposit (in multiples of 100): "))
        if amount % 100 != 0:
            print("Please enter amount in multiples of 100.")
        else:
            self.df.at[self.card_index, 'Balance'] += amount
            print(f"Deposited {amount} Rs. New balance: {self.df.at[self.card_index, 'Balance']} Rs.")
            self.update_transaction_history("Deposit", amount)
            self.df.to_csv(self.file_path, index=False)

    def check_balance(self):
        print(f"Available balance: {self.df.at[self.card_index, 'Balance']} Rs.")

    def bank_worker_access(self):
        worker_id = input("Enter bank worker ID: ")
        password = input("Enter password: ")
        if worker_id == bank_worker_credentials['worker_id'] and password == bank_worker_credentials['password']:
            print("Access granted.")
            bank_worker = BankWorker(atm_notes)
            bank_worker.display_total_value()
            bank_worker.add_notes()
        else:
            print("Access denied. Invalid credentials.")

class BankWorker:
    def __init__(self, atm_notes):
        self.atm_notes = atm_notes

    def display_total_value(self):
        total_value = (
            self.atm_notes['100']['count'] * 100 +
            self.atm_notes['200']['count'] * 200 +
            self.atm_notes['500']['count'] * 500
        )
        print(f"Total value of cash in ATM: {total_value} Rs.")

    def add_notes(self):
        while True:
            print("\nAdd Notes Menu:")
            print("1. Add 100 Rs notes")
            print("2. Add 200 Rs notes")
            print("3. Add 500 Rs notes")
            print("4. Exit")
            choice = int(input("Enter your choice: "))

            if choice in [1, 2, 3]:
                denomination = '100' if choice == 1 else '200' if choice == 2 else '500'
                amount = int(input(f"Enter number of {denomination} Rs notes to add: "))
                if self.atm_notes[denomination]['count'] + amount > self.atm_notes[denomination]['limit']:
                    print("Not enough space for these notes.")
                else:
                    self.atm_notes[denomination]['count'] += amount
                    print(f"Added {amount} notes of {denomination} Rs. New count: {self.atm_notes[denomination]['count']}.")
            elif choice == 4:
                return
            else:
                print("Invalid choice. Please try again.")

# Example usage of the ATM simulation function
atm = ATM(df, file_path,ist)
atm.simulate()

