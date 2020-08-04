class MyException(Exception):
    def __init__(self, message, detail, code=500):
        self.code = code
        self.message = message
        self.detail = detail

    def get_code(self):
        if self.code is None:
            return 500
        return self.code

    def get_message(self):
        if self.message is None:
            return '操作失败'
        return self.message

    def get_detail(self):
        return self.detail
