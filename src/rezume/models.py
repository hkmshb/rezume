from datetime import date
from typing import List, Optional
from pydantic import BaseModel, EmailStr, HttpUrl


class DatedEntry(BaseModel):
    """Represents an entry having a start and end date.
    """

    start_date: date
    end_date: Optional[date]


class NamedKeywords(BaseModel):
    """Represents details describing a named list of keywords.
    """

    name: str
    keywords: Optional[List[str]]


class Education(DatedEntry):
    """Represents details describing an educational qualification.
    """

    institution: str
    study_area: str
    study_type: str = "Bachelor"
    gpa: Optional[str]
    courses: Optional[List[str]]


class Experience(DatedEntry):
    """Represents details describing a work-related experience.
    """

    company: str
    position: str
    summary: Optional[str]
    website: Optional[HttpUrl]
    highlights: Optional[List[str]]


class Language(BaseModel):
    """Represents details describing language spoken.
    """

    language: str = "English"
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
    url: HttpUrl


class Skill(NamedKeywords):
    """Represents details describing skill.
    """

    level: str


class PersonalInfo(BaseModel):
    """Represents personal details for resume owner.
    """

    name: str
    label: str
    email: EmailStr
    location: Location
    phone: Optional[str]
    picture: Optional[str]
    summary: Optional[str]
    website: Optional[HttpUrl]
    profiles: List[Profile]


class Rezume(BaseModel):
    """Represents resume data.
    """

    basics: PersonalInfo
    education: List[Education]
    interests: Optional[List[NamedKeywords]]
    languages: Optional[List[Language]]
    skills: Optional[List[Skill]]
    volunteer: Optional[List[Experience]]
    work: Optional[List[Experience]]
