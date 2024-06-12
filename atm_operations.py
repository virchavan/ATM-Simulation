import hashlib
from datetime import datetime
import pytz
from bank_worker import BankWorker

class ATMOperations:
    def __init__(self, df, card_index, file_path, ist, bank_worker_credentials, atm_notes):
        self.df = df
        self.card_index = card_index
        self.file_path = file_path
        self.ist = ist
        self.bank_worker_credentials = bank_worker_credentials
        self.atm_notes = atm_notes

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
            elif choice == 2:
                self.withdraw_money()
            elif choice == 3:
                self.deposit_money()
            elif choice == 4:
                self.check_balance()
            elif choice == 5:
                self.view_last_transaction()
            elif choice == 6:
                self.bank_worker_access()
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
        hashed_pin = hashlib.sha256(pin.encode()).hexdigest()
        if hashed_pin == self.df.at[self.card_index, 'PIN']:
            new_pin = input("Enter new PIN: ")
            if len(new_pin) == 4 and new_pin.isdigit():
                hashed_new_pin = hashlib.sha256(new_pin.encode()).hexdigest()
                re_new_pin = input("Re-enter new PIN: ")
                hashed_re_new_pin = hashlib.sha256(new_pin.encode()).hexdigest()
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
        if worker_id == self.bank_worker_credentials['worker_id'] and password == self.bank_worker_credentials['password']:
            print("Access granted.")
            bank_worker = BankWorker(self.atm_notes)
            bank_worker.display_total_value()
            bank_worker.add_notes()
        else:
            print("Access denied. Invalid credentials.")
