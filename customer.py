import sqlite3
import time
import operator
import os
import sys

connection = None
cursor = None

def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA forteign_keys=ON; ')
    connection.commit()
    return

"""
Define all the tables and data into the database
"""
def define_tables_values():
    global connection, cursor

    with open('prj-tables.sql') as tables:
        cursor.executescript(tables.read())
    with open('prj-data.sql') as values:
        cursor.executescript(values.read())
    connection.commit()
    return

"""
Gives the options to select the page number
Returns: user input()
"""
def customer_main(page):
    print("\nCustomer Main Page\n")
    display="1. Search for Products\n2. Place an order\n3. List orders\n4. Log out\n\nSelect one of the above: "
    inp=("1","2","3","4")
    while True:
        cust_input=input(display)
        if cust_input in inp: return int(cust_input)
        else: print("\nWRONG INPUT PLEASE SELECT FROM THE GIVEN OPTIONS\n")

"""
Argument: cid (customer id), path of database
Main function of Customer to manage all different pages
"""
def Customer(cid,path=""):
    global connection, cursor
    connect(path)
    page=0
    basket=[]
    while True:
        if page==0:
            page=customer_main(page)
        elif page==1:
            basket=search_products()
            page=0
        elif page==2:
            place_order(cid,basket)
            page=0
        elif page==3:
            list_orders(cid)
            page=0
        elif page==4: break

    connection.commit()
    connection.close()

    # os.system('cls' if os.name=='nt' else 'clear')
    return

"""
Gives the options to enter multiple keywords
Returns: matched products
"""
def enter_keyword():
        match=dict()
        keywords=input("\nEnter one or more keyword with a space: ").split(' ')
        for each in keywords:
            key='%'+each+'%'
            rows=cursor.execute("select distinct name from products where name like ?;",(key,) )
            for e_product in rows:
                if e_product[0] in match: match[e_product[0]]=match[e_product[0]]+1
                else: match[e_product[0]]=1
        if len(match)==0:
            print("\nNothing Matched Please Try Again" )
            return enter_keyword()
        sorted_match=sorted(match.items(), key=operator.itemgetter(1), reverse=True)
        return sorted_match

"""
Collects all the information of the matched products
Returns: details as dict() of the products
"""
def match_details(match):
    details=dict()
    counter=1
    for each in match:
        pid_name_unit=cursor.execute("select pid,name,unit from products where name=?;",(each[0],))
        pid,name,unit=pid_name_unit.fetchone()

        store_carry=cursor.execute("select count(distinct sid),min(uprice) from carries where pid=?",(pid,))
        no_store_carry,carry_min_price=store_carry.fetchone()

        store_instock=cursor.execute("select count(distinct sid),min(uprice) from carries where pid=? and qty>0;",(pid,))
        no_store_instock,instock_min_price=store_instock.fetchone()

        no_of_orders=cursor.execute('''
                                select sum(qty) from olines ol,orders od
                                where pid=? and ol.oid=od.oid and
                                date(od.odate, '+7 day') >= date('now');''',(pid,))
        no_of_orders=no_of_orders.fetchone()[0]

        details[counter]=[ \
        ["product id:",pid],["name:",name],["unit:",unit],\
        ["number of stores that carry:",no_store_carry],\
        ["number of stores that have it in stock:",no_store_instock],\
        ["minimum price among the stores that carry:",carry_min_price],\
        ["minimum price among the stores that have the product in stock:",instock_min_price],\
        ["number of orders within the past 7 days:",no_of_orders] ]

        counter+=1

    return details

"""
Gives options to select product or go back to search again
Returns: customer input
"""
def decide_product(details,order=0):
        if len(details)<=5:
            if order==0:
                display="1. Selct a product \n2. Go back to Search product\n\nSelect one of the above: "
            elif order==1:
                display="1. Selct an order \n2. Go back to Customer Main Page\n\nSelect one of the above: "
            counter=0
        elif len(details)>5:
            if order==0:
                display="1. Selct a product\n2. See more products \n3. Go back to Search product\n\nSelect one of the above: "
            elif order==1:
                display="1. Selct an order\n2. See more orders \n3. Go back to Customer Main Page\n\nSelect one of the above: "
            counter=1
        else: return 0,0
        cust_input=input(display)
        if counter==0 and (cust_input in ["1","2"] ):
            return int(cust_input),counter
        elif counter==1 and (cust_input in ["1","2","3"] ):
            return int(cust_input),counter
        else:
            print("\nWrong Input Please Select from the above options\n")
            return decide_product(details,order)

"""
Arguments: details,order,index
details - is the dict() containing the information of the products/orders
order - checks if the orders or products needs to be displayed
index - To track the the items to display

Function displays the products/orders 5 at a time

"""
def show_products(details,index,order=0):
    counter=0
    for each in range(index,len(details)):
        if order==0: print("Product Number",each+1)
        elif order==1: print("Order",each+1)
        for each_detail in details[each+1]:
            print(each_detail[0],each_detail[1])
        counter+=1
        print()
        if counter==5: return
    return


def Matched_Products(details,order=0):
    index=0
    while True:
        if order==0: print("\nMatched Products\n")
        elif order==1: print("\nMatched Orders\n")
        show_products(details,index,order)
        cust_input,counter=decide_product(details,order)
        
        if cust_input==2 and counter==0:
            search=True
            break
        elif cust_input==3 and counter==1:
            search=True
            break
        elif cust_input==1:
            search=False
            break
        elif cust_input==2 and counter==1:
            index+=5
            if index>=len(details):
                index-=5
                if order==0: print("\nSorry No More Products\n")
                elif order==1: print("\nSorry No More Orders\n")
            continue
    return search

"""
Arguments: details
details - is the dict() containing the information of the products

Function collects the necessary information of the products and store it
in product_details

Returns: product details,info
"""
def Product_Selected(details):
    product_details=dict()
    while True:
        print("\nIn Product Selected\n")
        display="Please Enter a product number between 1 to " +str(len(details))+": "
        product_selected=input(display)
        if product_selected not in [str(each) for each in range(1,len(details)+1)]:
            print("\nWrong Input Please Try again")
            continue

        cat=cursor.execute("select cat from products where pid=?;",\
                            (details[int(product_selected)][0][1],))
        cat=cat.fetchone()[0]

        info=[ \
        ["pid:",details[int(product_selected)][0][1]],\
        ["product name:",details[int(product_selected)][1][1]],\
        ["unit:",details[int(product_selected)][2][1]],\
        ["category:",cat] ]

        store_info_InStock=cursor.execute("select c.sid,name,c.qty,c.uprice \
                                        from stores,carries c \
                                        where c.pid=? and c.qty>0 and c.sid=stores.sid \
                                        order by uprice;", \
                                        (info[0][1],))
        store_info_InStock=store_info_InStock.fetchall()
        store_info_NotInStock=cursor.execute("select c.sid,name,c.qty,c.uprice \
                                        from stores,carries c \
                                        where c.pid=? and c.sid=stores.sid and c.qty=0 \
                                        order by uprice;", \
                                        (info[0][1],))
        store_info_NotInStock=store_info_NotInStock.fetchall()

        counter=1
        for each in range(0,len(store_info_InStock)):
            order=cursor.execute('''
                                select sum(qty) from olines ol,orders od
                                where pid=? and sid=? and ol.oid=od.oid and
                                date(od.odate, '+7 day') >= date('now');''',\
                                (info[0][1],store_info_InStock[each][0],))
            store_info_InStock[each]=store_info_InStock[each] + order.fetchone()

            product_details[counter]=[ \
            ["store id:",store_info_InStock[each][0]],["store name:",store_info_InStock[each][1]],\
            ["quantity:",store_info_InStock[each][2]],["price:",store_info_InStock[each][3]],\
            ["no_of_order past 7 days:",store_info_InStock[each][4]] ]

            counter+=1
        for each in range(0,len(store_info_NotInStock)):
            order=cursor.execute('''
                                select sum(qty) from olines ol,orders od
                                where pid=? and sid=? and ol.oid=od.oid and
                                date(od.odate, '+7 day') >= date('now');''',\
                                (info[0][1],store_info_NotInStock[each][0],))
            store_info_NotInStock[each]=store_info_NotInStock[each] + order.fetchone()

            product_details[counter]=[ \
            ["store id:",store_info_NotInStock[each][0]],["store name:",store_info_NotInStock[each][1]],\
            ["quantity:",store_info_NotInStock[each][2]],["price:",store_info_NotInStock[each][3]],\
            ["no_of_order past 7 days:",store_info_NotInStock[each][4]] ]

            counter+=1
        return product_details,info

"""
Arguments: details,info
details - is the dict() containing the information of the products
info - has pid,name,cat,unit of product

Function : displays the stores which match the selected product
"""
def match_specific_product(details,info):
    for each in info:
        print(each[0],each[1])
    print()
    for each in range(1,len(details)+1):
        print("Store Number",each)
        for each_detail in details[each]:
            print(each_detail[0],each_detail[1])
        print()
    search=[False,0]
    while True:
        display='1. Select the store to add the products to basket\n2. Enter "y" or "Y" to Go back to Search\n'
        print(display)
        store_selected=input("Select one of the above options: ")
        if store_selected=="y" or store_selected=="Y": search=[True,0]; return search
        if store_selected not in [str(each) for each in range(1,len(details)+1)]:
            print("\nWrong Input Please Try again\n")
            continue
        search=[False,store_selected]
        return search

"""
Arguments: basket,index
basket - contains the customers orders
index - To check if the item needs to be deleted or just changed
will have the option to delete in case the user quantity exceeds the store limit

Function changes the quantity of the basket or deleted the products from the basket
based on the input

Returns: basket
"""
def change_quantitiy(basket,index=0):
    while True:
        if len(basket)==0:
            print("Sorry your Basket is Empty")
            return basket
        if index==1: display='\n1. Enter the Item number to change to change the quantity\n2. Enter "D" or "d" to delete the item \n3. Enter "y" or "Y" to Go back to Place Order\n'
        elif index==0: display='\n1. Enter the Item number to change the quantity\n2. Enter "y" or "Y" to Go back to Search\n'
        print(display)
        cust_input=input("Select one of the above options: ")
        if cust_input=="y" or cust_input=="Y": return basket
        elif index==1 and (cust_input=="d" or cust_input=="D"):
            while True:
                delete_item=input("Enter the item no to delete: ")
                if delete_item not in [str(each) for each in range(1,len(basket)+1)]:
                    print("\nWrong Input Please Try again\n")
                    continue
                basket.remove(basket[int(delete_item)-1])
                print("Item",int(delete_item),"deleted")
                print("\nBASKET\n")
                counter=1
                for each in basket:
                    print("Item:",counter)
                    counter+=1
                    for each_detail in each:
                        print(*each_detail)
                    print()
                break
            continue
        if cust_input not in [str(each) for each in range(1,len(basket)+1)]:
            print("\nWrong Input Please Try again\n")
            continue
        while True:
            cus_input=input("\nEnter the new quantity: ")
            if cus_input.isnumeric() is False:
                print("\nWrong Input Please Try again\n")
                continue
            else: break
        print("Quantity changed for product",basket[int(cust_input)-1][5][1],"to",cus_input)
        basket[int(cust_input)-1][3][1]=int(cus_input)


"""
Arguments: details,info,basket
details - is the dict() containing the information of the products/orders
basket - contains the customers orders
info - has pid,name,cat,unit of product

Function :
1) displays the products in the basket
2) gives the options to users to either change the quantity or go back to search
3) if required calls the change_quantity()

Returns: basket
"""
def Basket(details,info,basket):
    quantity=1
    details.append( ["user quantity",quantity] )
    for each in info: details.append(each)
    basket.append(details)
    print()
    print("\nBASKET\n")
    counter=1
    for each in basket:
        print("Item:",counter)
        counter+=1
        for each_detail in each:
            print(*each_detail)
        print()
    while True:
        display="\n1. Change the quantity\n2. Go back to Search"
        print(display)
        cust_input=input("Select one of the above options: ")
        if cust_input not in ["1","2"]:
            print("\nWrong Input Please Try again\n")
            continue
        elif cust_input=="2": return basket
        elif cust_input=="1":
            basket=change_quantitiy(basket)
            return basket

"""
Function :
Main function of search which manages all function calls to provide the
required functionality of searching products

Returns: basket
"""
def search_products():
    basket=[]
    while True:
        print("\nIn search products")
        display="\n1. Search a product\n2. Go back to Customer main page\n"
        print(display)
        cus_input=input("Select one of the above: ")
        if cus_input not in ["1","2"]:
            print("\nWrong Input Please Try again")
            continue
        if cus_input=="2": page=0; return basket
        details=match_details(enter_keyword())
        # for each in details: print(each,details[each])

        search=Matched_Products(details)
        if search is True: continue

        specific_product_details,info=Product_Selected(details)

        search = match_specific_product(specific_product_details,info)
        if search[0] is True: continue

        Product_for_basket=[\
        specific_product_details[int(search[1])][0],\
        specific_product_details[int(search[1])][1],\
        specific_product_details[int(search[1])][3] ]

        basket=Basket(Product_for_basket,info,basket)
        # print(basket)

    return basket

"""
Arguments: basket

Function : Checks the user quantity with the store quantity

Returns: item_no as list containing all the user items that excedded
         the store quantity
"""
def check_quantity(basket):
    item_no=[] # stores []s where [item no, store quantity]
    counter=1
    for each in basket:
        # print(each[3])
        rows=cursor.execute("select qty from carries where pid=? and sid=?;",\
                            (each[4][1],each[0][1],) )
        store_quantity=rows.fetchone()[0]
        if store_quantity<each[3][1]: item_no.append([counter,store_quantity])
        # print("store_quantity for item",counter,"--",store_quantity)

        counter+=1
    # print("item_no:",item_no)
    return item_no

"""
Arguments : item_no, basket

Function :
1) Alerts the user if the store quantity < user quantity
2) call the change_quantitiy() to give an option to user to change/delete the quantity

Returns: basket
"""
def update_quantity(item_no,basket):
    print("\nBASKET\n")
    counter=1
    for each in basket:
        print("Item:",counter)
        counter+=1
        for each_detail in each:
            print(*each_detail)
        print()

    for each in item_no:
        print("Item no:",each[0],"exceeds quantity in the store\nChange the quantity to place the order")
    change_quantitiy(basket,1)

    # print("back after change, new basket: ",basket)
    return basket

"""
Arguments : basket

Function : updates the store quantity according to user quantity
"""
def update_store_quantity(basket):
    global connection, cursor

    print("WIll update the store quantity now")
    for each in basket:
        sid=each[0][1]
        pid=each[4][1]
        user_quantity=each[3][1]
        # print(sid,pid,user_quantity)

        cursor.execute("update carries set qty=qty-? where pid=? and sid=?;",\
        (user_quantity,pid,sid,))

    connection.commit()
    return

def get_unique_orderid():
    import random
    return random.randint(1,99999)

"""
Arguments : cid,basket

Function : places the order for all products in the basket
"""
def PlaceOrder(cid,basket):
    global connection, cursor

    odate=time.strftime("%Y-%m-%d %H:%M:%S")

    rows=cursor.execute("select address from customers where cid=?;",(cid,))
    address=rows.fetchone()[0]

    for each in basket:
        sid=each[0][1]
        pid=each[4][1]
        qty=each[3][1]
        uprice=each[2][1]

        while True:
            oid=get_unique_orderid()
            rows=cursor.execute('select * from orders where oid=?',(oid,))
            row=rows.fetchall()

            if len(row)>0:
                continue
            else: break

        cursor.execute("INSERT INTO orders(oid,cid,odate,address) VALUES \
        (?,?,?,?)",(oid,cid,odate,address,))

        cursor.execute("INSERT INTO olines(oid,sid,pid,qty,uprice) VALUES \
        (?,?,?,?,?)",(oid,sid,pid,qty,uprice,))

    print("Order Placed")
    connection.commit()
    return

"""
Function :
Main function of place order which manages all function calls to provide the
required functionality of place an order
"""
def place_order(cid,basket):
    if len(basket)==0:
        print("Sorry your basket is empty")
        return

    while True:
        item_no=check_quantity(basket) # check if the quantity is greater then store quantity
        if len(item_no)==0: break
        basket=update_quantity(item_no,basket) # if quantity is too high, change or delete
        if len(basket)==0: return

    update_store_quantity(basket)

    print("Will place the order now")
    PlaceOrder(cid,basket) # ask details and update the order and olines tables
    return

"""
Function :
1) Collects the information of all orders of the given cutomer id
2) calls the Matched_Products() to display the orders 5 at a time
"""
def matched_orders(cid):
    details=dict()
    rows=cursor.execute('''select o.oid,o.odate,count(distinct pid),sum(uprice)
                        from orders o, olines
                        where cid=? and o.oid=olines.oid
                        group by o.oid,o.odate
                        order by o.odate;''',(cid,))
    orders=rows.fetchall()

    counter=1
    for each in orders:
        details[counter]=[\
        ["order id:",each[0]],["order date",each[1]],\
        ["number of products ordered",each[2]],["total price",each[3]] ]
        counter+=1

    MainPage=Matched_Products(details,1)

    return MainPage,details

"""
Arguments: cid, details (details of all orders)

Function : prints the information of all products in the order
"""
def selected_order(cid,details):
    while True:
        print("\nIn Order Selected\n")
        display="Please Enter a order number between 1 to " +str(len(details))+": "
        order_selected=input(display)
        if order_selected not in [str(each) for each in range(1,len(details)+1)]:
            print("\nWrong Input Please Try again")
            continue

        oid=details[int(order_selected)][0][1]
        rows=cursor.execute('''select trackingNo, pickUpTime, dropOffTime, address
                            from orders o, deliveries d
                            where o.oid=? and o.oid=d.oid;''',(oid,))
        row=rows.fetchone()
        try:
            print("Tracking No:",row[0])
            print("Pick Up Time:",row[1])
            print("Drop Off Time:",row[2])
            print("Address To be delivered:",row[3])
        except:
            print("Tracking No:",None)
            print("Pick Up Time:",None)
            print("Drop Off Time:",None)
            print("Address To be delivered:",None)

        rows=cursor.execute('''select ol.sid, s.name, ol.pid, p.name, ol.qty, p.unit, ol.uprice
                            from olines ol, stores s, products p
                            where ol.oid=? and ol.pid=p.pid and ol.sid=s.sid;''',(oid,))
        row=rows.fetchone()
        print("store id:",row[0])
        print("store name:",row[1])
        print("product id:",row[2])
        print("product name:",row[3])
        print("quantitity:",row[4])
        print("unit:",row[5])
        print("uprice:",row[6])
        return

"""
Function :
Main function of list orders which manages all function calls to provide the
required functionality of list orders
"""
def list_orders(cid):
    while True:
        MainPage,details=matched_orders(cid)
        if MainPage==True: break
        print("Will select the order now")
        selected_order(cid,details)
    return


def main():
    global connection, cursor
    path="./project_1.db"
    connect(path)
    define_tables_values()
    cid=1
    Customer(cid)
    connection.commit()
    connection.close()
    return

if __name__ == "__main__":
	main()
