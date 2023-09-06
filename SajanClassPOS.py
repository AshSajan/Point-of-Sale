from datetime import date
UIPassDict = {}  # password Dictionary
SaleDict = {}  # Sale dictionary to store receipt number and value will be the sale object


def verifyUIAndPW(userid, password):
    passReturned = UIPassDict.get(userid)
    if passReturned == password:
        return True
    else:
        print("Invalid User or Password. Please double-check your input")


def getAllUIAndPasswordData():
    try:
        with open("UserIDPassword.txt", "r") as passwordFile:
            for aLine in passwordFile:
                data = aLine.split()
                if len(data) == 2:
                    userid = data[0]
                    password = data[1]
                    UIPassDict[userid] = password
                else:
                    print("getAllUI Invalid file format. Please check the file contents.")
    except FileNotFoundError:
        print("getAllUI File not found. Please make sure the file exists.")
    except:
        print("Catch All error om getALLUI method")



class Sale:
    # This dictionary will store UPC as the key & Item object as value
    ItemDictionary = {}

    def __init__(self):
        self.receiptNumber = 0
        self.totalAmount = 0
        self.totalTax = 0
        self.ItemDictionary = {}
        self.date = date.today() # to record today's sales

    def createReceipt(self, inventory):
        self.receiptNumber = hash(self)  # memory # for receipt
        self.totalAmount = 0
        self.totalTax = 0
        while True:
            UPC = input("Please enter the UPC of the item: ")
            if UPC not in inventory.AllItemsDict:
                print("Invalid UPC. Please double check your input.")
                continue
            item = inventory.AllItemsDict[UPC]
            print("You entered: ", item.Description)
            while True:  # Loop to ask for quantity until a valid quantity is provided
                quantity = int(input("How many would you like? "))
                if quantity > float(item.Item_on_hand):
                    print("We don't have that many in stock. Please select a lower number.")
                    continue
                else:
                    break
            item_price = float(item.Unit_price)
            item_total = round(item_price * quantity, 2)
            print("Price of", quantity, item.Description, "is", item_total)
            item.UpdateUnitOnHand(quantity)
            self.ItemDictionary[item.UPC] = quantity
            self.calculateTotal(inventory)
            choice = input("1 = Sell another item, 2 = Return Item/s,  9 = Complete Sale: ")
            if choice == "1":
                continue
            elif choice == "2":
                print("2 = Return Item/s")
                self.returnItem(inventory)
            elif choice == "9":
                print("9 = Complete Sale")
                self.calculateTotal(inventory)
                self.printReceiptNumber()
                break
            else:
                print("Invalid choice. Returning to the main menu.")
                break

    def printReceiptNumber(self):
        print("Receipt Number:", self.receiptNumber)


    def cancelSale(self):
        pass

    def returnItem(self, inventory):
        receipt_number = int(input("Please enter the receipt number: "))
        if receipt_number not in SaleDict:
            print("Invalid receipt number.")
            return

        sale = SaleDict[receipt_number]

        return_choice = input("1 = Return Single Item, 2 = Return All Items ")
        if return_choice == "1":
            sale.returnSingleItem(inventory)
        elif return_choice == "2":
            print("2 = Return All Items")
            sale.returnAllItem(inventory)
        else:
            print("Invalid choice.")

    def returnSingleItem(self, inventory):
        # Ask for the UPC of the item to return
        UPC = input("Please enter the UPC of the item you want to return: ")

        # Check if the item was sold in this sale
        if UPC not in self.ItemDictionary:
            print("The item with the provided UPC was not sold in this sale.")
            return

        # Check if all items with this UPC have been returned already
        if self.ItemDictionary[UPC] <= 0:
            print("All items with the provided UPC have been returned already.")
            return

        item = inventory.AllItemsDict[UPC]
        quantity = 1  # hard coding so this will always return 1 item

        return_amount = float(item.Unit_price) * quantity
        self.ItemDictionary[UPC] -= quantity

        print("Return amount for one " + item.Description, "is", return_amount)

        while True:
            choice = input("1 = Sell another item, 2 = Return Item/s,  9 = Complete Sale: ")
            if choice == "1":
                break
            elif choice == "2":
                print("2 = Return Item/s")
                return_choice = input("1 = Return Single Item, 2 = Return All Items")
                if return_choice == "1":
                    self.returnSingleItem(inventory)
                elif return_choice == "2":
                    self.returnAllItem(inventory)
                else:
                    print("Invalid choice.")
            elif choice == "9":
                print("9 = Complete Sale")
                self.calculateTotal(inventory)
                self.printReceiptNumber()
                break
            else:
                print("Invalid choice.")

    def returnAllItem(self, inventory):
        # Code for returning all items
        returnCheck = input("Are you sure you want to return all items? (y/n) ")
        if returnCheck.lower() not in ["y", "yes"]:
            print("We canceled the return as requested")
            return
        return_amount = 0
        for UPC, quantity in self.ItemDictionary.items():
            item = inventory.AllItemsDict[UPC]
            return_amount += float(item.Unit_price) * quantity
            self.ItemDictionary[UPC] = 0

        print("Return amount for all items is", round(return_amount,2))
        while True:
            choice = input("1 = Sell another item, 2 = Return Item/s,  9 = Complete Sale: ")
            if choice == "1":
                break
            elif choice == "2":
                print("2 = Return Item/s")
                return_choice = input("1 = Return Single Item, 2 = Return All Items")
                if return_choice == "1":
                    self.returnSingleItem(inventory)
                elif return_choice == "2":
                    self.returnAllItem(inventory)
                else:
                    print("Invalid choice.")
            elif choice == "9":
                print("9 = Complete Sale")
                self.calculateTotal(inventory)
                break
            else:
                print("Invalid choice. Please select a valid option.")

    def calculateTotal(self, inventory):
        self.totalAmount = 0
        self.totalTax = 0
        for item_upc, quantity in self.ItemDictionary.items():
            item = inventory.AllItemsDict[item_upc]
            item_total = float(item.Unit_price) * quantity
            self.totalAmount += item_total
            self.totalTax += item_total * 0.07
            self.totalAmount = round(self.totalAmount, 2) #round both to 2 decimal places
            self.totalTax = round(self.totalTax, 2)

    def viewCart(self):
        pass

def reportTotalSalesToday():
    today = date.today()
    total_sales = 0
    for sale in SaleDict.values():
        if sale.date == today:
            total_sales += sale.totalAmount
    print("Total Sales for Today Is: ", total_sales)

def reportTotalSalesThisMonth():
    today = date.today()
    total_sales = 0
    for sale in SaleDict.values():
        if sale.date.month == today.month and sale.date.year == today.year:
            total_sales += sale.totalAmount
    print("Total Sales for this Month is: ", total_sales)

class Item:
    def __init__(self, UPC, Description, Item_Max_Qty, Order_Threshold, replenishment_order_qty, Item_on_hand,
                 Unit_price):
        self.UPC = UPC  # this should be private. Use set and get
        self.Description = Description
        self.Item_Max_Qty = Item_Max_Qty
        self.Order_Threshold = Order_Threshold
        self.replenishment_order_qty = replenishment_order_qty
        self.Item_on_hand = float(Item_on_hand)
        self.Unit_price = Unit_price

    @property
    def UPC(self):
        return self._UPC

    @UPC.setter
    def UPC(self, UPC):
        if isinstance(UPC, str):
            self._UPC = UPC
        else:
            raise ValueError('UPC must be a string')

    @property
    def Item_on_hand(self):
        return self._Item_on_hand

    @Item_on_hand.setter
    def Item_on_hand(self, quantity):
        if quantity >= 0:
            self._Item_on_hand = quantity
        else:
            raise ValueError("Item_on_hand must be greater than or equal to zero")

    def UpdateUnitOnHand(self, quantity):
        if self._Item_on_hand - quantity < 0:
            raise ValueError("Item_on_hand cannot go below zero")
        self._Item_on_hand -= quantity
class Inventory:
    # will have collection of all items
    AllItemsDict = {}

    def __init__(self):
        self.AllItemsDict = {}
        try:
            with open(r"C:\Users\evils\OneDrive\Desktop\MS DS\603\FinalProject\RetailStoreItemData-1.txt", "r+") as f:
                lines = f.readlines()

                for j in lines:
                    i = j.split(",")
                    i = [elem.strip() for elem in i]
                    try:
                        UPC = (i[0])
                        Description = i[1]
                        Item_Max_Qty = (i[2])
                        Order_Threshold = (i[3])
                        replenishment_order_qty = (i[4])
                        Item_on_hand = (i[5])
                        Unit_price = (i[6])
                        itemObj = Item(UPC, Description, Item_Max_Qty, Order_Threshold, replenishment_order_qty,Item_on_hand,Unit_price)
                        self.AllItemsDict[UPC] = itemObj
                        # print(itemObj)
                    except (ValueError, IndexError):
                        print("Error reading file or invalid file format")
        except FileNotFoundError:
            print("File not found. Please make sure the file exists.")
        except:
            print("Catch All error in inventory class")
    def generateInventoryReport(self):
        print("\n--- Inventory Report ---")
        for item in self.AllItemsDict.values():
            print("Item Name: ", item.Description)
            print("Quantity: ", item.Item_on_hand)
            print("Threshold: ", item.Order_Threshold)
            availableAmount = "Yes" if item.Item_on_hand > 0 else "No"
            print("Available in Store Today: ", availableAmount)
            print("-------------------------")

inventoryObject = Inventory()


print("Welcome to the POS System")

counter = 0
locked_out = False
currentSale = None

while counter < 3:
    userid = input("Please enter userid: ")
    password = input("Please enter password: ")

    getAllUIAndPasswordData()

    if verifyUIAndPW(userid, password):

        print("Welcome", userid)

        while True:
            choice = int(input("1 = New Sale, 2 = Return Item/s, 3 = Backroom Operations, 9 = Exit Application: "))
            if choice == 1:
                print("1 = New Sale")
                currentSale = Sale()
                currentSale.createReceipt(inventoryObject)
                SaleDict[currentSale.receiptNumber] = currentSale
                #currentSale.printReceiptNumber()
            elif choice == 2:
                print("2 = Return Item/s")
                if currentSale is None:
                    print("No sale has been created. Please create a new sale first.")
                else:
                    currentSale.returnItem(inventoryObject)
            elif choice == 3:
                print("3 = Backroom Operations")
                operation_choice = int(input("1 = Generate Inventory Report, 2= Total Sales for Today, 3, Total Sales for the Month, 9 = Go back: "))
                if operation_choice == 1:
                    inventoryObject.generateInventoryReport()
                elif operation_choice == 2:
                    reportTotalSalesToday()
                elif operation_choice == 3:
                    reportTotalSalesThisMonth()
                elif operation_choice == 9:
                    continue
            elif choice == 9:
                print("9 = Exit Application")
                break
            else:
                print("Invalid choice")

        break

    counter += 1
    if counter == 3:
        print("You have been locked out. Please contact the administrator.")
    else:
        print("This is now attempt", counter+1, "of 3.")

