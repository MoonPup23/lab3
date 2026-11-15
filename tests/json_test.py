import pytest
from pydantic import ValidationError

from basa.catalog import Command
from basa.exceptions import (
    BrokenFile,
    DuplicateId,
    IncorrectEssence,
    UnsupportedFormatVersion,
)
from basa.models import Detail, Rule
from basa.storage import load_file, save_file
from tests.catalog_test import create_base, create_detail


def test_save_and_load(tmp_path):
    """Тест загрузки и сохранения"""

    db = create_base()
    d = create_detail()
    db.add(d)

    path = tmp_path / "data.json"

    save_file(db, str(path))

    new_db = create_base()
    load_file(new_db, str(path))

    assert new_db.get("A001") == d


def test_broken_file(tmp_path):
    """Проверка на сломанный файл"""

    path = tmp_path / "broken_data.json"
    path.write_text("{broken data json}", encoding="utf-8")

    with pytest.raises(BrokenFile):
        load_file(create_base(), str(path))


def test_incorrect_format(tmp_path):
    """Проверка на правильный формат версии"""

    path = tmp_path / "data.json"
    data = {"format_version": 2, "items": []}

    import json

    path.write_text(json.dumps(data), encoding="utf-8")

    db = Command()

    with pytest.raises(UnsupportedFormatVersion):
        load_file(db, str(path))


def test_correct_essence(tmp_path):
    """Проверка на корректную сущность"""

    d = create_detail()

    assert d.id == "A001"
    assert d.title == "колеса"
    assert d.category == "шасси"
    assert d.year == 1967
    assert d.serial_number == "ASD1234"
    assert d.rule == Rule.MINOR


def test_incorrect_essence():
    """Проверка на некорректную сущность"""

    with pytest.raises(ValidationError):
        Detail(
            id="srtID",
            title="Турбина",
            category="двигатель",
            year=2020,
            serial_number="SER_123",
            rule=Rule.CATASTROPHIC,
        )


def test_duplicate_detail(tmp_path):
    """Проверка на дублированную деталь"""

    d = create_detail().model_dump(mode="json")
    path = tmp_path / "data.json"

    import json

    path.write_text(
        json.dumps({"format_version": 1, "items": [d, d]}), encoding="utf-8"
    )
    with pytest.raises(DuplicateId):
        load_file(create_base(), str(path))


def test_no_edit_file(tmp_path):
    """Проверка на неизменяемость базы данных при одном плохом файле"""

    path = tmp_path / "test.json"
    path.write_text('{"format_version": 1, "items": [{}]}', encoding="utf-8")

    db = Command()
    d1 = create_detail()
    db.add(d1)

    with pytest.raises(IncorrectEssence):
        load_file(db, str(path))

    assert db.get("A001") == d1
