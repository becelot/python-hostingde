from dataclasses import dataclass
from enum import Enum

from marshmallow_enum import EnumField

from python_hde.model import Model


class SortOrder(Enum):
    ASC = 'ASC'
    DESC = 'DESC'


@dataclass
class SortConfiguration(Model):
    """
    Adds sorting configuration to the endpoint
    """

    field: str
    order: SortOrder = EnumField(SortOrder)

    def __init__(self, field: str, order: SortOrder):
        """
        The field you want to order on.

        :param field: The field name
        :param order: The ordering of the results. Either 'ASC' or 'DESC'
        """
        super().__init__()
        self.field: str = field
        self.order: SortOrder = order
