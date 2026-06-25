import json

class Food:
    def __init__(self, food_id, name, price):
        self.food_id = food_id
        self.name = name
        self.price = price

def view_foods():
      with open("foods.json", "r") as file:
        foods = json.load(file)

      print("\n==== FOOD MENU ====")

      for food in foods:
        print(f"ID: {food['food_id']} | "f"Name: {food['name']} | "f"Price: ₹{food['price']}")