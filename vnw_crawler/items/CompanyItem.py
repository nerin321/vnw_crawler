# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from dataclasses import dataclass, field
from typing import Optional

@dataclass 
class CompanyUrlItem():
    _id : str #
    name: str
    url : str

@dataclass
class CompanySubUrlItem():
    _id : str #
    name: str
    url : str

@dataclass
class CompanyDetailItem():
    _id : str #
    name: str
    company_url : str
    career: str
    follow : Optional[str] = None
    area : Optional[str] = None
    social: Optional[str] = None
    address: Optional[list] = field(default_factory=list)

@dataclass
class CompanySubDetailItem():
    _id : str
    name : str
    follower : str
    address : str
    career : str
    headquarters : Optional[str] = None
    scale : Optional[str] = None
    contact : Optional[str] = None
    benefit : Optional[list] = field(default_factory=list)