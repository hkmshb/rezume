from copy import deepcopy
from pathlib import Path

import pytest


@pytest.fixture
def rezume_mini():
    """Returns the path to the rezume-mini.yml fixture file."""
    return Path("./tests/fixtures/rezume-mini.yml")


@pytest.fixture
def sample_rezume():
    """Returns the data for a sample rezume as a dict."""
    return deepcopy(
        {
            "basics": {
                "name": "John Doe",
                "label": "Programmer",
                "email": "john@doe.com",
                "phone": "0807-0000-1111",
                "website": "http://johndoe.com",
                "summary": "A summary of john doe...",
                "location": {
                    "address": "276 Alu Avenue",
                    "postal_code": "KN 700214",
                    "city": "Kano",
                    "region": "Kano State",
                    "country_code": "NG",
                },
                "profiles": [
                    {
                        "network": "twitter",
                        "username": "john",
                        "url": "http://twitter.com/john",
                    }
                ],
            },
            "education": [
                {
                    "institution": "University",
                    "area": "Software Engineering",
                    "startDate": "2020-07-05",
                }
            ],
        }
    )
