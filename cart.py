class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, food):
        self.items.append(food)

    def view_cart(self):
        total = 0
        if len(self.items) == 0:
            print("Cart is Empty")
            return

        print("\nYOUR CART")

        for item in self.items:
            print(f"{item['name']} - ₹{item['price']}")
            total += item["price"]
        print(f"\nTotal = ₹{total}")