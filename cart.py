class Cart:

    def __init__(self):
        self.items = []

    def add_item(self, food):
        self.items.append(food)

    def remove_item(self, food_id):
        for item in self.items:
            if item["food_id"] == food_id:
                self.items.remove(item)
                print(f"{item['name']} removed from the cart.")
                return
        print("Food not found in the cart.")

    def view_cart(self):
        if len(self.items) == 0:
            print("Cart is Empty!")
            return

        total = 0
        print("\n===== YOUR CART =====")
        for item in self.items:
            print(f"ID: {item['food_id']}")
            print(f"Food : {item['name']}")
            print(f"Price: ₹{item['price']}")
            print("----------------------")
            total += item["price"]
        print(f"Total = ₹{total}")