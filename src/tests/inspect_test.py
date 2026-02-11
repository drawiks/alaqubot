import inspect

class MyClass:
    def __init__(self):
        self.data = 1
    def method(self):
        print("Hello")

obj = MyClass()

all_members = inspect.getmembers(obj)

methods = inspect.getmembers(obj, predicate=inspect.ismethod)

print(methods)