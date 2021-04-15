from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar

T = TypeVar('T')


class Observer(ABC, Generic[T]):
    @abstractmethod
    def update(self, value: T) -> None:
        ...


class ObservableAttribute(Generic[T]):
    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, instance: object, value: T) -> None:
        instance.__dict__[self.name] = value
        observers = getattr(instance, self.name + '_observers')
        for observer in observers:
            observer.update(value)


class ObservableExample:
    a = ObservableAttribute[int]()
    c = ObservableAttribute[str]()

    def __init__(self, a: int, b: int, c: str) -> None:
        self.a_observers: list[Observer[int]] = []
        self.a = a
        self.b = b
        self.c_observers: list[Observer[str]] = []
        self.c = c

    def a_register(self, observer: Observer[int]) -> None:
        self.a_observers.append(observer)

    def c_register(self, observer: Observer[str]) -> None:
        self.c_observers.append(observer)


class ConcreteObserver(Observer[int]):
    def update(self, value: int) -> None:
        print(f'I have been notified the value is now {value}')


example = ObservableExample(1, 2, 'three')
observer = ConcreteObserver()

# before registering, the observer does not get updated
example.a += 1

# after registering, the observer gets notified anytime
# the attribute changes.
example.a_register(observer)
example.a += 1
example.a = 1

# the observer does not get notified when other attributes change
example.c = 'nine'
example.b = 1

# other Observable instances do not notify observers of pre-existing
# instances
example2 = ObservableExample(900, 1, 'ok')

