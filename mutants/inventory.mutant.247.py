from datetime import datetime


class Product:
    def __init__(self, name, category, price, quantity, description=""):
        self.name = name
        self.category = category
        self.price = price
        self.quantity = quantity
        self.sales = []  # (quantity, sale_date)
        self.reviews = []
        self.description = description

    def update_price(self, new_price):
        if new_price < 0:
            raise ValueError("Price cannot be negative")
        self.price = new_price

    def update_quantity(self, new_quantity):
        if new_quantity < 0:
            raise ValueError("Quantity cannot be negative")
        self.quantity = new_quantity

    def add_sale(self, quantity_sold):
        if quantity_sold <= 0:
            raise ValueError("Quantity sold must be positive")
        if quantity_sold > self.quantity:
            raise ValueError("Not enough stock to sell")
        self.quantity -= quantity_sold
        self.sales.append((quantity_sold, datetime.now()))

    def get_sales(self):
        return self.sales

    def get_revenue(self):
        return sum(quantity for quantity, _ in self.sales) * self.price

    def add_review(self, review):
        self.reviews.append(review)

    def get_reviews(self):
        return self.reviews

    def apply_discount(self, discount_percentage):
        if not 0 < discount_percentage <= 100:
            raise ValueError("Discount percentage must be between 0 and 100")
        self.price *= (1 - discount_percentage / 100)

    def needs_restock(self, threshold=10):
        return self.quantity < threshold

    def __str__(self):
        return f"{self.name} ({self.category}) - ${self.price:.2f}, {self.quantity} in stock"


class Customer:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.purchases = {}

    def make_purchase(self, product_name, quantity):
        if product_name not in self.purchases:
            self.purchases[product_name] = 0
        self.purchases[product_name] += quantity

    def get_purchase_history(self):
        return self.purchases

    def notify_about_new_product(self, product_name):
        print(f"Email to {self.email}: New product '{product_name}' is now available!")

    def add_reward_points(self, points):
        if not hasattr(self, 'reward_points'):
            self.reward_points = 0
        self.reward_points += points

    def get_reward_points(self):
        return getattr(self, 'reward_points', 0)

    def __str__(self):
        return f"Customer: {self.name} ({self.email})"


class Supplier:
    def __init__(self, name, contact_info):
        self.name = name
        self.contact_info = contact_info
        self.products_supplied = []

    def supply_product(self, product_name):
        self.products_supplied.append(product_name)

    def rate_supplier(self, rating):
        if not hasattr(self, 'ratings'):
            self.ratings = []
        if not 0 <= rating <= 5:
            raise ValueError("Rating must be between 0 and 5")
        self.ratings.append(rating)

    def average_rating(self):
        if not hasattr(self, 'ratings') or not self.ratings:
            return None
        return sum(self.ratings) / len(self.ratings)

    def get_supply_list(self):
        return self.products_supplied

    def __str__(self):
        return f"Supplier: {self.name} - Contact: {self.contact_info} - Products Supplied: {', '.join(self.products_supplied)}"


class Warehouse:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.inventory = {}

    def add_product(self, product: Product, quantity: int):
        if product.name in self.inventory:
            self.inventory[product.name].update_quantity(self.inventory[product.name].quantity + quantity)
        else:
            self.inventory[product.name] = product
            product.update_quantity(quantity)

    def remove_product(self, product_name: str):
        if product_name not in self.inventory:
            raise ValueError(f"Product {product_name} not found in warehouse {self.name}")
        del self.inventory[product_name]

    def suggest_reallocation(self, other_warehouse):
        for product_name, product in self.inventory.items():
            if product_name in other_warehouse.inventory:
                if product.quantity <= other_warehouse.inventory[product_name].quantity:
                    diff = (product.quantity - other_warehouse.inventory[product_name].quantity) // 2
                    print(f"Move {diff} units of {product_name} to {other_warehouse.name}")

    def display_inventory(self):
        print(f"\nInventory at {self.name} ({self.location}):")
        for product in self.inventory.values():
            print(product)

    def __str__(self):
        return f"Warehouse: {self.name} located in {self.location}"


class Inventory:
    def __init__(self):
        self.products = {}
        self.customers = {}
        self.suppliers = {}
        self.warehouses = {}

    def add_product(self, name, category, price, quantity, description="", supplier_name=None, warehouse_name=None):
        if name in self.products:
            raise ValueError("Product already exists in inventory")
        self.products[name] = Product(name, category, price, quantity, description)
        if supplier_name:
            if supplier_name not in self.suppliers:
                self.suppliers[supplier_name] = Supplier(supplier_name, contact_info="Unknown")
            self.suppliers[supplier_name].supply_product(name)
        if warehouse_name:
            if warehouse_name not in self.warehouses:
                self.warehouses[warehouse_name] = Warehouse(warehouse_name, location="Unknown")
            self.warehouses[warehouse_name].add_product(self.products[name], quantity)

    def remove_product(self, name):
        if name not in self.products:
            raise ValueError("Product not found")
        del self.products[name]

    def update_product_price(self, name, new_price):
        if name not in self.products:
            raise ValueError("Product not found")
        self.products[name].update_price(new_price)

    def update_product_quantity(self, name, new_quantity):
        if name not in self.products:
            raise ValueError("Product not found")
        self.products[name].update_quantity(new_quantity)

    def adjust_pricing_based_on_demand(self):
        for product in self.products.values():
            total_sales = sum(quantity for quantity, _ in product.get_sales())
            if total_sales > 50:  # Example threshold
                product.update_price(product.price * 1.10)  # Increase by 10%
            elif total_sales < 10:
                product.update_price(product.price * 0.90)  # Decrease by 10%

    def display_products(self):
        print("\nCurrent Inventory:")
        for product in self.products.values():
            print(product)

    def make_sale(self, customer_name, product_name, quantity_sold):
        if product_name not in self.products:
            raise ValueError("Product not found")
        if customer_name not in self.customers:
            self.customers[customer_name] = Customer(customer_name, email="unknown@example.com")

        product = self.products[product_name]
        product.add_sale(quantity_sold)
        self.customers[customer_name].make_purchase(product_name, quantity_sold)

    def search_products(self, category=None, price_range=None, in_stock_only=False):
        results = []
        for product in self.products.values():
            if category and product.category != category:
                continue
            if price_range and not (price_range[0] <= product.price <= price_range[1]):
                continue
            if in_stock_only and product.quantity == 0:
                continue
            results.append(product)
        return results

    def display_customer_purchases(self, customer_name):
        if customer_name not in self.customers:
            raise ValueError("Customer not found")
        purchases = self.customers[customer_name].get_purchase_history()
        print(f"\nPurchase History for {customer_name}:")
        for product_name, quantity in purchases.items():
            print(f"{product_name}: {quantity} units")

    def display_product_reviews(self, product_name):
        if product_name not in self.products:
            raise ValueError("Product not found")
        product = self.products[product_name]
        print(f"\nReviews for {product_name}:")
        for review in product.get_reviews():
            print(f"- {review}")

    def add_supplier(self, name, contact_info):
        self.suppliers[name] = Supplier(name, contact_info)

    def add_warehouse(self, name, location):
        self.warehouses[name] = Warehouse(name, location)

    def display_warehouses(self):
        print("\nList of Warehouses:")
        for warehouse in self.warehouses.values():
            print(warehouse)


class Report:
    @staticmethod
    def generate_inventory_report(products):
        print("\nInventory Report:")
        for name, product in products.items():
            print(f"{product.name} - {product.category} - Revenue: ${product.get_revenue():.2f}")
        total_value = sum(p.price * p.quantity for p in products.values())
        print(f"Total Inventory Value: ${total_value:.2f}")

    @staticmethod
    def generate_sales_report(products):
        print("\nSales Report:")
        for name, product in products.items():
            total_sales = sum(quantity for quantity, _ in product.get_sales())
            print(f"{product.name} - Total Units Sold: {total_sales}, Revenue: ${product.get_revenue():.2f}")

    @staticmethod
    def generate_category_revenue_report(products):
        category_revenue = {}
        for product in products.values():
            if product.category not in category_revenue:
                category_revenue[product.category] = 0
            category_revenue[product.category] += sum(quantity for quantity, _ in product.get_sales()) * product.price
        print("\nCategory Revenue Report:")
        for category, revenue in category_revenue.items():
            print(f"{category}: ${revenue:.2f}")


if __name__ == "__main__":
    inventory = Inventory()
