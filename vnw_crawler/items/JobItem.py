# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class JobUrlItem():
    _id : str
    name: str
    # job_kind: str
    url : str

@dataclass
class JobDetailItem():
    _id : str
    name: str
    company_id : str
    company: str
    area : str
    salary : str
    day_left : str
    rank : str
    day_start : str
    # job_kind : str
    urgent : Optional[str] = field(default_factory=str)
    career : Optional[str] = None
    detail: Optional[list] = field(default_factory=list)