# -*- coding: utf-8 -*-

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
        self.connect = None

    def __connect__(self):
        self.connect = pymysql.connect(host=self.host,
                                       user=self.user,
                                       password=self.password,
                                       database=self.database,
                                       port=self.port,
                                       charset=self.charset,
                                       cursorclass=self.cursor_class)

    def __close__(self):
        self.connect.close()

    def __execute_void__(self, sql_str):
        self.__connect__()
        cursor = self.connect.cursor()
        cursor.execute(sql_str)
        self.__close__()

    def __execute_object__(self, sql_str):
        self.__connect__()
        cursor = self.connect.cursor()
        cursor.execute(sql_str)
        data = cursor.fetchone()
        self.__close__()
        return data

    def __execute_list__(self, sql_str):
        self.__connect__()
        cursor = self.connect.cursor()
        cursor.execute(sql_str)
        data = cursor.fetchall()
        self.__close__()
        return data

    def __execute_page__(self, sql_str, size):
        self.__connect__()
        cursor = self.connect.cursor()
        cursor.execute(sql_str)
        data = cursor.fetchall(self, size)
        self.__close__()
        return data
