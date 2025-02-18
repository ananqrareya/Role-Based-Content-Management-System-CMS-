from enum import Enum

class RoleEnum(str,Enum):
    ADMIN = "Admin"
    EDITOR= "Editor"
    AUTHOR = "Author"
    READER = "Reader"