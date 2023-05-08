# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from dataclasses import dataclass

@dataclass
class CategoryAreaItem():
    _id : str #
    name : str
    url : str

@dataclass
class CategoryRankItem():
    _id : str #
    name : str
    url : str

@dataclass
class CategoryJobKindItem():
    _id : str #
    name : str
    url : str

@dataclass
class CategoryCareerItem():
    _id : str #
    name : str
    url : str