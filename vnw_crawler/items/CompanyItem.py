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
    career: Optional[str] = None
    area : Optional[str] = None
    follow : Optional[str] = None
    social: Optional[str] = field(default_factory=str)
    infor : Optional[list] = field(default_factory=list)