import time
import os
import pandas as pd
from colorama import Fore
print(Fore.LIGHTGREEN_EX)

# Banking Program
# The small edits I've made to the original file are just general best practices
# such as constants being in capitals, using print() instead of print('\n'),
# having 2 double clear lines between functions and the main code, etc.

# I've also added one or two comments saying where something could be done
# better (only to later find realise you have tried to loop it ha. gj.)

# import pandas to run csv, os to delete csv, time to delay input of password

csv_file = 'data.csv'
# I've used capitals here as it's a constant (not going to change).
# It's good practice to use captials for constants.
PASSWORD = 'ABC123'
MAX_ATTEMPTS = 3


# CSV actions - load, save and update data
def load_csv(file_name):
    try:
        return pd.read_csv(file_name)
    except FileNotFoundError:
        return pd.DataFrame(columns=['Transaction Type',
                                     'Amount',
                                     'Balance After Transaction'])


def save_csv(data, file_name):
    data.to_csv(file_name, index=False)
    print(f'Data saved to {file_name}')


def update_data(data, transaction_type, amount, balance):
    new_row = {
        'Transaction Type': transaction_type,
        'Amount': f'£{amount:.2f}',
        'Balance After Transaction': f'£{balance:.2f}'
    }
    return pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)


def show_bal(data):
    if data.empty:
        print('No transaction history available. Starting balance is £0.00')
    else:
        latest_balance = data.iloc[-1]['Balance After Transaction']
        print(f'Your current balance is {latest_balance}')


# Delete history
def remove_history():
    try:
        if os.path.exists(csv_file):
            os.remove(csv_file)     # Remove the file.
            print(f'{csv_file} has been deleted.')
    except FileNotFoundError:
        print(f'Error: {csv_file} was not found.')
    except PermissionError:
        print(f'Error: Permission denied while trying to delete {csv_file}.')
    except OSError as os_error:
        print(
            f'Error: {os_error} occurred while trying to delete {csv_file}: {os_error.strerror}')
    except SystemError as sys_error:
        print(
            f'Error: {sys_error} occurred while trying to delete {csv_file}: {sys_error}')


# Enter deposit
def deposit(data):
    try:
        amount = float(input('Enter amount you would like to deposit: '))
        if amount < 0:
            raise ValueError('Negative amount entered.')
            # This needs to be in a loop of some kind to keep asking
            # for a positive number.
        # Get the latest balance.
        balance = 0 if data.empty else (
            data.iloc[-1]['Balance After Transaction'].strip('£'))
        balance += amount
        print()  # Does the same as print('\n')
        print(
            f'You have deposited £{amount:.2f}. New balance is £{balance:.2f}')
        return update_data(data, 'Deposit', amount, balance)
    except ValueError:
        print()
        print('Invalid input. Please enter a positive number.')
        return data


# Enter withdraw cash
def withdraw(data):
    try:
        print()
        amount = float(input('Enter amount you would like to withdraw: £ '))
        # Get the latest balance.
        balance = 0 if data.empty else float(
            data.iloc[-1]['Balance After Transaction'].strip('£'))
        if amount > balance:
            print()
            print('**********************')
            print('Insufficient funds')
            print('**********************')
        else:
            balance -= amount
            print()
            print('**********************')
            print(
                f'You have withdrawn £{amount:.2f}. New balance is £{balance:.2f}')
            print('**********************')
            return update_data(data, 'Withdraw', amount, balance)
    except ValueError:
        print()
        print('Invalid input. Please enter a positive number.')
        return data


# load csv file with current balance
def main():
    is_running = True
    data = load_csv(csv_file)

    # User interface to define input choices
    while is_running:
        print('1. Show Balance')
        print('2. Deposit Cash')
        print('3. Withdraw Cash')
        print('4. View Transaction History')
        print('5. Remove Transaction History')
        print('6. Exit')

        choice = input('Enter your choice 1 - 6: ')

        if choice == '1':
            show_bal(data)
            print()
        elif choice == '2':
            data = deposit(data)
            print()
        elif choice == '3':
            data = withdraw(data)
            print()
        elif choice == '4':
            print()
            print('Transaction History')
            print(data)
        elif choice == '5':
            remove_history()
            print('Transaction history has been removed.')
        elif choice == '6':
            save_csv(data, csv_file)
            is_running = False
        else:
            print()
            print('Invalid choice. Please try again.')


if __name__ == '__main__':
    for attempt in range(0, MAX_ATTEMPTS):
        pw = input(f'Attempt {attempt}/{MAX_ATTEMPTS}: Enter password: ')
        if pw == PASSWORD:
            main()
        else:
            print('Incorrect password. Please try again.')
            time.sleep(1)

    print()
    print('**********************')
    print('Goodbye!')
