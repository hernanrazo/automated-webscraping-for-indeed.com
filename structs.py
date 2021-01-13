from dataclasses import dataclass
from dataclasses_json import dataclass_json
from datetime import datetime
from typing import List, Dict


@dataclass_json
@dataclass
class JobInfo:
    job_id: str
    title: str
    company: str
    location: str
    salary: str
    date_listed: str
    date_scraped: datetime
    company_rating: float
    rank: int
    page_num: int
    url: str
    description: str
