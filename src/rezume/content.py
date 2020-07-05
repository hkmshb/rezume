from typing import List, Optional
from pydantic import BaseModel

from .base import DatedEntry, NamedKeywords


class Education(DatedEntry):
    """Represents details describing an educational qualification.
    """

    institution: str
    study_area: str
    study_type: str = "Bachelor"
    gpa: Optional[float]
    courses: Optional[List[str]]


class Experience(DatedEntry):
    """Represents details describing a work-related experience.
    """

    company: str
    position: str
    website: Optional[str]
    summary: Optional[str]
    highlights: Optional[List[str]]


class Language(BaseModel):
    """Represents details describing language spoken.
    """

    name: str = "English"
    fluency: str


class Location(BaseModel):
    """Represents a physical contact address.
    """

    address: str
    postal_code: Optional[str]
    region: str
    city: Optional[str]
    country_code: Optional[str] = "NG"


class Profile(BaseModel):
    """Represents a profile on a social or professional network.
    """

    network: str
    username: str
    url: str


class Skill(NamedKeywords):
    """Represents details describing skill.
    """

    level: str


class Interest(NamedKeywords):
    """Represents details describing an interest.
    """

    pass
