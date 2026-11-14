import json
from pydantic import ValidationError

from basa.catalog import Command
from basa.exceptions import (
    UnsupportedFormatVersion,
    DuplicateId,
    BrokenFile, IncorrectEssence
)
from basa.models import Detail


def save_file(database: Command, path: str) -> None:
    items = [
        detail.model_dump(mode="json")
        for detail in database.data.values()
    ]
    data = {
        "format_version": 1,
        "items": items
    }
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=3)


def load_file(database: Command, path: str) -> None:
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
            if not isinstance(data, dict):
                raise BrokenFile(f"incorrect data:{data}")

            if "format_version" not in data or "items" not in data:
                raise BrokenFile(f"incorrect format: {data}")

    except json.JSONDecodeError:
        raise BrokenFile(f"JSON file is broken")

    data_control = {}

    if data["format_version"] != 1:
        raise UnsupportedFormatVersion(f"format version data: {data} is unsupported")


    else:
        items = data["items"]
        if not isinstance(items, list):
            raise BrokenFile(f"incorrect data:{items}")


        for item in items:
            try:
                detail = Detail.model_validate(item)
            except ValidationError as error:
                raise IncorrectEssence(f"Incorrect detail") from error

            if detail.id in data_control:
                raise DuplicateId(f"this id:{detail.id} already in database")

            data_control[detail.id] = detail

        database.data = data_control
