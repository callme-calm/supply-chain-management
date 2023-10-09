from datetime import datetime
import rsa


class Node:

    def __init__(self, user_type=None, user_name=None):
        self.user_type = user_type
        self.user_name = user_name
        self.public_key = ""
        self.private_key = ""
        self.productReceived = False
        self.productSend = False
        self.product = None
        self.set_keys()

    def set_keys(self):
        self.public_key, self.private_key = rsa.newkeys(100)

    """
    Performs the action of receiving a product with the given product ID.
    This function updates the status of the product to indicate that it has been received.
    """

    def receive_product(self, product, issue=None):
        if not product or self.product:
            return False

        self.product = product
        self.productReceived = True

        if not issue: product.set_status(self, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "receive")

        return True

    """
    Performs the action of sending a product with the given product ID to the specified recipient.
    This function updates the status of the product to indicate that it has been sent to the recipient.
    """

    def send_product(self):
        if not self.product and self.user_type != 'manufacturer':
            print("No product present")
            return False

        # send product to the concerned person
        self.product.set_status(self, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "send")
        self.product = None
        self.productReceived = False
        self.productSend = True

    def __str__(self):
        return f"User Type: {self.user_type}, User Name: {self.user_name}, " \
               f"Public Key: {self.public_key}, " \
               f"Product Received: {self.productReceived}, " \
               f"Product Sent: {self.productSend}, Product: {None if not self.product else self.product.product_name}"


class ManufacturerNode(Node):
    def __init__(self, user_type=None, user_name=None):
        super().__init__(user_type, user_name)
        self.products = []

    """
    Add products in manufacturer's list
    """

    def add_products(self, product):
        self.products.append(product)

    """
    Sends multiple products from the given product list to the specified recipient.
    This function iterates over the product list, sends each product to the recipient, and updates their status accordingly.
    """

    def send_product_from_list(self, product):
        if len(product.history):
            print("Error: product not with manufacturer")
            return False
        for product_it in self.products:
            if product == product_it:
                self.product = product_it
                super().send_product()

    def __str__(self):
        parent_str = super().__str__()
        products_info = [product.product_name for product in self.products]
        return f"{parent_str}, Products: {products_info}"
