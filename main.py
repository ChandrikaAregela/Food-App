import json
from cart import Cart
from order import place_order
from food import view_foods
cart = Cart()


def register():
    username = input("Enter Username: ")
    password = input("Enter Password: ")
    
    user = { "username": username, "password": password}
    with open("users.json","r") as file:
        users = json.load(file)
    users.append(user)
    
    with open("users.json","w") as file:
        json.dump(users,file,indent=4)
    print("Registration is Successful")

def login():
    username = input("Enter Username: ")
    password = input("Enter Password: ")
    
    with open("users.json","r") as file:
        users = json.load(file)
    
    for user in users:
        if user["username"] == username and user["password"] == password:
            print("Login Successful")
            return username
    print("Invalid Username or Password") 
    return None  

def add_to_cart():
    food_id = int(input("Enter Food ID: "))
    
    with open("foods.json","r") as file:
        foods = json.load(file)
        
    for food in foods:
        if food["food_id"] == food_id:
            cart.add_item(food)
            print(" added successfully ")
            return
    print("Food not found")  





while True:
    print("--- FOOD APP ---")  
    print("1.Register")
    print("2.Login")
    print("3.Exit")
    choice = input("Enter Choice : ")
    
    if choice == "1":
        register()
    elif choice == "2":
       username = login()
       if username:
           while True:
               print("\n ====USER MENU===")
               print("1. View Foods")
               print("2. Add to Cart")
               print("3. View cart")
               print("4. Place Order")
               print("5. Logout")
               option = input("Enter Choice: ")
               if option == "1":
                   view_foods()
               elif option =="2":
                   add_to_cart()
               elif option == "3":
                   cart.view_cart()
               elif option == "4":
                    place_order(username, cart.items)
                    cart.items.clear()

               elif option == "5":
                    break

    elif choice == "3":
        print("Thank You")
        break
                
    