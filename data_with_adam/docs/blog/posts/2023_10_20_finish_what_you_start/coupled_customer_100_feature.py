class Customer:
    def __init__(self, name):
        self.name = name
        self.balance = None

    def read_customer(self):
        self.customer_file = open(self.name + ".rec", "r+")
        self.balance = float(self.customer_file.readline().strip())

    def write_customer(self):
        self.customer_file.seek(0)
        self.customer_file.write(str(self.balance))
        self.customer_file.truncate()
        self.customer_file.close()

    def update_customer(self, transaction_amount):
        self.read_customer()
        if transaction_amount > 100:
            self.balance += float(transaction_amount)
            self.write_customer()


if __name__ == "__main__":
    # update the customer's balance
    customer = Customer("john_doe")
    customer.update_customer(100)
