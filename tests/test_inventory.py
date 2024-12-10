import unittest
from unittest.mock import patch
from product.inventory import Product, Customer, Supplier, Warehouse, Inventory, Report


class TestInventorySystem(unittest.TestCase):
    
    def setUp(self):
        # Set up an instance of Inventory for testing
        self.inventory = Inventory()

        # Add suppliers and warehouses
        self.inventory.add_supplier("TechSupplier", "1234 Tech St.")
        self.inventory.add_supplier("FashionWear", "9876 Fashion Blvd.")
        self.inventory.add_warehouse("MainWarehouse", "NYC")
        self.inventory.add_warehouse("SecondaryWarehouse", "LA")

        # Add products
        self.inventory.add_product(
            "Laptop", "Electronics", 1000, 10, description="A high-performance laptop",
            supplier_name="TechSupplier", warehouse_name="MainWarehouse"
        )
        self.inventory.add_product(
            "Phone", "Electronics", 500, 20, description="A smart phone",
            supplier_name="TechSupplier", warehouse_name="SecondaryWarehouse"
        )
        self.inventory.add_product(
            "Shoes", "Apparel", 100, 50, description="Comfortable running shoes",
            supplier_name="FashionWear", warehouse_name="MainWarehouse"
        )

    def test_product_initialization(self):
        product = self.inventory.products["Laptop"]
        self.assertEqual(product.name, "Laptop")
        self.assertEqual(product.category, "Electronics")
        self.assertEqual(product.price, 1000)
        self.assertEqual(product.quantity, 10)
        self.assertEqual(product.description, "A high-performance laptop")

    def test_update_product_price(self):
        self.inventory.update_product_price("Laptop", 1200)
        self.assertEqual(self.inventory.products["Laptop"].price, 1200)
        with self.assertRaises(ValueError):
            self.inventory.update_product_price("Laptop", -100)

    def test_update_product_quantity(self):
        self.inventory.update_product_quantity("Laptop", 15)
        self.assertEqual(self.inventory.products["Laptop"].quantity, 15)
        with self.assertRaises(ValueError):
            self.inventory.update_product_quantity("Laptop", -5)

    def test_make_sale(self):
        self.inventory.make_sale("Alice", "Laptop", 2)
        self.assertEqual(self.inventory.products["Laptop"].quantity, 8)
        self.assertEqual(self.inventory.customers["Alice"].get_purchase_history()["Laptop"], 2)

        with self.assertRaises(ValueError):
            self.inventory.make_sale("Alice", "Laptop", 10)

        with self.assertRaises(ValueError):
            self.inventory.make_sale("Alice", "Laptop", 0)

    def test_add_review(self):
        self.inventory.products["Laptop"].add_review("Great laptop, very fast!")
        self.assertIn("Great laptop, very fast!", self.inventory.products["Laptop"].get_reviews())

    def test_calculate_category_sales(self):
        self.inventory.make_sale("Alice", "Laptop", 2)
        self.inventory.make_sale("Bob", "Phone", 5)
        self.inventory.make_sale("Alice", "Shoes", 10)

        category_sales = self.inventory.calculate_category_sales()
        self.assertGreater(category_sales["Electronics"], category_sales["Apparel"])

    def test_display_customer_purchases(self):
        self.inventory.make_sale("Alice", "Laptop", 2)
        self.inventory.make_sale("Alice", "Shoes", 3)
        with self.assertRaises(ValueError):
            self.inventory.display_customer_purchases("Bob")

        self.inventory.display_customer_purchases("Alice")

    def test_display_product_reviews(self):
        self.inventory.products["Laptop"].add_review("Great laptop!")
        self.inventory.products["Phone"].add_review("Nice phone.")
        self.inventory.display_product_reviews("Laptop")
        self.inventory.display_product_reviews("Phone")

    def test_supplier_and_warehouse_association(self):
        self.inventory.add_product("Tablet", "Electronics", 300, 5, supplier_name="TechSupplier", warehouse_name="SecondaryWarehouse")
        product = self.inventory.products["Tablet"]
        self.assertIn("TechSupplier", self.inventory.suppliers)
        self.assertIn("SecondaryWarehouse", self.inventory.warehouses)
        self.assertIn(product.name, self.inventory.warehouses["SecondaryWarehouse"].inventory)

    def test_remove_product(self):
        self.inventory.remove_product("Phone")
        with self.assertRaises(ValueError):
            self.inventory.remove_product("Phone")

    def test_inventory_report(self):
        report = Report.generate_inventory_report(self.inventory.products)
        self.assertIn("Laptop", report)
        self.assertIn("Phone", report)

    def test_sales_report(self):
        self.inventory.make_sale("Alice", "Laptop", 2)
        report = Report.generate_sales_report(self.inventory.products)
        self.assertIn("Laptop", report)

    def test_product_not_found(self):
        with self.assertRaises(ValueError):
            self.inventory.update_product_price("NonExistentProduct", 100)

    def test_invalid_supplier_addition(self):
        with self.assertRaises(ValueError):
            self.inventory.add_supplier("TechSupplier", "1234 Tech St.")

    def test_product_discounts(self):
        product = self.inventory.products["Laptop"]
        product.apply_discount(10)
        self.assertEqual(product.price, 900)
        with self.assertRaises(ValueError):
            product.apply_discount(110)

    def test_warehouse_inventory(self):
        warehouse = self.inventory.warehouses["MainWarehouse"]
        inventory_items = warehouse.display_inventory()
        self.assertIn("Laptop", inventory_items)
        self.assertIn("Shoes", inventory_items)

    def test_update_price_negative(self):
        product = Product("Test Product", "Test Category", 10.0, 100)
        with self.assertRaises(ValueError):
            product.update_price(-5)

    def test_add_sale_insufficient_stock(self):
        product = Product("Test Product", "Test Category", 10.0, 10)
        with self.assertRaises(ValueError):
            product.add_sale(15)

    def test_apply_discount(self):
        product = Product("Test Product", "Test Category", 100.0, 50)
        product.apply_discount(20)
        self.assertEqual(product.price, 80.0)

    def test_warehouse_add_remove(self):
        warehouse = Warehouse("Main Warehouse", "City Center")
        product = Product("Widget", "Gadget", 25.0, 0)
        warehouse.add_product(product, 100)
        self.assertIn("Widget", warehouse.inventory)
        warehouse.remove_product("Widget")
        self.assertNotIn("Widget", warehouse.inventory)


if __name__ == "__main__":
    unittest.main()
