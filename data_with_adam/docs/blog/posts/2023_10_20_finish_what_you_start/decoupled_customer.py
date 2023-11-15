class Customer:
    """A customer with a name and a balance to handle
    bank balance transactions"""

    def __init__(self, name):
        self.name = name
        self.balance = None

    def read_customer(self, file):
        """read a line from the file and set the balance"""
        self.balance = float(file.readline())

    def write_customer(self, file):
        """write the balance to the file"""
        file.seek(0)
        file.write(str(self.balance))

    def update_customer(self, transaction_amount):
        """update the customer's balance"""
        with open(self.name + ".rec", "r+", encoding="utf-8") as file:
            self.read_customer(file)
            self.balance += transaction_amount
            self.write_customer(file)


if __name__ == "__main__":
    customer = Customer("john_doe")

    # update the customer's balance
    customer.update_customer(50.25)
