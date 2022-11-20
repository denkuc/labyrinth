from abc import abstractmethod, ABC
from typing import Optional


class Collection(ABC):
    FIRST_ELEMENT_INDEX = 0
    LAST_ELEMENT_INDEX = -1

    @abstractmethod
    def __init__(self, elements):
        self.__elements = elements

    def is_empty(self) -> bool:
        return self.count() == 0

    def count(self) -> int:
        return len(self.__elements)

    def __len__(self) -> int:
        return self.count()

    def first(self):
        return (self.__elements or [None])[self.FIRST_ELEMENT_INDEX]

    def last(self):
        return (self.__elements or [None])[self.LAST_ELEMENT_INDEX]

    def get_as_tuple(self) -> tuple:
        if isinstance(self.__elements, tuple) is False:
            return tuple(self.__elements)
        else:
            return self.__elements

    def get_as_list(self) -> list:
        if isinstance(self.__elements, list) is False:
            return list(self.__elements)
        else:
            return self.__elements

    def __iter__(self):
        return iter(self.__elements)

    def __next__(self):
        element = next(self.__elements) or None
        if element is None:
            raise StopIteration

        return element

    def get_with_limit(self, limit: int) -> list:
        elements_as_list = self.get_as_list()
        if limit > len(elements_as_list):
            return elements_as_list

        return self.__elements[:limit]


class MutableCollection(Collection):
    def __init__(self, elements: Optional[list] = None):
        if elements is None:
            elements = []
        super().__init__(elements)

    def add(self, element_to_add):
        self.get_as_list().append(element_to_add)

    def extend(self, collection_to_extend):
        raise Exception('This method is not allowed for collections. Please use merge() instead!')

    def copy(self):
        return self.get_as_list().copy()

    def pop(self):
        return self.get_as_list().pop()

    def merge(self, collection: Collection):
        self.get_as_list().extend(collection.get_as_list())

    def remove(self, element_to_remove):
        self.get_as_list().remove(element_to_remove)

    def remove_all(self):
        self.get_as_list().clear()

    def _insert_at_index(self, element_to_insert, index: int):
        elements = self.get_as_list()
        elements.insert(index, element_to_insert)
        self.__init__(elements)
