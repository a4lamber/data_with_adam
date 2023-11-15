---
draft: true
date: 2023-10-20
authors:
  - adam
categories:
  - data
---

# Finish What You Start

- [Finish What You Start](#finish-what-you-start)
- [Motivation](#motivation)
- [Example](#example)
  - [Coupled code](#coupled-code)
  - [Decoupled code](#decoupled-code)
- [What happens with python open a file?](#what-happens-with-python-open-a-file)
- [Summary](#summary)
- [Reference](#reference)


# Motivation
When i was reading pragmatic programmer, i came across this tip,
> Finish What You Start

It means that for function and object that allocate resources, you should also free them. This is a good practice to avoid memory leak.


# Example
Let's take a look at the `class Customer` that handles the customer account information.


## Coupled code

First, let's take a look at a coupled code that violates the `finish what you start` principle.

```python
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
        self.balance += float(transaction_amount)
        self.write_customer()


if __name__ == "__main__":
    # update the customer's balance
    customer = Customer("john_doe")
    customer.update_customer(100)
```

It has a couple of read flag, the `read_customer` and `write_customer` are coupled together because,
- they share `self.customer_file`.
- `read_customer` open up the file and `write_customer` close the file

Then, `update_customer` calls upon `read_customer` and `write_customer` to update the customer's balance. The OS resource that has been allocated to `self.customer_file` is freed by `update_customer`.

This is a bad practice because it's not clear who is responsible for freeing the OS resource. And as we receive a new ticket, let's say we can only update balance if the customer transaction amount is positive, then the code will look like this.

```python
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
        if transaction_amount > 0:
            self.balance += float(transaction_amount)
            self.write_customer()


if __name__ == "__main__":
    # update the customer's balance
    customer = Customer("john_doe")
    customer.update_customer(100)
```

It will cause that the customer file is not closed if the transaction amount is negative. After a while, the OS resource will be exhausted and the program will crash (imagine many transactions per minute).

## Decoupled code

To fix this, we can decouple the `read_customer` and `write_customer` by passing a file handle to them.

```python
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
```

|problem|solution|
|-|-|
|coupling from `self.customer_file`|refactor it out and pass in `file handle` instead|
|`update_customer` may violates the finish where you start principle once|`with open()` in python, the `context manager` that does resource management for you |


# What happens with python open a file?

It goes through a series of steps,
- `request the OS:` python needs to talk to OS by making a system call.
- `check the file mode:` check if the file is opened in read, write or append mode to make sure we can operate on the file.
- `file descriptor:` the OS will return a file descriptor to python, which is an integer that represents the file. Recall the unix philosophy, `everything is a file` or more precisely `everything is a file descriptor`.
- `file handle (file object) creation:`  Python creates a file handle that represents the opened file. This file object is used to perform various operations on the file, such as reading, writing, and seeking.

In the meantime, python will be responsible for the resource management for the operation we perform on the file. 


# Summary

In this section, we covered 
- the `finish what you start` principle 
- how to decouple the code to avoid the problem with `customer class` example
- a bit dig-in on what's behind the scene when python open a file and the rise of `context manager`


In order to reduce the occurrences of the problem for python developer, context manager has been released in python 2.5. After that, developer always use `with open()` to open a file, which reduces the occurrences of the problem. So much effort has been put into guiding the developer to do the right thing and we are taking it for granted.

> Note: The same principle applied to database connection. If you don't do it properly, it will occupy the connection pool. 

Python `context manager` has more than just `with open()`. Feel free to explore it `from contextlib import contextmanager`, i have a link in the reference section.

# Reference
- [context manager, python tips](https://book.pythontips.com/en/latest/context_managers.html)
- [Corey Schafer!!!](https://www.youtube.com/watch?v=-aKFBoZpiqA&ab_channel=CoreySchafer)











