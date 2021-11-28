from enum import Enum


class StrEnum(str, Enum):
    """
    Используется для создания строковых констант
    """
    def __new__(cls, value, *args):
        obj = str.__new__(cls, value)
        obj._value_ = value

        obj.additional_fields = args
        return obj

    def __str__(self):
        return str(self.value)

    def __hash__(self):
        return self.value.__hash__()

    @property
    def value(self):
        """
        Вернет то, что было указано при объявлении Enum'а. Планируется, что
        в большинстве случаев это будет `str`.
        """
        return super(StrEnum, self).value

    def __eq__(self, other):
        return str(self.value) == other

    def __ne__(self, other):
        return str(self.value) != other

    def __radd__(self, other):
        return other + str(self.value)
