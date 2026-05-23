#!/usr/bin/env python3
"""E-Commerce Platform Generator."""

import json, sys
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class Store:
    name: str
    description: str
    products: list = field(default_factory=list)
    categories: list = field(default_factory=list)
    payment_gateways: list = field(default_factory=list)
    files: dict = field(default_factory=dict)

class EcomGenerator:
    def create(self, description: str) -> Store:
        store = Store(
            name=self._gen_name(description),
            description=description,
        )
        store.categories = self._gen_categories(description)
        store.products = self._gen_products(store.categories)
        store.payment_gateways = ["stripe", "midtrans"]
        store.files = self._gen_files(store)
        return store

    def _gen_name(self, desc: str) -> str:
        words = desc.split()[:3]
        return "-".join(w.lower() for w in words if w.isalpha())

    def _gen_categories(self, desc: str) -> list:
        cats = ["General"]
        lower = desc.lower()
        for kw, cat in [("fashion", "Clothing"), ("food", "Food & Beverage"),
                        ("tech", "Electronics"), ("beauty", "Beauty & Health")]:
            if kw in lower:
                cats.append(cat)
        return cats

    def _gen_products(self, categories: list) -> list:
        products = []
        templates = {
            "Clothing": [("T-Shirt", 25.99), ("Jeans", 49.99), ("Jacket", 89.99)],
            "Food & Beverage": [("Coffee Blend", 12.99), ("Snack Box", 19.99)],
            "Electronics": [("Phone Case", 15.99), ("USB Cable", 9.99)],
            "Beauty & Health": [("Face Wash", 14.99), ("Moisturizer", 29.99)],
            "General": [("Product A", 19.99), ("Product B", 29.99), ("Product C", 39.99)],
        }
        for cat in categories:
            for name, price in templates.get(cat, templates["General"]):
                products.append({"name": name, "price": price, "category": cat, "stock": 100})
        return products

    def _gen_files(self, store: Store) -> dict:
        return {
            "package.json": json.dumps({
                "name": store.name, "version": "1.0.0",
                "dependencies": {"next": "14.0.0", "react": "18.2.0", "stripe": "14.0.0"},
            }, indent=2),
            "config.json": json.dumps({
                "store": store.name, "currency": "USD",
                "payments": store.payment_gateways,
                "categories": store.categories,
            }, indent=2),
        }

    def deploy(self, store: Store, platform: str = "vercel") -> dict:
        return {"store": store.name, "platform": platform, "url": f"https://{store.name}.vercel.app",
                "products": len(store.products), "status": "deployed"}

def main():
    if len(sys.argv) < 3:
        print("Usage: python main.py create 'store description'")
        sys.exit(1)
    gen = EcomGenerator()
    desc = " ".join(sys.argv[2:])
    store = gen.create(desc)
    print(f"Store: {store.name}")
    print(f"Categories: {store.categories}")
    print(f"Products: {len(store.products)}")
    for p in store.products[:5]:
        print(f"  {p["name"]} - ${p["price"]}")

if __name__ == "__main__":
    main()
