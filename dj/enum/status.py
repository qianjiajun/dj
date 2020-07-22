from enum import Enum


class status_enum(Enum):
    SUCCESS = {"code": 200, "success": True, "message": "成功"}
    ERROR = {"code": 500, "success": False, "message": "失败"}
