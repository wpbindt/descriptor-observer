from typing import Generic, Optional, Protocol, TypeVar

T = TypeVar('T')


class Observer(Protocol[T]):
    def update(self, value: T) -> None:
        ...


class ObservableAttribute(Generic[T]):
    def __init__(self, observers: list[Observer[T]]) -> None:
        self.value: Optional[T] = None
        self.observers = observers

    def __get__(self, obj, type=None) -> T:
        if self.value is None:
            raise AttributeError('Not set')
        return self.value

    def __set__(self, obj, value: T) -> None:
        self.value = value
        for observer in self.observers:
            observer.update(self.value)


class ObservableExample:
    a_observers = []
    a = ObservableAttribute(a_observers)
    c_observers = []
    a = ObservableAttribute(c_observers)

    def __init__(self, a: int, b: int, c: str) -> None:
        self.a = a
        self.b = b
        self.c = c

    def a_register(self, observer: Observer[int]) -> None:
        self.a_observers.append(observer)

    def c_register(self, observer: Observer[str]) -> None:
        self.c_observers.append(observer)
