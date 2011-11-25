# encoding=utf-8
"""
    quick_orm.column_types
    ~~~~~~~~~~~~~~~~~~~~~~
    More database column types
"""
import json
from sqlalchemy.types import TypeDecorator, String

class JsonType(TypeDecorator):
    '''Dumps simple python data structures to json format and stores them as string
    Convert the data back to original python data structures when read.
    '''

    impl = String

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value
