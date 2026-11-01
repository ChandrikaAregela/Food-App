"""In-memory shopping cart with quantities and item customizations."""


class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, food, quantity=1, customization=""):
        existing = next((item for item in self.items
                         if item["food_id"] == food["food_id"] and
                         item.get("customization", "") == customization), None)
        if existing:
            existing["quantity"] += quantity
        else:
            self.items.append({**food, "quantity": quantity,
                               "customization": customization})

    def remove_item(self, food_id):
        for item in self.items:
            if item["food_id"] == food_id:
                self.items.remove(item)
                print(f"{item['name']} removed from the cart.")
                return
        print("Food not found in the cart.")

    def subtotal(self):
        return sum(item["price"] * item.get("quantity", 1) for item in self.items)

    def view_cart(self):
        if not self.items:
            print("Cart is Empty!")
            return
        print("\n===== YOUR CART =====")
        for item in self.items:
            quantity = item.get("quantity", 1)
            print(f"ID: {item['food_id']} | {item['name']} x {quantity} | ₹{item['price'] * quantity}")
            if item.get("customization"):
                print(f"  Customization: {item['customization']}")
        print(f"Subtotal = ₹{self.subtotal()}")
