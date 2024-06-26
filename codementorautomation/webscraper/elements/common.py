from typing import ClassVar, Type

from selenium_objects import Element, Selector
from selenium_objects.elements.common import LazyList


class LazyCardList(LazyList):
    """Common card list found on Codementor pages with the exception of the 
    sessions card list.
    """
    selector = Selector(by='css selector', value='.dashboard')
    item_element: ClassVar[Type[Element]]
    item_element = None
    lazy_load_wait_time = .8