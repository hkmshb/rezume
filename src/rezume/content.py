from typing import List, Optional
from pydantic import BaseModel

from .base import DatedEntry, Section, NamedSection, TimelinedSection


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
    website: Optional[str]
    summary: Optional[str]
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
    url: str


class NamedKeywords(BaseModel):
    """Represents details describing a named list of keywords.
    """

    name: str
    keywords: Optional[List[str]]


class Skill(NamedKeywords):
    """Represents details describing skill.
    """

    level: str


class Interest(NamedKeywords):
    """Represents details describing an interest.
    """

    pass


class EducationSet(NamedSection, TimelinedSection):
    """Represents a set of details describing educational qualifications.
    """

    name = "education"

    def _generate_key(self, item: Education):
        return f"{item.institution}:{item.study_area}:{item.study_type}"

    def _sorter(self, item: Education):
        return item.start_date


class ExperienceSet(NamedSection, TimelinedSection):
    """Represents a set of details describing work related experiences.
    """

    name = "experience"

    def _generate_key(self, item: Experience):
        key = f"{item.company}:{item.position}"
        if item.start_date:
            key += f":{item.start_date.strftime('%Y%m')}"
        return key


class LanguageSet(NamedSection):
    """Represents a set of spoken languages.
    """

    name = "language"

    def _generate_key(self, item: Language):
        return item.language


class ProfileSet(Section):
    """Represents a set of profiles.
    """

    def _generate_key(self, elem: Profile) -> str:
        return elem.network

    def _sorter(self, elem: Profile) -> str:
        return elem.network


class SkillSet(NamedSection):
    """Represents a set of skills.
    """

    name = "skill"

    def _generate_key(self, item: Skill):
        return item.name
