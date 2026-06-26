import json
from cart import Cart
from order import place_order
from food import view_foods

cart = Cart()


def register():
    username = input("Enter Username: ")
    password = input("Enter Password: ")

    user = {
        "username": username,
        "password": password
    }

    with open("users.json", "r") as file:
        users = json.load(file)

    users.append(user)

    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)

    print("Registration Successful")


def login():
    username = input("Enter Username: ")
    password = input("Enter Password: ")

    with open("users.json", "r") as file:
        users = json.load(file)

    for user in users:
        if user["username"] == username and user["password"] == password:
            print("Login Successful")
            return username

    print("Invalid Username or Password")
    return None


def add_to_cart():
    food_id = int(input("Enter Food ID: "))

    with open("foods.json", "r") as file:
        foods = json.load(file)

    for food in foods:
        if food["food_id"] == food_id:
            cart.add_item(food)
            print("Food added to cart successfully.")
            return

    print("Food not found.")


def remove_from_cart():
    if len(cart.items) == 0:
        print("Cart is Empty!")
        return

    cart.view_cart()

    food_id = int(input("Enter Food ID to remove: "))
    cart.remove_item(food_id)


while True:

    print("\n===== FOOD APP =====")
    print("1. Register")
    print("2. Login")
    print("3. Exit")

    choice = input("Enter Choice: ")

    if choice == "1":
        register()

    elif choice == "2":

        username = login()

        if username:

            while True:

                print("\n===== USER MENU =====")
                print("1. View Foods")
                print("2. Add to Cart")
                print("3. View Cart")
                print("4. Remove from Cart")
                print("5. Place Order")
                print("6. Logout")

                option = input("Enter Choice: ")

                if option == "1":
                    view_foods()
                    
                elif option == "2":
                    add_to_cart()

                elif option == "3":
                    cart.view_cart()

                elif option == "4":
                    remove_from_cart()

                elif option == "5":
                    if len(cart.items) == 0:
                        print("Cart is Empty!")

                    else:
                        place_order(username, cart.items)
                        cart.items.clear()

                elif option == "6":
                    print("Logged Out Successfully!")
                    break

                else:
                    print("Invalid Choice")

    elif choice == "3":
        print("Thank You!")
        break

    else:
        print("Invalid Choice")