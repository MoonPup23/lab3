import pytest
from pydantic import ValidationError

from basa.catalog import Command
from basa.exceptions import (
    DuplicateId,
    ObjectNotFound,
)
from basa.models import Detail, Rule


def create_detail(id="A001", title="колеса"):
    """Создание детали"""

    return Detail(
        id=id,
        title=title,
        category="шасси",
        year=1967,
        serial_number="ASD1234",
        rule=Rule.MINOR,
    )


def create_base():
    """Создание базы данных"""

    return Command()


def test_correct_detail():
    """Создание детали с id A001"""

    detail = create_detail()
    assert detail.id == "A001"


def test_incorrect_detail():
    """Создание детали без id"""

    with pytest.raises(ValidationError):
        Detail(
            id="",
            title="колеса",
            category="шасси",
            year=1967,
            serial_number="ASD1234",
            rule=Rule.MINOR,
        )


def test_command_add_get():
    """Проверка на добавление детали и получении ее же через get"""

    db = create_base()
    d = create_detail()

    db.add(d)

    assert db.get("A001") == d


def test_duplicate_id():
    """Ошибка на дубликат в id"""

    db = create_base()
    d = create_detail()

    db.add(d)

    with pytest.raises(DuplicateId):
        db.add(d)


def test_remove():
    """Удаление объекта из базы данных"""

    db = create_base()
    d = create_detail()

    db.add(d)

    db.remove("A001")

    assert "A001" not in db


def test_remove_void():
    """Удаление несуществующего"""

    db = create_base()

    with pytest.raises(ObjectNotFound):
        db.remove("void")


def test_get_void():
    """Получение несуществующего"""

    db = create_base()

    with pytest.raises(ObjectNotFound):
        db.get("void")


def test_find_category():
    """Поиск по категории"""

    db = create_base()
    d = create_detail()

    db.add(d)

    assert db.find_by_category("шасси") == [d]


def test_find_name():
    """Поиск по имени"""

    db = create_base()
    d = create_detail()

    db.add(d)

    assert db.find_by_name("КоЛес") == [d]


def test_len():
    """Длина базы данных"""

    db = create_base()
    d = create_detail()

    db.add(d)

    assert db.__len__() == len(db)


def test_contains():
    db = create_base()
    d = create_detail()

    db.add(d)

    assert "A001" in db
    assert "ID1337" not in db


def test_iter():
    """Тест итерации"""

    db = create_base()
    d1 = create_detail("A001", "колесо")
    d2 = create_detail("A002", "амортизатор")

    db.add(d1)
    db.add(d2)

    assert list(db) == [d1, d2]
