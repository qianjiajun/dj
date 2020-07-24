import cx_Oracle
import pymysql


class ms_mysql:

    def __init__(self, host, user, password, database, port):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.charset = "utf8"
        self.cursor_class = pymysql.cursors.DictCursor
        self.conn = None

    def connect(self):
        self.conn = pymysql.connect(host=self.host,
                                    user=self.user,
                                    password=self.password,
                                    database=self.database,
                                    port=self.port,
                                    charset=self.charset,
                                    cursorclass=self.cursor_class)

    def close(self):
        self.conn.close()

    def execute_void(self, sql_str):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(sql_str)
        self.close()

    def execute_object(self, sql_str):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(sql_str)
        data = cursor.fetchone()
        self.close()
        return data

    def execute_list(self, sql_str):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(sql_str)
        data = cursor.fetchall()
        self.close()
        return data

    def execute_page(self, sql_str, size):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(sql_str)
        data = cursor.fetchall(self, size)
        self.close()
        return data


def rows_to_dict_list(cursor, rows):
    columns = [i[0] for i in cursor.description]
    return [dict(zip(columns, row)) for row in rows]


def row_to_dict(cursor, row):
    columns = [i[0] for i in cursor.description]
    return dict(zip(columns, row))


class ms_oracle:

    def __init__(self, username, password, url):
        self.username = username
        self.password = password
        self.url = url
        self.conn = None

    def connect(self):
        self.conn = cx_Oracle.connect(self.username, self.password, self.url)

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

    def execute_void(self, sql_str):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(sql_str)
        cursor.close()
        self.commit()
        self.close()

    def execute_object(self, sql_str):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(sql_str)
        row = cursor.fetchone()
        if cursor.rowcount == 0:
            return None
        if cursor.rowcount >= 2:
            raise Exception("单行返回值返回多行数据", 1)
        data = row_to_dict(cursor, row)
        cursor.close()
        self.commit()
        self.close()
        return data

    def execute_list(self, sql_str):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(sql_str)
        rows = cursor.fetchall()
        count = cursor.rowcount
        if count == 0:
            return None
        data = rows_to_dict_list(cursor, rows)
        cursor.close()
        self.close()
        return data, count

    def execute_page(self, sql_str, size):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(sql_str)
        data = cursor.fetchall(self, size)
        cursor.close()
        self.close()
        return data
