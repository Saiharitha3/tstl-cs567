import unittest
pass
from examples.product.inventory import Product, Customer, Supplier, Warehouse, Inventory, Report


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
        self.inventory.add_product("Laptop", "Electronics", 1000, 10, description="A high-performance laptop", supplier_name="TechSupplier", warehouse_name="MainWarehouse")
        self.inventory.add_product("Phone", "Electronics", 500, 20, description="A smart phone", supplier_name="TechSupplier", warehouse_name="SecondaryWarehouse")
        self.inventory.add_product("Shoes", "Apparel", 100, 50, description="Comfortable running shoes", supplier_name="FashionWear", warehouse_name="MainWarehouse")

    def test_product_initialization(self):
        # Test that product attributes are correctly initialized
        product = self.inventory.products["Laptop"]
        self.assertEqual(product.name, "Laptop")
        self.assertEqual(product.category, "Electronics")
        self.assertEqual(product.price, 1000)
        self.assertEqual(product.quantity, 10)
        self.assertEqual(product.description, "A high-performance laptop")
        
    def test_update_product_price(self):
        # Test updating product price
        self.inventory.update_product_price("Laptop", 1200)
        self.assertEqual(self.inventory.products["Laptop"].price, 1200)

        # Test invalid price update (negative price)
        with self.assertRaises(ValueError):
            self.inventory.update_product_price("Laptop", -100)

    def test_update_product_quantity(self):
        # Test updating product quantity
        self.inventory.update_product_quantity("Laptop", 15)
        self.assertEqual(self.inventory.products["Laptop"].quantity, 15)

        # Test invalid quantity update (negative quantity)
        with self.assertRaises(ValueError):
            self.inventory.update_product_quantity("Laptop", -5)

    def test_make_sale(self):
        # Make sale and verify quantity and sales
        self.inventory.make_sale("Alice", "Laptop", 2)
        self.assertEqual(self.inventory.products["Laptop"].quantity, 8)
        self.assertEqual(self.inventory.customers["Alice"].get_purchase_history()["Laptop"], 2)

        # Test sale with insufficient stock
        with self.assertRaises(ValueError):
            self.inventory.make_sale("Alice", "Laptop", 10)

        # Test sale with invalid quantity
        with self.assertRaises(ValueError):
            self.inventory.make_sale("Alice", "Laptop", 0)

    def test_add_review(self):
        # Add review to a product and verify
        self.inventory.products["Laptop"].add_review("Great laptop, very fast!")
        self.assertIn("Great laptop, very fast!", self.inventory.products["Laptop"].get_reviews())

    def test_get_top_selling_products(self):
        # Make some sales for top-selling products
        self.inventory.make_sale("Alice", "Laptop", 2)
        self.inventory.make_sale("Bob", "Phone", 5)
        self.inventory.make_sale("Alice", "Shoes", 10)

        # Verify the top-selling products
        top_selling = self.inventory.get_top_selling_products()
        self.assertEqual(top_selling[0][0], "Shoes")
        self.assertEqual(top_selling[1][0], "Phone")
        self.assertEqual(top_selling[2][0], "Laptop")

    def test_calculate_category_sales(self):
        # Make sales for category-wise revenue calculation
        self.inventory.make_sale("Alice", "Laptop", 2)
        self.inventory.make_sale("Bob", "Phone", 5)
        self.inventory.make_sale("Alice", "Shoes", 10)

        # Calculate and check category sales
        category_sales = self.inventory.calculate_category_sales()
        self.assertGreater(category_sales["Electronics"], category_sales["Apparel"])

    def test_display_customer_purchases(self):
        # Make purchases and display customer history
        self.inventory.make_sale("Alice", "Laptop", 2)
        self.inventory.make_sale("Alice", "Shoes", 3)

        with self.assertRaises(ValueError):
            self.inventory.display_customer_purchases("Bob")

        self.inventory.display_customer_purchases("Alice")

    def test_display_product_reviews(self):
        # Add reviews to products and verify
        self.inventory.products["Laptop"].add_review("Great laptop!")
        self.inventory.products["Phone"].add_review("Nice phone.")
        
        self.inventory.display_product_reviews("Laptop")
        self.inventory.display_product_reviews("Phone")

    def test_warehouse_inventory(self):
        # Display warehouse inventory
        self.inventory.display_warehouses()
        warehouse = self.inventory.warehouses["MainWarehouse"]
        self.assertEqual(warehouse.name, "MainWarehouse")
        self.assertEqual(warehouse.location, "NYC")
        
    def test_supplier_and_warehouse_association(self):
        # Check suppliers and warehouse associations
        self.inventory.add_product("Tablet", "Electronics", 300, 5, supplier_name="TechSupplier", warehouse_name="SecondaryWarehouse")
        product = self.inventory.products["Tablet"]
        self.assertIn("TechSupplier", self.inventory.suppliers)
        self.assertIn("SecondaryWarehouse", self.inventory.warehouses)
        self.assertIn(product.name, self.inventory.warehouses["SecondaryWarehouse"].inventory)

    def test_remove_product(self):
        # Test removing a product from inventory
        self.inventory.remove_product("Phone")
        with self.assertRaises(ValueError):
            self.inventory.remove_product("Phone")

    def test_inventory_report(self):
        # Generate inventory report and verify the output
        with self.assertRaises(ValueError):
            Report.generate_inventory_report(self.inventory.products)

    def test_sales_report(self):
        # Generate sales report and verify
        Report.generate_sales_report(self.inventory.products)
        
    def test_product_not_found(self):
        # Test for non-existing product scenario
        with self.assertRaises(ValueError):
            self.inventory.update_product_price("NonExistentProduct", 100)

    def test_invalid_supplier_addition(self):
        # Add invalid supplier
        with self.assertRaises(ValueError):
            self.inventory.add_supplier("TechSupplier", "1234 Tech St.")

if __name__ == "__main__":
    unittest.main()
