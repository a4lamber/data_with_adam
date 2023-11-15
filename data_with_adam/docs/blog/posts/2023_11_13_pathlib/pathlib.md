---
draft: true
date: 2023-11-13
authors:
  - adam
categories:
  - python
---

# Pathlib vs OS in Python


## Motivation

When i was listening to [real python podcast](https://realpython.com/podcasts/rpp/175/#t=3051) on new features of python 3.12 including `Path.walk()`, it's the time i realize that there is a built-in library `pathlib` in Python (sorry, it took me this long to know this. It's available since 3.4). I was curious to know what is the difference between `pathlib` and `os` module in python. So i decided to write this blog post to share my findings.

## Pain points with OS module and solution

We manipulate file structure on a daily basis, some of the pain points we have are as follows

- **string for storing file path is error prone.** like `path = "~/docs/data.csv"` , if we want to change the file name we have to do string manipulation. It's annoying
- **multiple modules for file manipulation**. You need to use multiple modules and string trick like `os`, `os.path`, `shutil` to do simple file manipulation we can do easily in bash like `ls | grep '.md'` to find out all markdown files in the current directory.


Can we do better than this? That's why pathlib is born.


## What is Pathlib?

Pathlib is a object oriented-way of manipulating the file structure and talk to OS. The implementation is very straightforward, 

```
                +----------+
                |          |
       ---------| PurePath |--------
       |        |          |       |
       |        +----------+       |
       |             |             |
       |             |             |
       v             |             v
+---------------+    |    +-----------------+
|               |    |    |                 |
| PurePosixPath |    |    | PureWindowsPath |
|               |    |    |                 |
+---------------+    |    +-----------------+
       |             v             |
       |          +------+         |
       |          |      |         |
       |   -------| Path |------   |
       |   |      |      |     |   |
       |   |      +------+     |   |
       |   |                   |   |
       |   |                   |   |
       v   v                   v   v
  +-----------+           +-------------+
  |           |           |             |
  | PosixPath |           | WindowsPath |
  |           |           |             |
  +-----------+           +-------------+
```

The OOD design of the `pathlib` is very elegantly designed and the only requiremnt is that it needs to handles two different OS, POSIX and Windows. 

The `PurePath` is the base class for all path classes. `PurePosixPath` and `PureWindowsPath` are the subclasses of `PurePath` for POSIX and Windows respectively. `Path` is the base class for concrete path classes. `PosixPath` and `WindowsPath` are the subclasses of `Path` for POSIX and Windows respectively.

!!! note 
    It's always good to use default python modules instead of third party modules. It's more stable and less dependency. `pathlib` was a third-party module but adopted as a built-in module in python 3.4 in [PEP 428](https://peps.python.org/pep-0428/). So it's safe to use it.


Remember the key difference between pure and concrete classes are as follows,

- pure classes support only operations that don't need to do any actual I/O
- concrete classes support all operations of pure class (it's inherited) but also I/O operations like reading and writing files.

## Example

### Basic attributes

Import the `pathlib` module

```python
from pathlib import Path
```

Define a path
```python
>>> p = Path('~/hello.py')
PosixPath('~/hello.py')
```

You can expand it to absolute path by using `expanduser()` method
```python
>>> pp = p.expanduser()
PosixPath('/Users/adam/hello.py')
```

You can access following useful attributes, 
- the filename by using `name` attribute
- check suffix by using `suffix` attribute

```python
>>> p.suffix
'.py'

>>> p.name
'hellp.py'
```

### Basic methods

```
>>> pp.exists()
True

>>> pp.is_file()
True

>>> pp.is_dir()
False
```

### File opening

similar to the `built-in` open, you can use it for basic read and write. 
```python
with pp.open() as f:
    print(f.readline())
```


### Find all files with specific suffix

Let's create a directory with some files in it.

```python
p = Path('~/data_with_adam/')
```

We can use `glob()` method to find all files with specific suffix.

```python
for child in p.glob('**/*.md'):
    print(child)
```

## Summary

In this post we introduced python built-in module pathlib to handle filepath in an object-oriented way. It's been supported since python 3.4. We have learnt that 
- it's a drop-in replacement of `os` module and say byebye to string manipulation.
- pathlib has pure and concrete classes. 
- it handles both POSIX and Windows OS.

Definitely change my way of working with file structure from now on.

# References
- [PEP 428 - the pathlib module - object oriented filesystem paths](https://peps.python.org/pep-0428/)
- [pathlib python official docs](https://docs.python.org/3/library/pathlib.html)
- [real python](https://realpython.com/python-pathlib/)
- [geeksforgeek](https://www.geeksforgeeks.org/pathlib-module-in-python/)
- [freecodecamp](https://www.freecodecamp.org/news/how-to-use-pathlib-module-in-python/)
