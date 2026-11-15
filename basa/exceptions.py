class CatalogError(Exception):
    pass


class IncorrectEssence(CatalogError):
    pass


class DuplicateId(CatalogError):
    pass


class UnsupportedFormatVersion(CatalogError):
    pass


class BrokenFile(CatalogError):
    pass


class ObjectNotFound(CatalogError):
    pass
