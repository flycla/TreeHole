import os
import sqlite3
from time import time

import log
from config import *
from errors import *


def connect() -> sqlite3.Connection:
    """
    Connect to the database from config file.
    If the database doesn't exist, it will call `init()` to create it.
    :return: sqlite3.Connection
    """
    if not os.path.isfile(DATABASE):
        connection = init()
    else:
        connection = sqlite3.connect(DATABASE, check_same_thread=False)
    return connection


def init() -> sqlite3.Connection:
    """
    Initialize the sqlite database by the sql file from config file.
    :rtype: sqlite3.Connection
    """
    try:
        with open(DATABASE_INIT) as reader:
            sql = reader.read()
            connection = sqlite3.connect(DATABASE, check_same_thread=False)
            connection.executescript(sql)
            return connection
    except FileNotFoundError:
        log.error(DatabaseInitializeError())
        exit(1)


conn = connect()


class Records:
    def __init__(self, number, start=None):
        cur = conn.cursor()
        if start:
            cur.execute('SELECT * FROM Records WHERE timestamp > ? ORDER BY timestamp DESC LIMIT ?',
                        (start, number))
        else:
            cur.execute('SELECT * FROM Records ORDER BY timestamp DESC LIMIT ?',
                        (number, ))
        self.__records = cur.fetchall()
        self.__records_dict = list(map(Records.to_dict, self.__records))
        self.__length = len(self.__records)

    def __len__(self):
        return self.__length

    @staticmethod
    def to_dict(record):
        record_dict = {
            'timestamp': record[0],
            'nickname': record[1],
            'content': record[2],
            'remark': record[3]
        }
        return record_dict

    @staticmethod
    def add_record(record):
        cur = conn.cursor()
        record = (int(time()*1000), ) + record
        try:
            cur.execute('INSERT INTO Records (timestamp, nickname, content, remark) VALUES (?, ?, ?, ?)', record)
            conn.commit()
            return Records.to_dict(record)
        except sqlite3.Error:
            conn.rollback()
            return {
                'error': 'Add Record Fail'
            }

    def __convert_records2dict(self):
        self.__records_dict = map(Records.to_dict, self.__records)

    def get_records(self):
        return self.__records

    def get_records_dict(self):
        return self.__records_dict
