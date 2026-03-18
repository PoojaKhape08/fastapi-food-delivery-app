from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi import Query

app = FastAPI()

class OrderRequest(BaseModel):
    customer_name: str = Field(..., min_length=2)
    item_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0, le=20)
    delivery_address: str = Field(..., min_length=10)
    order_type: str = "delivery"

class CheckoutRequest(BaseModel):
    customer_name: str
    delivery_address: str
    
class NewMenuItem(BaseModel):
    name: str = Field(..., min_length=2)
    price: int = Field(..., gt=0)
    category: str = Field(..., min_length=2)
    is_available: bool = True

@app.get("/")
def home():
    return {"message": "Welcome to QuickBite Food Delivery"}

menu = [
    {"id": 1, "name": "Margherita Pizza", "price": 250, "category": "Pizza", "is_available": True},
    {"id": 2, "name": "Veg Burger", "price": 120, "category": "Burger", "is_available": True},
    {"id": 3, "name": "Coke", "price": 50, "category": "Drink", "is_available": True},
    {"id": 4, "name": "Chocolate Cake", "price": 180, "category": "Dessert", "is_available": False},
    {"id": 5, "name": "Paneer Pizza", "price": 300, "category": "Pizza", "is_available": True},
    {"id": 6, "name": "French Fries", "price": 100, "category": "Snack", "is_available": True}
]

def find_menu_item(item_id):
    for item in menu:
        if item["id"] == item_id:
            return item
    return None


def calculate_bill(price, quantity, order_type):
    total = price * quantity

    if order_type == "delivery":
        total += 30

    return total

def filter_menu_logic(category=None, max_price=None, is_available=None):
    result = []

    for item in menu:
        if category is not None and item["category"] != category:
            continue

        if max_price is not None and item["price"] > max_price:
            continue

        if is_available is not None and item["is_available"] != is_available:
            continue

        result.append(item)

    return result

@app.get("/menu")
def get_menu():
    return {
        "total": len(menu),
        "items": menu
    }

@app.post("/menu")
def add_menu_item(item: NewMenuItem):
    new_id = len(menu) + 1

    # duplicate check
    for m in menu:
        if m["name"].lower() == item.name.lower():
            return {"error": "Item already exists"}

    new_item = {
        "id": new_id,
        "name": item.name,
        "price": item.price,
        "category": item.category,
        "is_available": item.is_available
    }

    menu.append(new_item)

    return new_item
    
@app.get("/menu/summary")
def menu_summary():
    total_items = len(menu)
    available = sum(1 for item in menu if item["is_available"])
    unavailable = total_items - available
    categories = list(set(item["category"] for item in menu))

    return {
        "total_items": total_items,
        "available_items": available,
        "unavailable_items": unavailable,
        "categories": categories
    }

@app.get("/menu/filter")
def filter_menu(
    category: str = Query(None),
    max_price: int = Query(None),
    is_available: bool = Query(None)
):
    filtered = filter_menu_logic(category, max_price, is_available)

    return {
        "total": len(filtered),
        "items": filtered
    }

@app.get("/menu/search")
def search_menu(keyword: str):
    result = []

    for item in menu:
        if keyword.lower() in item["name"].lower() or keyword.lower() in item["category"].lower():
            result.append(item)

    if not result:
        return {"message": "No items found"}

    return {
        "total_found": len(result),
        "items": result
    }

@app.get("/menu/sort")
def sort_menu(sort_by: str = "price", order: str = "asc"):
    
    valid_fields = ["price", "name", "category"]

    if sort_by not in valid_fields:
        return {"error": "Invalid sort_by value"}

    if order not in ["asc", "desc"]:
        return {"error": "Invalid order value"}

    reverse = True if order == "desc" else False

    sorted_menu = sorted(menu, key=lambda x: x[sort_by], reverse=reverse)

    return {
        "sort_by": sort_by,
        "order": order,
        "items": sorted_menu
    }

@app.get("/menu/page")
def paginate_menu(page: int = 1, limit: int = 3):
    
    start = (page - 1) * limit
    end = start + limit

    paginated_items = menu[start:end]

    total = len(menu)
    total_pages = (total + limit - 1) // limit

    return {
        "page": page,
        "limit": limit,
        "total_items": total,
        "total_pages": total_pages,
        "items": paginated_items
    }

@app.get("/menu/browse")
def browse_menu(
    keyword: str = None,
    sort_by: str = "price",
    order: str = "asc",
    page: int = 1,
    limit: int = 4
):

    result = menu

    # Search
    if keyword:
        result = [
            item for item in result
            if keyword.lower() in item["name"].lower()
            or keyword.lower() in item["category"].lower()
        ]

    # Sort
    reverse = True if order == "desc" else False
    result = sorted(result, key=lambda x: x[sort_by], reverse=reverse)

    # Pagination
    start = (page - 1) * limit
    end = start + limit

    paginated = result[start:end]

    total = len(result)
    total_pages = (total + limit - 1) // limit

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
        "items": paginated
    }
    
@app.get("/menu/{item_id}")
def get_item(item_id: int):
    for item in menu:
        if item["id"] == item_id:
            return item
    return {"error": "Item not found"}

@app.put("/menu/{item_id}")
def update_menu_item(
    item_id: int,
    price: int = None,
    is_available: bool = None
):
    item = find_menu_item(item_id)

    if not item:
        return {"error": "Item not found"}

    if price is not None:
        item["price"] = price

    if is_available is not None:
        item["is_available"] = is_available

    return item

@app.delete("/menu/{item_id}")
def delete_menu_item(item_id: int):
    item = find_menu_item(item_id)

    if not item:
        return {"error": "Item not found"}

    menu.remove(item)

    return {"message": f"{item['name']} deleted successfully"}

orders = []
order_counter = 1

@app.get("/orders/search")
def search_orders(customer_name: str):
    result = []

    for order in orders:
        if customer_name.lower() in order["customer_name"].lower():
            result.append(order)

    return {
        "total_found": len(result),
        "orders": result
    }

@app.get("/orders/sort")
def sort_orders(order: str = "asc"):

    if order not in ["asc", "desc"]:
        return {"error": "Invalid order"}

    reverse = True if order == "desc" else False

    sorted_orders = sorted(orders, key=lambda x: x["total_price"], reverse=reverse)

    return {
        "order": order,
        "orders": sorted_orders
    }

@app.get("/orders")
def get_orders():
    return {
        "total_orders": len(orders),
        "orders": orders
    }

@app.post("/orders")
def create_order(order: OrderRequest):
    global order_counter

    item = find_menu_item(order.item_id)

    if not item:
        return {"error": "Item not found"}

    if not item["is_available"]:
        return {"error": "Item not available"}

    total_price = calculate_bill(item["price"], order.quantity, order.order_type)

    new_order = {
        "order_id": order_counter,
        "customer_name": order.customer_name,
        "item_name": item["name"],
        "quantity": order.quantity,
        "total_price": total_price,
        "delivery_address": order.delivery_address
    }

    orders.append(new_order)
    order_counter += 1

    return new_order

cart = []

@app.post("/cart/add")
def add_to_cart(item_id: int, quantity: int = 1):
    item = find_menu_item(item_id)

    if not item:
        return {"error": "Item not found"}

    if not item["is_available"]:
        return {"error": "Item not available"}

    # check if already in cart
    for c in cart:
        if c["item_id"] == item_id:
            c["quantity"] += quantity
            return {"message": "Quantity updated", "cart": cart}

    # add new item
    cart.append({
        "item_id": item_id,
        "name": item["name"],
        "price": item["price"],
        "quantity": quantity
    })

    return {"message": "Item added to cart", "cart": cart}

@app.get("/cart")
def view_cart():
    total = sum(item["price"] * item["quantity"] for item in cart)

    return {
        "cart_items": cart,
        "grand_total": total
    }

@app.delete("/cart/{item_id}")
def remove_from_cart(item_id: int):
    for item in cart:
        if item["item_id"] == item_id:
            cart.remove(item)
            return {"message": "Item removed from cart"}

    return {"error": "Item not found in cart"}

@app.post("/cart/checkout")
def checkout(data: CheckoutRequest):
    global order_counter

    if not cart:
        return {"error": "Cart is empty"}

    created_orders = []
    grand_total = 0

    for c in cart:
        total_price = calculate_bill(c["price"], c["quantity"], "delivery")

        new_order = {
            "order_id": order_counter,
            "customer_name": data.customer_name,
            "item_name": c["name"],
            "quantity": c["quantity"],
            "total_price": total_price,
            "delivery_address": data.delivery_address
        }

        orders.append(new_order)
        created_orders.append(new_order)
        grand_total += total_price
        order_counter += 1

    cart.clear()

    return {
        "message": "Order placed successfully",
        "orders": created_orders,
        "grand_total": grand_total
    }
