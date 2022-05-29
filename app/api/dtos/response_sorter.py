from enum import Enum
from typing import Optional

from pydantic import BaseModel


class SorterDirection(str, Enum):
    ASC = "ASC"
    DESC = "DESC"


class ResponseSorter(BaseModel):
    field: str
    direction: Optional[SorterDirection] = SorterDirection.DESC
