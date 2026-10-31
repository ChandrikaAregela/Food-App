"""Restaurant menu and order management."""

import json
from food import load_foods
from order import STATUSES, admin_show_orders, admin_update_status


def add_food():
    foods = load_foods()
    food_id = max((food["food_id"] for food in foods), default=0) + 1
    name = input("Food name: ").strip()
    try:
        price = float(input("Price: "))
        if price <= 0:
            raise ValueError
    except ValueError:
        print("Enter a valid price greater than zero.")
        return
    foods.append({"food_id": food_id, "name": name, "price": price,
                  "category": input("Category: ").strip() or "Other",
                  "description": input("Description: ").strip(),
                  "dietary": input("Dietary tag (e.g. vegetarian): ").strip(),
                  "available": True})
    _save_foods(foods)
    print(f"Food added with ID {food_id}.")


def _save_foods(foods):
    with open("foods.json", "w", encoding="utf-8") as file:
        json.dump(foods, file, indent=4)


def manage_availability():
    foods = load_foods()
    for food in foods:
        print(f"{food['food_id']}. {food['name']} — {'Available' if food.get('available', True) else 'Sold out'}")
    try:
        food_id = int(input("Food ID to toggle availability: "))
    except ValueError:
        print("Enter a valid food ID.")
        return
    food = next((item for item in foods if item["food_id"] == food_id), None)
    if food:
        food["available"] = not food.get("available", True)
        _save_foods(foods)
        print(f"{food['name']} is now {'available' if food['available'] else 'sold out'}.")
    else:
        print("Food not found.")


def manage_order_status():
    admin_show_orders()
    try:
        order_id = int(input("Order ID to update: "))
    except ValueError:
        print("Enter a valid order ID.")
        return
    print("Statuses: " + ", ".join(STATUSES + ["Cancelled"]))
    status = input("New status: ").strip().title()
    choices = {choice.casefold(): choice for choice in STATUSES + ["Cancelled"]}
    if status.casefold() not in choices:
        print("Unknown status.")
        return
    admin_update_status(order_id, choices[status.casefold()])


def admin_menu():
    while True:
        print("\n===== RESTAURANT ADMIN =====")
        print("1. Add menu item\n2. Mark item available/sold out\n3. View/update orders\n4. Logout")
        choice = input("Choice: ").strip()
        if choice == "1":
            add_food()
        elif choice == "2":
            manage_availability()
        elif choice == "3":
            manage_order_status()
        elif choice == "4":
            return
        else:
            print("Invalid choice.")
