from typing import TypedDict, TypeVar

T = TypeVar('T')      # Declare type variable

class ValueDict(TypedDict):
    name: str
    value: T
    ambient: T

class IndividualWeight(TypedDict):
    """ Returns the weight """
    name: str
    value: float


class IndividualRewards(TypedDict):
    """ Returns the weight """
    name: str
    value: float