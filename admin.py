import json


def add_food():
    food_id = int(input("Enter Food ID: "))
    name = input("Enter Food Name: ")
    price = int(input("Enter Price: "))

    with open("foods.json", "r") as file:
        foods = json.load(file)

    foods.append({
        "food_id": food_id,
        "name": name,
        "price": price
    })

    with open("foods.json", "w") as file:
        json.dump(foods, file, indent=4)

    print("Food Added Successfully")