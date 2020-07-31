import random
import sqlite3

# create connection and cursor for db
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()


# create table
cur.execute("""CREATE TABLE IF NOT EXISTS card(
id INTEGER PRIMARY KEY, 
number TEXT, 
pin TEXT, 
balance INTEGER DEFAULT  0)""")
conn.commit()


# insert new values in table
def insert_values(num, pin):
    cur.execute('INSERT INTO card(number, pin) VALUES (?, ?)', (num, pin))
    conn.commit()


# Add income to balance
def add_income(new_income, card_num):
    cur.execute('UPDATE card SET balance = balance + ? WHERE number = ?', (new_income, card_num))
    conn.commit()


# decrease money in balance
def decrease_balance(money, card_num):
    cur.execute('UPDATE card SET balance = balance - ? WHERE number = ?', (money, card_num))
    conn.commit()


# close bank account
def close_account(card_num):
    cur.execute("DELETE FROM card WHERE number = ?", (card_num, ))
    conn.commit()
    print("The account has been closed!")


# check if card number is in database
def check_number(card_num):
    cur.execute('SELECT number FROM card WHERE number = ?', (card_num, ))
    return cur.fetchone() is not None


# check if pin is correct
def check_pin(card_num, pin_num):
    cur.execute("SELECT pin FROM card WHERE number = ?", (card_num, ))
    return cur.fetchone()[0] == pin_num


# Transfer money from one bank account to another
def do_transfer(first_card):
    print("Transfer")
    trans_card = input("Enter card number:\n")
    luth_num = trans_card[:15] + luhn_alg(trans_card[:15])
    if luth_num != trans_card:
        print("Probably you made mistake in the card number. Please try again!")
    elif not check_number(trans_card):
        print("Such a card does not exist.")
    else:
        money = int(input("Enter how much money you want to transfer:\n"))
        cur.execute('SELECT balance FROM card WHERE number = ?', (first_card, ))
        if money > int(cur.fetchone()[0]):
            print("Not enough money!")
        else:
            decrease_balance(money, first_card)
            add_income(money, trans_card)
            print("Success!")


# get last number on card number with luhn algorithm
def luhn_alg(number):
    num_list = []
    final_number = 0
    for i in range(len(number)):
        if i % 2 == 0:
            num_list.append(int(number[i]) * 2)
        else:
            num_list.append(int(number[i]))
    for j in num_list:
        if j >= 10:
            final_number += j - 9
        else:
            final_number += j
    if final_number % 10 == 0:
        final_number = 0
    else:
        final_number = 10 - final_number % 10
    return str(final_number)


# creates new account with card number and pin number
def create_account():
    num = ""
    for i in range(9):
        num += str(random.randint(0, 9))
    card_number = "400000" + num + luhn_alg("400000" + num)
    pin_number = ""
    for i in range(4):
        pin_number += str(random.randint(0, 9))
    print("Your card has been created")
    print(f"Your card number: \n{card_number}")
    print(f"Your card PIN: \n{pin_number}")
    insert_values(card_number, pin_number)


# enter logged menu
def logged_menu(card_num):
    while True:
        option = input("1. Balance \n2. Add income \n3. Do transfer \n4. Close account \n5. Log out \n0. Exit \n")
        if option == "1":
            cur.execute('SELECT balance FROM card WHERE number = ?', (card_num, ))
            print("Balance: {}".format(cur.fetchone()[0]))
        elif option == "2":
            income = input("Enter income:\n")
            add_income(income, card_num)
            print("Income was added!")
        elif option == "3":
            do_transfer(card_num)
        elif option == "4":
            close_account(card_num)
            break
        elif option == "5":
            print("You have successfully logged out! \n")
            break
        else:
            print("Bye!")
            quit()


# login into account
def login():
    card_input = input("Enter your card number: \n")
    pin_input = input("Enter your PIN: \n")
    if not check_number(card_input):
        print("Wrong card number or PIN! \n")
    elif check_pin(card_input, pin_input):
        print("You have successfully logged in! \n")
        logged_menu(card_input)
    else:
        print("Wrong card number or PIN! \n")


while True:
    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")
    menu_choice = input()
    if menu_choice == "1":
        create_account()
        continue
    elif menu_choice == "2":
        login()
        continue
    elif menu_choice == "0":
        print("Bye!")
        # cur.execute('SELECT * FROM card')
        # print(cur.fetchall())
        conn.close()
        break
    else:
        continue
