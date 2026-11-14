from pydantic import BaseModel, Field, field_validator
from enum import Enum



class Rule(Enum):

    CATASTROPHIC = "A"
    HAZARDOUS = "B"
    MAJOR = "C"
    MINOR = "D"
    NO_EFFECT = "E"


class Detail(BaseModel):
    id: str
    title: str
    category: str
    year: int = Field(gt=1903, lt=2027)
    serial_number: str = Field(min_length=1 , max_length=15)
    # serial_number/SER - уникальный серийный номер
    rule: Rule
    # rule - правило АП-25, указывающие на критичность при поломке

    @field_validator("id", "title" , "category" , "serial_number")
    @classmethod
    def check_len(cls, value:str) -> str:
        if not value.strip():
            raise ValueError(f"detail cannot be empty")
        return value

    @field_validator("serial_number")
    @classmethod
    def check_ser(cls, value:str) -> str:
        if not value.isascii() or not value.isalnum():
            raise ValueError(f"serial_number {value} is incorrect")
        return value 
