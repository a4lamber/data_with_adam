class Class:
    def __init__(self) -> None:
        self.__student_count = 0

    def get_student_count(self):
        return self.__student_count

    def set_student_count(self, count):
        self.__student_count = count


class MathClass(Class):
    def __init__(self) -> None:
        super().__init__()
        self.__student_count = 10

    # def get_student_count(self):
    #     return self.__student_count

    # def set_student_count(self, count):
    #     self.__student_count = count


if __name__ == "__main__":
    c = Class()
    math_c = MathClass()

    print(c.__dict__)
    print(math_c.__dict__)

    math_c.set_student_count(20)
    print(c.__dict__)
    print(math_c.__dict__)
