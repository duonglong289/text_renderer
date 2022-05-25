from dataclasses import dataclass

@dataclass
class Test:
    param1: str = "Hello"
    param2: str = "Hello"


abc = Test()

print(abc.meta('param1'))