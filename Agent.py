import sqlite3
import time
import datetime
from random import randint
import sys

connection = None
cursor = None

def connect(path):
    global connection, cursor
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return

def Agent(path=""):
    global connection,cursor
    connect(path)

    while True:
        print('\nThis is agents site\n')
        print('1.Set up a delivery')
        print('2.Update a delivery')
        print('3.Add to stock')
        print('4.Log out')

        while True:
            choice = input("Select from the above options: ")
            if choice not in ["1","2","3","4"]:
                print("\nWrong Input please try again\n")
                continue
            choice=int(choice)
            break
        if choice == 1:
            print("In Set up a delivery")
            orderid = int(input("please enter an order id: "))
            print("Please enter the pickuptime")
            pickuptime = enter_date()
            print("Please enter the dropfftime")
            dropofftime = enter_date()
            agents_set_order(orderid,pickuptime,dropofftime)
            print("\nDelivery set up successful\n")
        elif choice == 2:
            print("In Update a delivery")
            trackingNo = int(input("Enter the trancking number: "))
            agents_update_order(trackingNo)
            print("\nDelivery updated\n")
        elif choice == 3:
            print("In Add to Stock")
            while (True):
                storeid = int(input("Enter the store id: "))
                product_id = input("Enter the product_id: ")
                data = find_carries(storeid,product_id)
                if (len(data) == 0):
                    continue
                else:
                    break
            agents_add_stock(storeid,product_id)
            print("\nAdded to Stock\n")
        elif choice == 4:
            return
    connection.commit()
    connection.close()

    return

def find_store(storeid):
    global connection, cursor
    all_stores = []
    storeid = (storeid,)
    cursor.execute('SELECT * FROM stores WHERE sid = ?; ' ,storeid)
    rows  = cursor.fetchall()
    for each in rows:
        all_stores.append(each)
    return all_stores

def find_product(product_id):
    global connection, cursor
    all_products = []
    product_id = (product_id , )
    cursor.execute('SELECT * FROM products p WHERE p.pid = ?;' , product_id)
    rows = cursor.fetchall()
    for each in rows:
        all_products.append(each)
    return all_products

def find_carries(store_id,product_id):
    global connection, cursor
    all_carries = []
    key = (store_id ,product_id , )
    cursor.execute('SELECT * FROM carries c WHERE c.sid = ? AND c.pid = ?;' , key)
    rows = cursor.fetchall()
    for each in rows:
        all_carries.append(each)
    print(all_carries)
    return all_carries

def find_delevaries(Tracking_number):
    global connection, cursor
    all_deliveries = [ ]
    key  = (Tracking_number,)
    cursor.execute('SELECT * FROM deliveries WHERE trackingNo= ?;',key)
    rows = cursor.fetchall()
    for each in rows:
        all_deliveries.append(each)
    return (all_deliveries)

def deliveries_arrived(date):
    if (date == None):
        print("no dropoff date")
        return
    current_date = time.strftime("%Y-%m-%d %H:%M:%S")
    current_date = datetime.datetime.strptime(current_date,"%Y-%m-%d %H:%M:%S")
    date = datetime.datetime.strptime(date,"%Y-%m-%d %H:%M:%S" )
    if current_date >= date:
        print("arrived")
    else:
        print("not arrieved")
    return

def remove_data(Tracking_number , order_number):
    global connection, cursor
    data=(Tracking_number , order_number,)
    cursor.execute('DELETE FROM deliveries WHERE trackingNo = ? AND oid = ?',data )
    connection.commit()
    return

def enter_quantity():
    quantity = int(input("enter_quantity :"))
    return quantity

def random_with_N_digits():
    n=4
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def get_all_track_num():
    all_tracknum = []
    global connection, cursor
    cursor.execute('SELECT * FROM deliveries;')
    rows = cursor.fetchall()
    for each in rows:
        all_tracknum.append(each[0])
    connection.commit()
    return all_tracknum

def enter_date():
    while(True):
        try:
            date = input("Please enter the date like yyyy/mmmm/dddd/hhhh/mmmm/ssss")
            if date == '':
                break
            a = date.strip().split('/')
            year,month,date,hour,minute,second = a
            break
        except ValueError:
            print("Date entered is n valid please enter again")
            continue
    # if  (year == '') & (month == '') & (date== '')& (hour== '')& (minute== '')& (second== ''):
    if  date == '':
        return None
    else:
        t = (int(year),int(month),int(date),int(hour),int(minute),int(second),0,0,0)
        t = time.mktime(t)
        return(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(t)))

###########################################################################
###########################################################################
###########################################################################



def agents_set_order(orderid , pickuptime , dropofftime ):
    global connection, cursor
    if pickuptime == None:
        dropofftime = None
    flag = True
    all_tracknum = []
    trackingNo = random_with_N_digits()
    all_tracknum = get_all_track_num()
    while (flag == True):
        if trackingNo not in all_tracknum:
            flag = False
        else:
            trackingNo = random_with_N_digits()

    data = (trackingNo , orderid , pickuptime , dropofftime)
    print(data)
    cursor.execute('INSERT INTO deliveries(trackingNo,oid,pickUpTime,dropOffTime) VALUES (?,?,?,?);',data)
    connection.commit()
    return

def agents_add_stock(store_id, product_id):

    if (find_carries(store_id,product_id)):
        data = (enter_quantity(),store_id,product_id)
        cursor.execute('UPDATE carries SET qty = qty+? WHERE sid = ? AND pid = ?;',data )
        while True:
            print("\n1. Proceed\n2. Change the price")
            cust_input=input("Enter one of the above options:")
            if cust_input not in["1","2"]:
                continue
            elif cust_input=="2":
                uprice=input("Enter the new price: ")
                uprice=float(uprice)
                break
            elif cust_input=="1":
                break
        if cust_input=="2":
            data  =(uprice,store_id,product_id)
            cursor.execute('UPDATE carries SET uprice = ? WHERE sid = ? AND pid = ?;',data )
        connection.commit()
    return

def agents_update_order(trackingNo):
    while (True):
        deliveries = find_delevaries(trackingNo)
        if (len(deliveries) == 0):
            print("this deliveries do not exist")
            print("Please enter another trackingNo")
            trackingNo = int(input("Please enter tracking number again"))
        else:
            break
    for i in range(0, len(deliveries)):
        print ("The order of : tranckingNO:  {}  Ordernumber : {} ".format(deliveries[i][0],deliveries[i][1]))
        print ("is")
        deliveries_arrived(deliveries[i][3])

    choice = 0
    print ("1.update order pickup and drop off time")
    print("2.delete an order")
    choice = int(input("please make a choice"))
    if choice == 1:
        orderid = input("enter orderid:")
        data = (trackingNo,orderid,)
        # cursor.execute('SELECT * FROM deliveries WHERE trackingNo = ? AND oid = ? ;', data)

        ######################################################
        ######### can pick up time and drop time euqal to None##################
        while (True):
            print("Please enter the pickUpTime\n")
            PICK_TIME = enter_date()
            if (PICK_TIME == None):
                print("pickup time cannot be empty\n please type it again")
                continue

            print("Pleass enter the dropOffTime\n")
            DROP_TIME = enter_date()
            if (DROP_TIME == None):
                print("dropoff time cannot be empty\n please type it again")
                continue
            else:
                break
        data = (PICK_TIME,DROP_TIME,trackingNo,orderid)
        cursor.execute('UPDATE deliveries SET pickUpTime= ? , dropOffTime = ? WHERE trackingNo = ? AND oid = ?;' , data)
        connection.commit()
    if choice == 2:
        orderid = input("enter orderid:")
        remove_data(trackingNo,orderid)
    return
