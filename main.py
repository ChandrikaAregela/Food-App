"""Console entry point for the food ordering app."""

from admin import admin_menu
from cart import Cart
from food import load_foods, search_foods, view_foods
from order import (cancel_order, leave_review, place_order, show_order_history,
                   track_order)
from user import (admin_credentials_valid, authenticate, get_profile, register,
                  update_profile)


def ask_int(prompt, minimum=None, maximum=None):
    try:
        value = int(input(prompt))
        if minimum is not None and value < minimum:
            raise ValueError
        if maximum is not None and value > maximum:
            raise ValueError
        return value
    except ValueError:
        print("Please enter a valid number.")
        return None


def search_menu():
    query = input("Name or description (Enter to skip): ").strip()
    category = input("Category (Enter to skip): ").strip()
    dietary = input("Dietary preference (Enter to skip): ").strip()
    price_text = input("Maximum price (Enter to skip): ").strip()
    try:
        max_price = float(price_text) if price_text else None
        results = search_foods(query, category, dietary, max_price)
    except ValueError:
        print("Invalid price; showing results without a price filter.")
        results = search_foods(query, category, dietary)
    view_foods(results)


def add_to_cart(cart):
    foods = [food for food in load_foods() if food.get("available", True)]
    view_foods(foods)
    food_id = ask_int("Food ID: ", minimum=1)
    if food_id is None:
        return
    food = next((item for item in foods if item["food_id"] == food_id), None)
    if not food:
        print("Food not found or currently sold out.")
        return
    quantity = ask_int("Quantity: ", minimum=1)
    if quantity is None:
        return
    customization = input("Customization (size/toppings/spice; Enter for none): ").strip()
    cart.add_item(food, quantity, customization)
    print("Added to cart.")


def checkout(username, cart):
    cart.view_cart()
    profile = get_profile(username) or {}
    addresses = profile.get("addresses", [])
    address = ""
    if addresses:
        print("Saved addresses:")
        for index, saved in enumerate(addresses, 1):
            print(f"{index}. {saved}")
        print("0. Enter a new address or choose pickup")
        selection = ask_int("Address choice: ", minimum=0, maximum=len(addresses))
        if selection is None:
            return False
        if selection:
            address = addresses[selection - 1]
    if not address:
        address = input("Delivery address (leave blank for pickup): ").strip()
        if address and address not in addresses:
            if input("Save this address? (y/n): ").strip().casefold() == "y":
                update_profile(username, address=address)
    try:
        tip = float(input("Tip (0 if none): ") or "0")
        if tip < 0:
            raise ValueError
    except ValueError:
        print("Tip must be a non-negative amount.")
        return False
    promo = input("Promo code (WELCOME10 or FOOD20; Enter to skip): ").strip()
    print("Payment options: 1. Cash on delivery/pickup  2. Pay at counter")
    payment_choice = input("Payment choice: ").strip()
    if payment_choice not in ("1", "2"):
        print("Choose a listed payment option.")
        return False
    payment_method = "Cash on delivery" if payment_choice == "1" and address else (
        "Cash on pickup" if payment_choice == "1" else "Pay at counter")
    order = place_order(username, cart.items, address, tip, promo, payment_method)
    cart.items.clear()
    return order


def profile_menu(username):
    profile = get_profile(username) or {}
    print(f"Username: {username}\nPhone: {profile.get('phone') or 'Not set'}")
    for index, address in enumerate(profile.get("addresses", []), 1):
        print(f"Address {index}: {address}")
    if input("Update phone number? (y/n): ").strip().casefold() == "y":
        update_profile(username, phone=input("Phone: ").strip())
    if input("Add a delivery address? (y/n): ").strip().casefold() == "y":
        address = input("Address: ").strip()
        if address:
            update_profile(username, address=address)


def order_menu(username):
    show_order_history(username)
    choice = input("Track (t), cancel (c), review delivered order (r), or Enter to return: ").strip().casefold()
    if choice not in ("t", "c", "r"):
        return
    order_id = ask_int("Order ID: ", minimum=1)
    if order_id is None:
        return
    if choice == "t":
        track_order(username, order_id)
    elif choice == "c":
        cancel_order(username, order_id)
    else:
        rating = ask_int("Rating (1-5): ", minimum=1, maximum=5)
        if rating is not None:
            leave_review(username, order_id, rating, input("Comment: ").strip())


def user_menu(username):
    cart = Cart()
    while True:
        print("\n===== USER MENU =====")
        print("1. Browse menu\n2. Search/filter menu\n3. Add item to cart\n4. View cart")
        print("5. Remove item from cart\n6. Checkout\n7. Orders, tracking, cancellation, reviews")
        print("8. Profile and addresses\n9. Logout")
        choice = input("Choice: ").strip()
        if choice == "1":
            view_foods()
        elif choice == "2":
            search_menu()
        elif choice == "3":
            add_to_cart(cart)
        elif choice == "4":
            cart.view_cart()
        elif choice == "5":
            cart.view_cart()
            food_id = ask_int("Food ID to remove: ", minimum=1)
            if food_id is not None:
                cart.remove_item(food_id)
        elif choice == "6":
            if cart.items:
                checkout(username, cart)
            else:
                print("Cart is empty.")
        elif choice == "7":
            order_menu(username)
        elif choice == "8":
            profile_menu(username)
        elif choice == "9":
            print("Logged out.")
            return
        else:
            print("Invalid choice.")


def main():
    while True:
        print("\n===== FOOD APP =====\n1. Register\n2. Login\n3. Restaurant admin\n4. Exit")
        choice = input("Choice: ").strip()
        if choice == "1":
            username = input("Username: ").strip()
            password = input("Password: ")
            if not username or not password:
                print("Username and password are required.")
            elif register(username, password):
                print("Registration successful.")
            else:
                print("That username is already registered.")
        elif choice == "2":
            username = authenticate(input("Username: ").strip(), input("Password: "))
            if username:
                print("Login successful.")
                user_menu(username)
            else:
                print("Invalid username or password.")
        elif choice == "3":
            admin_user = input("Admin username: ")
            admin_password = input("Admin password: ")
            if admin_credentials_valid(admin_user, admin_password):
                admin_menu()
            else:
                print("Admin credentials are not configured or are incorrect.")
        elif choice == "4":
            print("Thank you!")
            return
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
