class Test:
    def __init__(self) -> None:
        # use of some c++ lingo
        self.public = 11
        self._private =  23
        self.__protected = 42

    def __private_method(self):
        print("private method")
        
    # def public_method(self):
    #     print(f"The result of self.__private_method: {self.__private_method}")
    #     print(f"The value of self.__private_method: {self.__private_method}")


if __name__ == "__main__":
    t = Test()
    print(t.__dict__)
    print(f"_private variable: {t._private}")
    print(f"__protected variable: {t._Test__protected}")
    t._Test__private_method()
    
    
   
    