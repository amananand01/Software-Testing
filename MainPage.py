import os
import sys
import getpass
import sqlite3
import re
from argparse import ArgumentParser
from customer import *
from Agent import *

DBpath = "./miniproject.db"

def validateLogInInfo(info):
    return re.match("^[A-Za-z0-9_]*$", info)

def getMainMenuSelection():

    ''' Gets the Page Selection'''
    print("Please choose an option: ")
    print("1. Sign in as customer")
    print("2. Sign in as agent")
    print("3. Register as new customer")
    print("4. Exit the program")

    PageSelection = int(input())

    while PageSelection < 0 and PageSelection > 4:
        print("Not a valid choice. Please enter selection again")
        PageSelection = int(input())

    return PageSelection;



def MainMenu():
    ''' Main Menu Loop '''
    while (True):
        #os.system('cls' if os.name == 'nt' else 'clear')
        selection = getMainMenuSelection()

        if selection == 1:
            SignInCustomer()
        elif selection == 2:
            SignInAgent()
        elif selection == 3:
            RegisterCustomer()
        elif selection == 4:
            exitProgram()

def RegisterCustomer():
    print("Register Customer Page")

    ''' Customer registration page. Validates required input
        and registers the customer '''

    # make sure valid cid is entered
    print("Please enter a unique cid:")
    cid = input().strip()
    cidSearchResult = cidSearch(cid)
    while len(cidSearchResult) > 0 or not validateLogInInfo(cid):
        print("Please enter a valid and unique cid")
        cid = input().strip()
        cidSearchResult = cidSearch(cid)

    # Enter name, address and password
    CustomerInfo = {}
    CustomerInfo["cid"] = cid
    print("Please enter your name:")
    CustomerInfo["name"] = input().strip()
    print("Please enter your address:")
    CustomerInfo["address"] = input().strip()

    # password shouldn't be visible while typed
    CustomerInfo["pwd"] = getpass.getpass("Enter your password: ").strip()
    while (len(CustomerInfo["pwd"]) <= 0 or not validateLogInInfo(CustomerInfo["pwd"])):
        print("Please enter a valid password")
        CustomerInfo["pwd"] = getpass.getpass("Enter your password: ").strip()

    #saving the entry into the database
    SaveCustomer(CustomerInfo)

def cidSearch(cid):
    ''' Searches for cid in the database and returns all matching tuples '''
    conn = sqlite3.connect(DBpath)
    cursor = conn.cursor()
    cursor.execute("Select * from customers Where cid=:cid", {"cid":cid})
    cidSearchResult = cursor.fetchall()
    conn.close()
    return cidSearchResult

def aidSearch(aid):
    ''' Searches for aid in the database and returns all matching tuples '''
    conn = sqlite3.connect(DBpath)
    cursor = conn.cursor()
    cursor.execute("Select * from agents Where aid=:aid", {"aid":aid})
    cidSearchResult = cursor.fetchall()
    conn.close()
    return cidSearchResult

def SaveCustomer(CustomerInfo):
    ''' Takes in a dictionary of customer info as parameter
        and saves the information into the database '''
    conn = sqlite3.connect(DBpath)
    cursor = conn.cursor()
    cursor.execute("Insert into customers values (?, ?, ?, ?)", (CustomerInfo["cid"], CustomerInfo["name"], CustomerInfo["address"],CustomerInfo["pwd"]))
    conn.commit()
    conn.close()
    return

def SignInAgent():
    print("Agent Sign-in Page")

    ''' The sign-in page for agents, ensures a valid aid is entered
        and if matching password is entered goes to customer page '''

    print("Please enter a valid aid:")
    aid = input().strip()
    AgentInfo = aidSearch(aid)
    while not AgentInfo or not validateLogInInfo(aid):
        print("The aid doesn't exist. Please enter a valid aid:")
        aid = input().strip()
        AgentInfo = aidSearch(aid)

    password = AgentInfo[0][2]
    #get the password and check for match
    PasswordInput = getpass.getpass("Please enter your password: ").strip()
    while PasswordInput != password or not validateLogInInfo(PasswordInput):
        PasswordInput = getpass.getpass("Incorrect Password. Please try again: ").strip()

    # authentication complete
    # calling the CustomerPage function with string cid as parameter

    print("Signed in as agent")
    Agent(DBpath)

def SignInCustomer():
    print("Customer Sign-in Page")

    ''' The sign-in page for customers, ensures a valid cid is entered
        and if matching password is entered goes to customer page '''

    print("Please enter a valid cid:")
    cid = input().strip()
    CustomerInfo = cidSearch(cid)
    while not CustomerInfo or not validateLogInInfo(cid):
        print("The cid doesn't exist. Please enter a valid cid")
        cid = input().strip()
        CustomerInfo = cidSearch(cid)

    password = CustomerInfo[0][3]
    # get the password and check for match
    PasswordInput = getpass.getpass("Please enter your password: ").strip()
    while PasswordInput != password or not validateLogInInfo(PasswordInput):
        PasswordInput = getpass.getpass("Incorrect Password. Please try again: ").strip()

    # authentication complete
    # calling the CustomerPage function with string cid as parameter
    Customer(cid, DBpath)


def exitProgram():
    sys.exit()

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", dest="myFile", help="Open specified file")
    args = parser.parse_args()
    DBpath = args.myFile
    MainMenu()
