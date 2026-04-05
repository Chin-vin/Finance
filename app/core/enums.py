from enum import Enum


class ScopeEnum(str, Enum):
    SELF = "self"
    ALL = "all"


class RoleEnum(str, Enum):
    ADMIN = "admin"
    ANALYST = "analyst"
    VIEWER = "viewer"

