import base64
import hmac
import json
import time

claims_key = 'qjj_love_yry'


class token:

    def __init__(self, string, secret, expire=60, claims: dict = None):
        if claims is None:
            claims = {}
        self.string = string
        self.secret = secret
        self.expire = expire
        self.token = None
        self.claims = claims
        self.key = None

    def add_claim(self, key, value):
        self.claims[key] = value
        return self

    # def generate_token(self):
    #     end_str = str(time.time() + self.expire)
    #     ts_byte = end_str.encode("utf-8")
    #     sha1_str = hmac.new(self.key.encode("utf-8"), ts_byte, 'sha1').hexdigest()
    #     access_token = end_str + ':' + sha1_str
    #     self.token = base64.urlsafe_b64encode(access_token.encode("utf-8"))
    #     return self.token

    def generate_token(self):
        self.key = hmac.new(self.secret.encode("utf-8"), self.string.encode("utf-8"), 'sha1').hexdigest()
        self.claims['timestamp'] = time.time()
        claims_str = json.dumps(self.claims)
        print(claims_str)
        ts_byte = claims_str.encode("utf-8")
        sha1_str = hmac.new(self.key.encode("utf-8"), ts_byte, 'sha1').hexdigest()
        access_token = claims_str + ':' + sha1_str
        self.token = base64.urlsafe_b64encode(access_token.encode("utf-8")).decode("utf-8")
        return self

    # def certify_token(self, access_token):
    #     token_str = base64.urlsafe_b64decode(access_token).decode('utf-8')
    #     token_list = token_str.split(':')
    #     if len(token_list) != 2:
    #         return False
    #     end_str = token_list[0]
    #     if float(end_str) < time.time():
    #         return False
    #     known_str = token_list[1]
    #     sha1 = hmac.new(self.key.encode("utf-8"), end_str.encode('utf-8'), 'sha1')
    #     calc_str = sha1.hexdigest()
    #     if calc_str != known_str:
    #         return False
    #     else:
    #         return True

    def certify_token(self, access_token):
        token_str = base64.urlsafe_b64decode(access_token.encode("utf-8")).decode('utf-8')
        token_list = token_str.split(':')
        if len(token_list) != 2:
            return None
        claims_str = token_list[0]
        print(claims_str)
        if claims_str is not None:
            self.claims = json.loads(claims_str)
        print(self.claims)
        known_str = token_list[1]
        sha1 = hmac.new(self.key.encode("utf-8"), claims_str.encode('utf-8'), 'sha1')
        calc_str = sha1.hexdigest()
        if calc_str != known_str:
            return None
        else:
            return self
