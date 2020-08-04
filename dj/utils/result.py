import json


class Result(object):

    def __init__(self, code=200, success=True, message='', detail='', data: object = None, token=None, extra=None):
        self.res: dict = {
            'code': code,
            'success': success,
            'message': message,
            'detail': detail,
            'data': data,
            'token': token,
            'extra': extra
        }

    def set_status(self, status, detail, data: object = None):
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

    def set_data(self, data: object = None):
        self.res['data'] = data
        return self

    def set_token(self, token):
        self.res['token'] = token
        return self

    def set_extra(self, extra):
        self.res['extra'] = extra
        return self

    def get(self, key):
        if self.res is None:
            return None
        if key in self.res.keys():
            return self.res[key]
        return None

    def success(self, message='', detail='', data: object = None):
        self.res['code'] = 200
        self.res['success'] = True
        self.res['message'] = message
        self.res['detail'] = detail
        self.res['data'] = data
        return self

    def fail(self, message='', detail='', data: object = None):
        self.res['code'] = 500
        self.res['success'] = False
        self.res['message'] = message
        self.res['detail'] = detail
        self.res['data'] = data
        return self

    def to_string(self, ensure_ascii: bool = False):
        return json.dumps(self.res, ensure_ascii=ensure_ascii)
