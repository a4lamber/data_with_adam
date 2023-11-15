---
draft: true
date: 2023-10-19
authors:
  - adam
categories:
  - python
---

# Private Name Mangling

## Introduction

Came across this post on DE subreddit. This post is about private name mangling in python, link is [here](https://www.reddit.com/r/dataengineering/comments/179dm3v/linkedin_is_such_a_bad_place_for_python_advice_i/).

In python, it doesn't support strict private variable like other languages such as C++. However, python has a way to "implement" private variable by name mangling. It has everything to do with the number of leading underscore `_` or `__`

|-|description|-|
|-|-|-|
|`self.public`|all can access|-|
|`self._private`|`_` is a friendly hint to other programmer that this variable is private but doesn't enforce rule. You can still access it.|-|
|`self.__protected`|`__` is very `private name mangling` happens. Python will store any variable starts with two leading underscores `__variable` in the form of `_ClassName__variable` with a prefix `_ClassName`|-|

> Analogy of public, private and protected, borrowed from C++

## Example 1 public, private and protected

Free to play with the following code snippet to explore the difference between `public`, `_private` and `__protected` variable.
and how it's handled in python.


```python
class Test:
    def __init__(self) -> None:
        # use of some c++ lingo
        self.public = 11
        self._private =  23
        self.__protected = 42

    def __private_method(self):
        print("private method")
        
if __name__ == "__main__":
    t = Test()
    print(t.__dict__)
    print(f"_private variable: {t._private}")
    print(f"__protected variable: {t._Test__protected}")
    t._Test__private_method()
```

The output of the script is 
```
{'public': 11, '_private': 23, '_Test__protected': 42}
_private variable: 23
__protected variable: 42
private method
```

you can see there is no `__protect` attribute in the namespace of the instance. However, you can still access it by `t._Test__protected`.



## Motivation

The reason behind this feature is that they wish to avoid name collision when inheritance. As project gets larger or working on other people's codebase for example, it is inevitable to name collision between parent and child class.



### Example 2: inspect the `__dict__`

Let's have a class `Class` to illustrate the concept

```python
class Class:
    def __init__(self) -> None:
        self.__student_count = 0

    def get_student_count(self):
        return self.__student_count

    def set_student_count(self, count):
        self.__student_count = count


if __name__ == "__main__":
    c = Class()
    # snapshot 1
    print(c.__dict__)

    # snapshot 2
    c.set_student_count(23)
    print(c.__dict__)

    # snapshot 3
    c.__student_count = 10
    print(c.get_student_count())
    print(c.__dict__)
```

The output is 
```
{'_Class__student_count': 0}
{'_Class__student_count': 23}
23
{'_Class__student_count': 23, '__student_count': 10}
```

When you try to set the variable `__student_count` with setter method, it works as expected. However, when you try to set it directly, it doesn't work. It's because python will store any variable starts with two leading underscores `__variable` in the form of `_ClassName__variable` with a prefix `_ClassName`. It is illustrated in the `__dict__` of the instance.


## Example 3: class and math class

Let's say we have two classes,
- `Class`: a class with a private variable `__count`, written by author 1 foo. He wants to keep track of the number of students in the class.
- `MathClass`: a class that inherits from `Class` and has a private variable `__count` as well,, written by author 2 bar. He wants to keep track of the number of textbook used for the math class.

author 1 left the job and author 2 inherit the `class Class` and name his own class `MathClass`. He wants to use `__count` as well but to count completely different things. He will create his own setter and getter method for `__count` as well. A code snippet is shown below.

```python
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
```

Output is here. It works fine.
```
{'_Class__count': 0}
{'_Class__count': 0, '_MathClass__count': 10}
{'_Class__count': 0}
{'_Class__count': 0, '_MathClass__count': 20}
```

But imagine if there is no `name mangling feature` in python to treat `__count` as `_<ClassName>__count`. The output will be
```
{'__count': 0}
{'__count': 10}
{'__count': 0}
{'__count': 20}
```

You will be accidentally overwrite the variable `__count` in the parent class but it stand for different meaning in the parent class. This is the reason why python has this feature.

## Summary

In this section, we touched upon
- private, public and protected variable in python
- name mangling in python with example

private name mangling is kinda debatable feature. It's python's effort to adopt more statically typed features from other languages. It's not a perfect solution but it's a solution. It's a trade off between flexibility and safety.

This feature acts as a fail-safe for programmer to make mistakes. Also it's advocate for better naming, if we change it to
- `self.__count` in `class Class`to `self.student_count`
- `self.__count` in `class MathClass`to `self.textbook_count`

It's more clear and less confusing and you should put more thoughts into naming things to be more pragmatic. It echos there are two hard things in computer science: cache invalidation, and naming things.

## Reference

- [mcoding: private name mangling](https://www.youtube.com/watch?v=0hrEaA3N3lk&t=91s&ab_channel=mCoding)
- [real python](https://www.youtube.com/watch?v=ALZmCy2u0jQ&ab_channel=RealPython)
