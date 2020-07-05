from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class DatedEntry(BaseModel):
    """Represents an entry having a start and end date.
    """

    start_date: datetime
    end_date: Optional[datetime]


class NamedKeywords(BaseModel):
    """Represents details describing a named list of keywords.
    """

    name: str
    keywords: Optional[List[str]]
