from enum import Enum


class StatusEnum(Enum):
    SUCCESS = {"code": 200, "success": True, "message": "成功"}
    ERROR = {"code": 500, "success": False, "message": "失败"}
