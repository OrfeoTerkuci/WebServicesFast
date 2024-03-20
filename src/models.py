"""
This module contains the Pydantic models for the API parameters.
"""
from pydantic import BaseModel


class CountryName(BaseModel):
    name: str


class Country(BaseModel):
    name: CountryName
    capital: str
    population: int
    area: float
    currency: str
    language: str
    timezone: str
    continent: str
