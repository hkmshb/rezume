from datetime import date
from typing import List, Optional
from pydantic import BaseModel, EmailStr, HttpUrl


class Model(BaseModel):
    class Config:
        @classmethod
        def alias_generator(cls, value: str) -> str:
            [word, *words] = value.split("_")
            return "".join([word] + [word.capitalize() for word in words])


class DatedEntry(Model):
    """Represents an entry having a start and end date.
    """

    start_date: date
    end_date: Optional[date]


class NamedKeywords(Model):
    """Represents details describing a named list of keywords.
    """

    name: str
    keywords: Optional[List[str]]


# =============================================================================
# Personal Info


class Location(Model):
    """Represents a physical contact address.
    """

    address: str
    postal_code: Optional[str]
    region: str
    city: Optional[str]
    country_code: Optional[str] = "NG"


class Profile(Model):
    """Represents a profile on a social or professional network.
    """

    network: str
    username: str
    url: Optional[HttpUrl]


class PersonalInfo(Model):
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


class Reference(Model):
    """Represents details describing reference received.
    """

    name: str
    reference: str


# =============================================================================
# Experience & Education


class Education(DatedEntry):
    """Represents details describing an educational qualification.
    """

    institution: str
    area: str
    study_type: str = "Bachelor"
    gpa: Optional[str]
    courses: Optional[List[str]]


class Experience(DatedEntry):
    """Represents base model for experience related objects.
    """

    position: str
    summary: Optional[str]
    website: Optional[HttpUrl]
    highlights: Optional[List[str]]


class Work(Experience):
    """Represents details describing a work-related experience.
    """

    company: str


class Volunteer(Experience):
    """Represents details describing a volunteer-related experience.
    """

    organization: str


# =============================================================================
# Ability


class Language(Model):
    """Represents details describing language spoken.
    """

    language: str = "English"
    fluency: str


class Skill(NamedKeywords):
    """Represents details describing skill.
    """

    level: str


# =============================================================================
# Achievements


class Award(Model):
    """Represents details describing a received award.
    """

    title: str
    awarder: str
    date: date
    summary: Optional[str]


class Publication(Model):
    """Represents details describing a publication.
    """

    name: str
    publisher: str
    release_date: date
    summary: Optional[str]
    website: Optional[HttpUrl]


# =============================================================================
# Rezume


class Rezume(Model):
    """Represents resume data.
    """

    basics: PersonalInfo
    work: Optional[List[Work]]
    volunteer: Optional[List[Volunteer]]
    education: List[Education]
    awards: Optional[List[Award]]
    publications: Optional[List[Publication]]
    skills: Optional[List[Skill]]
    languages: Optional[List[Language]]
    interests: Optional[List[NamedKeywords]]
    references: Optional[List[Reference]]
