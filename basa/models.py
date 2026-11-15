from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Rule(Enum):
    """Правило АП-25 через Enum"""

    CATASTROPHIC = "A"
    HAZARDOUS = "B"
    MAJOR = "C"
    MINOR = "D"
    NO_EFFECT = "E"


class Detail(BaseModel):
    """Авиационная деталь через Pydantic и валидация некоторых полей"""

    model_config = ConfigDict(frozen=True)
    id: str
    title: str
    category: str
    year: int = Field(gt=1903, lt=2027)
    serial_number: str = Field(min_length=1, max_length=15)
    # serial_number/SER - уникальный серийный номер
    rule: Rule

    # rule - правило АП-25, указывающие на критичность при поломке

    @field_validator("id", "title", "category", "serial_number")
    @classmethod
    def check_len(cls, value: str) -> str:
        """Проверка на пустые поля и пробелы"""

        if not value.strip():
            raise ValueError("detail cannot be empty")
        return value

    @field_validator("serial_number")
    @classmethod
    def check_ser(cls, value: str) -> str:
        """Проверка SER, чтобы была только латиницы и цифры """

        if not value.isascii() or not value.isalnum():
            raise ValueError(f"serial_number {value} is incorrect")
        return value
