from _collections_abc import Iterator

from basa.exceptions import DuplicateId, ObjectNotFound
from basa.models import Detail


class Command:
    """Каталог деталей"""

    def __init__(self):

        self.data: dict = {}

    def add(self, item: Detail) -> None:
        if item.id in self.data:
            raise DuplicateId(f"this detail: {item} in database")
        self.data[item.id] = item

    def get(self, item_id: str) -> Detail:
        if item_id not in self.data:
            raise ObjectNotFound(f"{item_id} not found in file")
        return self.data[item_id]

    def remove(self, item_id: str) -> None:
        if item_id not in self.data:
            raise ObjectNotFound(f"{item_id} not found in file")
        del self.data[item_id]

    def find_by_category(self, category: str) -> list[Detail]:
        category_name = []

        for obj in self.data.values():
            if obj.category.lower() == category.lower():
                category_name.append(obj)

        return category_name

    def find_by_name(self, query: str) -> list[Detail]:
        name_list = []

        for name in self.data.values():
            if query.lower() in name.title.lower():
                name_list.append(name)

        return name_list

    def __len__(self) -> int:
        return len(self.data)

    def __iter__(self) -> Iterator[Detail]:
        """Итерация деталей выполняется по добавлению в файл"""
        return iter(self.data.values())

    def __contains__(self, item_id: str) -> bool:
        return item_id in self.data
