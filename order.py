import json

def place_order(username,cart_items):
    total = 0
    for item in cart_items:
        total += item['price']
    
    order = {"username" : username, "items": cart_items, "total": total}
    
    with open("orders.json", "r") as file:
        orders = json.load(file)
    orders.append(order)
    
    with open("orders.json", "w") as file:
        json.dump(orders,file,indent=4)
    print("Order Placed Successfully")
        