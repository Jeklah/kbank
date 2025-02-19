import time
import os
import pandas as pd
from colorama import Fore


print(Fore.LIGHTGREEN_EX)

CSV_FILE = 'data.csv'
PASSWORD = 'ABC123'
MAX_ATTEMPTS = 3


def get_input_in_range(min_val, max_val):
    """
    Get input within a range

    :param min_val: int
    :param max_val: int

    :return: int
    """
    while True:
        try:
            choice = int(input('Enter your choice: '))
            if min_val <= choice <= max_val:
                return choice
            print(f'Please enter a number between {min_val} and {max_val}')
        except ValueError:
            print('Invalid input. Please enter a number.')


def load_csv(file_name):
    """
    Load CSV file to a pandas DataFrame

    :param file_name: str

    :return: pandas.DataFrame
    """
    try:
        with open(file_name, 'r') as file:
            return pd.read_csv(file)
    except FileNotFoundError:
        return pd.DataFrame(columns=['Transaction Type',
                                     'Amount',
                                     'Balance After Transaction'])
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=['Transaction Type',
                                     'Amount',
                                     'Balance After Transaction'])


def save_csv(data, file_name):
    """
    Save data to a CSV file

    :param data: pandas.DataFrame
    :param file_name: str
    """
    try:
        with open(file_name, 'w') as file:
            data.to_csv(file_name, index=False)
        print(f'Data saved to {file_name}')
    except Exception as err:
        print(f'Error saving data: {err}')


def update_data(data, transaction_type, amount, balance):
    """
    Update data with new transaction

    :param data: pandas.DataFrame
    :param transaction_type: str
    :param amount: float
    :param balance: float

    :return: pandas.DataFrame
    """
    new_row = {
        'Transaction Type': transaction_type,
        'Amount': f'£{amount:.2f}',
        'Balance After Transaction': f'£{balance:.2f}'
    }
    return pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)


def get_balance(data):
    """
    Get the current balance

    :param data: pandas.DataFrame

    :return: float
    """
    if not data.empty:
        # Ensure it's a string
        balance_str = str(data.iloc[-1]['Balance After Transaction'])
        return float(balance_str.strip('£')) if balance_str.startswith('£') else float(balance_str)
    return 0.0


def show_balance(data):
    """
    Show the current balance

    :param data: pandas.DataFrame
    """
    balance = get_balance(data)
    print(f'Your current balance: £{balance:.2f}')


def deposit(data):
    """
    Handle deposit transaction

    :param data: pandas.DataFrame

    :return: pandas.DataFrame
    """
    while True:
        try:
            amount = get_input_in_range(0.01, float('inf'))

            if amount > 0:
                break
            print('Deposit amount must be positive. Please try again.')
            balance = get_balance(data) + amount
        except ValueError:
            print('Invalid input. Please enter a numeric value.')

    balance = get_balance(data) + amount
    print(
        f'You have deposited £{amount:.2f}. Your new balance is £{balance:.2f}'
    )
    return update_data(data, 'Deposit', amount, balance)


def withdraw(data):
    """
    Handle withdraw transactions

    :param data: pandas.DataFrame

    :return: pandas.DataFrame
    """
    while True:
        try:
            amount = float(input('Enter the withdrawal amount: £ '))
            if amount <= 0:
                print('Withdrawal amount must be positive. Please try again.')
                continue
            balance = get_balance(data)
            if amount > balance:
                print('Insufficient funds.')
                return data
            break
        except ValueError:
            print('Invalid input. Please enter a numeric value.')

    balance -= amount
    print(
        f'You have withdrawn £{amount:.2f}. Your new balance is £{balance:.2f}'
    )
    return update_data(data, 'Withdraw', amount, balance)


def remove_history():
    """
    Remove the transaction history file

    NOTE: This function is destructive as it removes the transaction history
          file without any confirmation, which also stores the current balance.
          It would be a good idea to implement a seperate file to store the
          history of transactions. This way, the transaction history can be
          removed without affecting the current balance.
    """
    try:
        os.remove(CSV_FILE)
        print('Transaction history removed.')
    except FileNotFoundError:
        print('No transaction history found.')
    except Exception as err:
        print(f'Error removing transaction history: {err}')


def main():
    """
    Main function loop.
    """
    data = load_csv(CSV_FILE)

    print()
    print('1. Show Balance')
    print('2. Deposit Cash')
    print('3. Withdraw Cash')
    print('4. View Transaction History')
    print('5. Remove Transaction History')
    print('6. Exit')
    while True:
        choice = get_input_in_range(1, 6)

        if choice == 1:
            show_balance(data)
        elif choice == 2:
            data = deposit(data)
        elif choice == 3:
            data = withdraw(data)
        elif choice == 4:
            print()
            print('Transaction History')
            print('No transactions' if data.empty else data)
        elif choice == 5:
            print('This functionality has been temporarily disabled.')
            # remove_history()
            # data = pd.DataFrame(
            #    columns=['Transaction Type',
            #             'Amount',
            #             'Balance After Transaction']
            # )
        elif choice == 6:
            save_csv(data, CSV_FILE)
            print('Exiting...')
            break


if __name__ == '__main__':
    for attempt in range(1, MAX_ATTEMPTS + 1):
        if input(f'Attempt {attempt}/{MAX_ATTEMPTS}: Enter password: ') == PASSWORD:
            main()
            break
        else:
            print('Incorrect password. Please try again.')
            time.sleep(1)
    else:
        print('Maximum attempts reached. Exiting...')
