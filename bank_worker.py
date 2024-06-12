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
