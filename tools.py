# The shop's tools. You can change this file if you need to, apart from stock_sdk_lookup.

import asyncio
import time
from decimal import Decimal

CATALOGUE = [
    {"id": "p-101", "name": "Whey Protein Powder (Chocolate)", "price": Decimal("24.99"), "vegan": False},
    {"id": "p-102", "name": "Vegan Protein Powder (Chocolate)", "price": Decimal("27.99"), "vegan": True},
    {"id": "p-103", "name": "Vegan Protein Bar (Peanut)", "price": Decimal("2.49"), "vegan": True},
]

_basket = {}


def stock_sdk_lookup(product_id):
    # The warehouse's Python SDK (third party). Don't change this function.
    time.sleep(0.5)
    return product_id != "p-103"


async def search_products(query, max_price=None):
    await asyncio.sleep(0.5)  # the search service takes about half a second
    words = query.lower().split()
    return [
        p for p in CATALOGUE
        if any(w in p["name"].lower() for w in words)
        and (max_price is None or p["price"] <= max_price)
    ]


async def get_product(product_id):
    for p in CATALOGUE:
        if p["id"] == product_id:
            return p
    raise ValueError(f"Unknown product {product_id}")


async def check_stock(product_id):
    in_stock = stock_sdk_lookup(product_id)
    return {"product_id": product_id, "in_stock": in_stock}


async def add_to_basket(product_id, quantity):
    await get_product(product_id)
    stock = await check_stock(product_id)
    if not stock["in_stock"]:
        raise ValueError(f"{product_id} is out of stock")
    _basket[product_id] = _basket.get(product_id, 0) + quantity
    return {"ok": True}


async def track_order(order_id):
    await asyncio.sleep(30)  # the order service sometimes doesn't answer
    return {"order_id": order_id, "status": "dispatched"}


def get_basket():
    return dict(_basket)


TOOLS = {
    "search_products": search_products,
    "get_product": get_product,
    "check_stock": check_stock,
    "add_to_basket": add_to_basket,
    "track_order": track_order,
}
