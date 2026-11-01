"""Menu loading, search, and display."""

import json

FOODS_FILE = "foods.json"


class Food:
    def __init__(self, food_id, name, price, **details):
        self.food_id = food_id
        self.name = name
        self.price = price
        self.details = details


def load_foods():
    with open(FOODS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def view_foods(foods=None):
    foods = load_foods() if foods is None else foods
    print("\n==== FOOD MENU ====")
    if not foods:
        print("No available items right now.")
        return
    for food in foods:
        if not food.get("available", True):
            continue
        details = food.get("description", "")
        category = food.get("category", "Other")
        diet = food.get("dietary", "")
        print(f"ID: {food['food_id']} | {food['name']} | ₹{food['price']} | {category}"
              f"{(' | ' + diet) if diet else ''}{(' | ' + details) if details else ''}")


def search_foods(query="", category="", dietary="", max_price=None):
    query = query.casefold().strip()
    category = category.casefold().strip()
    dietary = dietary.casefold().strip()
    matches = []
    for food in load_foods():
        if not food.get("available", True):
            continue
        if query and query not in (food["name"] + " " + food.get("description", "")).casefold():
            continue
        if category and category not in food.get("category", "").casefold():
            continue
        if dietary and dietary not in food.get("dietary", "").casefold():
            continue
        if max_price is not None and food["price"] > max_price:
            continue
        matches.append(food)
    return matches
