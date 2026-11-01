"""Order checkout, history, tracking, cancellation, and reviews."""

import json
from datetime import datetime

ORDERS_FILE = "orders.json"
DELIVERY_FEE = 40
TAX_RATE = 0.05
PROMO_CODES = {"WELCOME10": 0.10, "FOOD20": 0.20}
STATUSES = ["Confirmed", "Preparing", "Ready for pickup", "Out for delivery", "Delivered"]


def _read_orders():
    with open(ORDERS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def _write_orders(orders):
    with open(ORDERS_FILE, "w", encoding="utf-8") as file:
        json.dump(orders, file, indent=4)


def place_order(username, cart_items, address="", tip=0, promo_code="", payment_method=""):
    subtotal = sum(item["price"] * item.get("quantity", 1) for item in cart_items)
    promo_code = promo_code.strip().upper()
    discount = round(subtotal * PROMO_CODES.get(promo_code, 0))
    delivery_fee = DELIVERY_FEE if address else 0
    tax = round((subtotal - discount) * TAX_RATE)
    total = subtotal - discount + tax + delivery_fee + tip
    orders = _read_orders()
    order_id = max((order.get("order_id", 0) for order in orders), default=1000) + 1
    order = {
        "order_id": order_id, "username": username,
        "items": [dict(item) for item in cart_items], "subtotal": subtotal,
        "discount": discount, "promo_code": promo_code if discount else "",
        "tax": tax, "delivery_fee": delivery_fee, "tip": tip, "total": total,
        "address": address, "payment_method": payment_method,
        "status": "Confirmed", "created_at": datetime.now().isoformat(timespec="minutes"),
        "review": None,
    }
    orders.append(order)
    _write_orders(orders)
    print(f"\n===== RECEIPT: ORDER #{order_id} =====")
    print(f"Subtotal: ₹{subtotal}\nDiscount: -₹{discount}\nTax: ₹{tax}")
    print(f"Delivery fee: ₹{delivery_fee}\nTip: ₹{tip}\nTotal: ₹{total}")
    print(f"Payment: {payment_method or 'Not specified'} | Status: Confirmed")
    print("Estimated delivery: 30–45 minutes" if address else "Pickup estimate: 20–30 minutes")
    return order


def user_orders(username):
    return [order for order in _read_orders() if order.get("username") == username]


def show_order_history(username):
    orders = user_orders(username)
    if not orders:
        print("You have no orders yet.")
        return
    for order in orders:
        order_id = order.get("order_id", "Legacy")
        status = order.get("status", "Delivered (legacy order)")
        print(f"Order #{order_id} | {status} | ₹{order['total']} | {order.get('created_at', 'Date unavailable')}")
        for item in order["items"]:
            print(f"  {item['name']} x {item.get('quantity', 1)}")


def cancel_order(username, order_id):
    orders = _read_orders()
    for order in orders:
        if order.get("username") == username and order.get("order_id") == order_id:
            if order.get("status") != "Confirmed":
                print("Orders can only be cancelled while confirmed.")
                return False
            order["status"] = "Cancelled"
            _write_orders(orders)
            print(f"Order #{order_id} cancelled.")
            return True
    print("Order not found.")
    return False


def track_order(username, order_id):
    order = next((item for item in user_orders(username)
                  if item.get("order_id") == order_id), None)
    if order:
        print(f"Order #{order_id}: {order.get('status', 'Status unavailable')}")
        if order.get("address"):
            print(f"Delivering to: {order['address']}")
        return order
    print("Order not found.")
    return None


def leave_review(username, order_id, rating, comment):
    orders = _read_orders()
    for order in orders:
        if order.get("username") == username and order.get("order_id") == order_id:
            if order.get("status") != "Delivered":
                print("You can review an order after it is delivered.")
                return False
            order["review"] = {"rating": rating, "comment": comment}
            _write_orders(orders)
            print("Thanks for your review!")
            return True
    print("Order not found.")
    return False


def admin_update_status(order_id, status):
    orders = _read_orders()
    for order in orders:
        if order.get("order_id") == order_id:
            order["status"] = status
            _write_orders(orders)
            print(f"Order #{order_id} updated to {status}.")
            return True
    print("Order not found.")
    return False


def admin_show_orders():
    for order in _read_orders():
        print(f"#{order.get('order_id', 'Legacy')} {order.get('username')} | "
              f"{order.get('status', 'Legacy')} | ₹{order['total']}")
