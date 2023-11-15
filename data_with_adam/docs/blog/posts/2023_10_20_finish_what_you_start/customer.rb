# code snippet 1: 耦合度很高的代码
def read_customer(file)
    @customer_file = File.open(@name + ".rec", "r+")
    @balance=BigDecimal(@customer_file.gets)
end

def write_customer(file)
    @customer_file.rewind
    @customer_file.puts @balance.to_s
    @customer_file.close
end

def update_customer(transaction_amount) 
    read_customer
    @balance = @balance.add(transaction_amount)
    write_customer
end


# code snippet 2: 降低耦合度的代码
def read_customer(file)
    @balance=BigDecimal(file.gets)
end

def write_customer(file)
    file.rewind
    file.puts @balance.to_s
end

def update_customer(transaction_amount) 
    file = File.open(@name + ".rec", "r+")
    read_customer(file)
    @balance = @balance.add(transaction_amount)
    write_customer(file)
    file.close
end


