from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar

T = TypeVar('T')


class Observer(ABC, Generic[T]):
    @abstractmethod
    def update(self, value: T) -> None:
        ...


class ObservableAttribute(Generic[T]):
    def __init__(self, observers: list[Observer[T]]) -> None:
        self.value: Optional[T] = None
        self.observers = observers

    def __get__(self, obj: object, type: type = None) -> T:
        if self.value is None:
            raise AttributeError('Not set')
        return self.value

    def __set__(self, obj: object, value: T) -> None:
        self.value = value
        for observer in self.observers:
            observer.update(self.value)

    @classmethod
    def create(cls) -> tuple[list[Observer[T]], ObservableAttribute[T]]:
        observers: list[Observer[T]] = []
        return observers, cls(observers)


class ObservableExample:
    a_observers, a = ObservableAttribute[int].create()
    c_observers, c = ObservableAttribute[str].create()

    def __init__(self, a: int, b: int, c: str) -> None:
        self.a = a
        self.b = b
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

