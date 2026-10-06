

def calculate_subtotal(items: list[dict[str, any]]) -> float:
    subtotal = 0.0
    for item in items:
        price = item["price"]
        quantity = item["qty"]
        if price <= 0 or quantity <= 0:
            continue
        subtotal += price * quantity
    return subtotal 


def calculate_discount(subtotal: float, is_member: bool) -> float:
    if not is_member:
        return 0.0
    if subtotal > 100:
        return subtotal * 0.2
    if subtotal > 50:
        return subtotal * 0.1
    return 0.0


def calculate_shipping(country: str) -> float:
    if country == "PK":
        return 5.0
    if country == "US":
        return 15.0
    return 25.0


def calculate_order_total(order: dict[str, any]) -> float:
    subtotal = calculate_subtotal(order["items"])
    discount = calculate_discount(subtotal, order["member"])
    shipping = calculate_shipping(order["country"])
    return subtotal - discount + shipping