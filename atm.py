import hashlib
import pandas as pd
from datetime import datetime, timedelta
import pytz
from atm_operations import ATMOperations
from bank_worker import BankWorker

class ATM:
    def __init__(self, df, file_path, ist, bank_worker_credentials, atm_notes):
        self.df = df.sort_values('Card Number').reset_index(drop=True)
        self.file_path = file_path
        self.ist = ist
        self.bank_worker_credentials = bank_worker_credentials
        self.atm_notes = atm_notes

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
                atm_operations = ATMOperations(self.df, card_index, self.file_path, self.ist, self.bank_worker_credentials, self.atm_notes)
                atm_operations.perform_operations()
