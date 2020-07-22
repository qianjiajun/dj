import json


class resultSet(object):

    def __init__(self, code=200, success=True, message='', detail='', data=None):
        self.res = {
            'code': code,
            'success': success,
            'message': message,
            'detail': detail,
            'data': data
        }

    def set_status(self, status, detail, data):
        self.res['code'] = status.code
        self.res['success'] = status.success
        self.res['message'] = status.message
        self.res['detail'] = detail
        self.res['data'] = data
        return self

    def set_code(self, code):
        self.res['code'] = code
        return self

    def set_success(self, success):
        self.res['success'] = success
        return self

    def set_message(self, message):
        self.res['message'] = message
        return self

    def set_detail(self, detail):
        self.res['detail'] = detail
        return self

    def set_data(self, data):
        self.res['data'] = data
        return self

    def success(self, message, detail, data):
        self.res['code'] = 200
        self.res['success'] = True
        self.res['message'] = message
        self.res['detail'] = detail
        self.res['data'] = data
        return self

    def fail(self, message, detail, data):
        self.res['code'] = 500
        self.res['success'] = False
        self.res['message'] = message
        self.res['detail'] = detail
        self.res['data'] = data
        return self

    def to_string(self):
        return json.dumps(self.res)
