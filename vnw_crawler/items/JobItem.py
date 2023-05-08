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
    date_update: str
    job_kind: str
    url : str

@dataclass
class JobDetailItem():
    _id : str
    name: str
    company: str
    area : str
    wage : str
    date_start : str
    day_left : str
    rank : str
    job_kind : str
    urgent : Optional[str] = field(default_factory=str)
    career : Optional[str] = None
    detail: Optional[list] = field(default_factory=list)