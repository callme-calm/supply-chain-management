from datetime import datetime

import qrcode


class Product:
    counter = 1

    def __init__(self, product_id, product_name, timestamp, at=None):
        self.product_id = product_id
        self.product_name = product_name

        self.history = []

        # self.status = "In Manufacturer's Warehouse"  # Initialize status

    def set_status(self, node, timestamp, type_of_status):
        print(f"Setting status for {self.product_name, self.product_id}...")
        print(f'Setting done by: {node.user_name}')

        if self.history:
            latest_record = self.history[-1]
            print(
                f'Latest history record: at={latest_record["at"].user_name}, time={latest_record["time"]}, type={latest_record["type"]}')

        status_record = {"at": node, "time": timestamp, "type": type_of_status}
        self.history.append(status_record)

        # print(len(self.history))
        print(f'Now: at={status_record["at"].user_name}, time={status_record["time"]}, type={status_record["type"]}')
        self.print_qr_code()
    """
    Sets the status of an item with the given item ID to the specified status.
    This function updates the status of an item in the system based on the provided item ID and status.
    """

    def print_qr_code(self):
        if self.history:
            qr_data = f"Product ID: {self.product_id}\nProduct Name: {self.product_name}\nCurrent Location: {self.history[-1]['at'].user_name}\nTime: {self.history[-1]['time']}"
        else:
            qr_data = f"Product ID: {self.product_id}\nProduct Name: {self.product_name}\nCurrent Location: " \
                      f"manufacturer \nTime: {datetime.now()}"
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")

            img.save(f"qr/my_qr_code{self.counter}.png")
            # img.show()
            self.counter += 1
            return True
        except Exception:
            print("Error in creating qrcode")
            return False
    """
    Prints a QR code representing the given data.
    This function generates a QR code image based on the provided data and prints it.
    """
    def to_dict(self):
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "history": len(self.history),
        }

    """
    Converts an object to a dictionary representation.
    This function takes an object as input and returns a dictionary representation of the object.
    """