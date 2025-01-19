import os
from pathlib import Path
import json

ABORT = "abort"
GROCERY_ITEMS_FILE = Path("groceryItems.json").read_text()
JSON_GROCERY = json.loads(GROCERY_ITEMS_FILE)
GROCERY_ITEMS = JSON_GROCERY["groceryList"]

class Responses:
    def invalid_option(self):
        print("Invalid Option, please try again.")

Response = Responses()

class MenuText:
    def main_menu_text(self):
        clear()
        print()
        print("\033[1mWelcome to our shop!\033[0m" )
        print()
        print("Please select an option below.\n")
        print("(1) Buy items.")
        print("(2) Exit")

    def exit(self):
        clear()
        print("\nThank you for visiting our store!")
        print("We hope to see you again!\n")


def clear():
    os.system("cls") #Clears the screen in Windows on Terminal


class Menus:
    def __init__(self, Menu_text):
        self.grocery_items = GROCERY_ITEMS
        self.MenuText = Menu_text

    def cart(self, content, total):
        print("\n\t\tCart\n")
        for item in content:
            summed = int(item["unitPrice"]) * int(item["qty"])
            print(f"{item["qty"]}\t {item["name"]}\t\t R{summed}")
            total += int(item["unitPrice"])*int(item["qty"])
        print(f"\n\t Subtotal:\t R{total}")

    def tax_invoice_printout(self, content, total):     # Display your invoice on the screen
        clear()
        print("\t\033[1mTax invoice\033[0m")
        print("\nQty \tItem\t\tAmount\n")
        for item in content:
            summed = int(item["unitPrice"]) * int(item["qty"])
            print(f"{item["qty"]}\t {item["name"]}\t\t R{summed:.2f}")
            total += int(item["unitPrice"])*int(item["qty"])
        print("\t\t================")
        print(f"\n\t Subtotal:\t R{round((total*0.85), 2):.2f}")
        print(f"\t VAT(15%):\t R{round((total*0.15), 2):.2f}")
        print("\t\t================")
        print(f"\n\tTotal:\t\t R{total:.2f}")
        print("\n\n")
        
    def tax_invoice_save_copy(self, content, total):    # Save a text file of your invoice
        data = ""
        filename = input("Save invoice as?: ")
        filename = f"{filename}.txt"
        data += "\tTax invoice"
        data += "\nQty\tItem\t\tAmount\n"
        for item in content:
            summed = int(item["unitPrice"]) * int(item["qty"])
            data += f"{item["qty"]}\t{item["name"]}\t\tR{summed:.2f}"
            data += '\n'
            total += int(item["unitPrice"])*int(item["qty"])
        data += "\t===================="            
        data += f"\n\tSubtotal:\tR{round((total*0.85), 2):.2f}"
        data += f"\n\tVAT(15%):\tR{round((total*0.15), 2):.2f}"
        data += "\n\t===================="
        data += f"\n\tTotal:\t\tR{total:.2f}"
        with open(f"invoices\{filename}", "w") as file:
            file.write(data)

        print(f"\nYour invoice has been saved as {filename}.")
        print("Please press 'ENTER' to continue...")
        input()
        clear()
        return ABORT


    def check_out(self,cart, total):
        while True:
            print("There is items in your cart.")
            self.cart(cart, total)
            print("Choose an option: \n(c)Check out.\n(e)Edit Cart. \n(a)Abort Cart.")
            option = input("Input: ").lower()
            print(f"value={option}")
            
            if option == "e":
                self.edit_cart(cart, total)
                continue
            if option == "a":
                print("Are you sure you want to abort your sale?")
                abort = input("(y/n)").lower() 
                if abort not in ("y","n"):
                    Response.invalid_option()
                elif abort == "y":
                    return ABORT
            if option == 'c':
                self.tax_invoice_printout(cart, total)
                return self.tax_invoice_save_copy(cart, total)
                
            else:
                Response.invalid_option()

    def check_if_item_in_cart(self, cart, option, items):
        item_found = False
        for cartitem in cart:
            if cartitem['name'] == items[option]["name"]:
                item_found = True
        return (item_found)
            
    def cart_add(self,cart, items, total, options):        
        while True:  
            option = input(f"Option(0-{len(items)-1}): ")   #Check file and Display ITEMS available to add to cart
            try:
                if option.lower() == 'n':   # If choosing 'n' while cart is empty, ABORTING shop option, RETURING to Main menu
                    if cart == []:
                        return
                    else:
                        if self.check_out(cart, total) == ABORT:
                            return ABORT
                option = int(option)
                if option in options:
                    while True:
                        try:
                            qty = int(input(f"How many of item {items[option]["name"]} would you like to add?: "))
                            break
                        except ValueError:
                            Response.invalid_option()
                    if self.check_if_item_in_cart(cart, option, items):
                        for index, cartitem in enumerate(cart):
                            if cartitem['name'] == items[option]["name"]:
                                cart[index]["qty"] += int(qty)
                    else:
                        cart.append(items[option])
                        cart[-1]['qty'] = int(qty)
                    break    

                else:
                    Response.invalid_option()
                    continue
            except ValueError:
                Response.invalid_option()
                continue


    def edit_cart_edit_item(self, cart, item, index):
        print("Change the qty to? \n(c) to cancel.")
        value = input("Choice: ")
        try:
            if value.lower() == "c":
                return False
            elif int(value) > 0:
                item["qty"] = value
            elif int(value) == 0:
                del cart[index]
            elif int(value) < 0:
                Response.invalid_option()
        except ValueError:
            Response.invalid_option()


    def edit_cart(self, cart, total):
        self.cart(cart, total)
        print("\n\nDo you want to change or remove items?")
        option = input("\n(0) Change Item Qty. \n(1) Remove item.\n(2) Return to cart. \nChoose option: ")
        print()
        if option == "0":
            print("Choose item to edit")
            for index, item in enumerate(cart):
                print(f"({index})\t{item["qty"]}\t{item["name"]}")
            print("(c) to cancel.")
            choice = input("Choice: ")
            for index, item in enumerate(cart):
                if choice == str(index):
                   cancel = self.edit_cart_edit_item(cart, item, index)
                   if cancel == False:
                    return
                elif choice.lower() == "c":
                    break
                else:
                    Response.invalid_option()
            return
        elif option == "1":
            print("Choose item to delete")
            for index, item in enumerate(cart):
                print(f"({index})\t{item["qty"]}\t{item["name"]}")
            print("(c) to cancel.")
            choice = input("Choice: ")
            for index, item in enumerate(cart):
                if choice == str(index):
                    del cart[index]
                elif choice.lower() == 'c':
                    return
                else:
                    Response.invalid_option()
        elif option == "2":
            return
        else:
            Response.invalid_option()

    def buy(self): #Displays cart(if any items in) and add items requested
        cart = []
        options = []
        items = self.grocery_items
        while True:
            total = 0
            clear()
            print("\n\033[1m--Point Of Sales--\033[0m")
            print()

            if cart == []:
                print("\nCart is empty...\n")
            else:
                self.cart(cart, total)
            print("\nPlease see our selection below:\n")
            for index, item in enumerate(items):
                print(f"({index}) {item["name"]} : {item["unitPrice"]}")
                options.append(index)
            print("Select an option which you add to your cart: ('n' to cancel or checkout cart)")
            if self.cart_add(cart, items, total, options):
                return ABORT

    def main_menu(self):
        self.MenuText.main_menu_text()
        option = input("Option: ")
        return option            

class PosSystem:
    def __init__(self, grocery_items):
        self.grocery_items = grocery_items

    def main_menu(self):
        MenuTextt = MenuText()    
        while True:
            Main = Menus(MenuTextt)
            option = str(Main.main_menu())
            if option == "2":
                MenuTextt.exit()
                break
            elif option == "1":
                self.buy(Main)
            else:
                Response.invalid_option()
    
    def buy(self, Main):
        Main.buy()


def main():
    Pos = PosSystem(GROCERY_ITEMS)
    Pos.main_menu()

if __name__ == "__main__":
    main()