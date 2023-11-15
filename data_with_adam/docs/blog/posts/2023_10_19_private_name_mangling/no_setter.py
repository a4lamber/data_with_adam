class Class:
    def __init__(self) -> None:
        # author 1: foo
        # number of students in the class
        self.__count = 0

    def get_count(self):
        return self.__count

    def set_count(self, count):
        self.__count = count


class MathClass(Class):
    def __init__(self) -> None:
        super().__init__()
        # author 2: bar
        # number of textbook used for the math class
        self.__count = 10

    def get_count(self):
        return self.__count

    def set_count(self, count):
        self.__count = count


if __name__ == "__main__":
    c = Class()
    math_c = MathClass()

    print(c.__dict__)
    print(math_c.__dict__)

    math_c.set_count(20)
    print(c.__dict__)
    print(math_c.__dict__)
