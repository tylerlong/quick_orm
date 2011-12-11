# coding=utf-8
"""
    quick_orm.testsuite.models
    ~~~~~~~~~~~~~~~~~~~~~~~~~~
    database models to be tested against
"""
from quick_orm.core import Database
from sqlalchemy import Column, String, Text, func


class DefaultModel(object):
    created = Column(DateTime, default = func.now(), nullable = False)

metaclass = Database.MetaBuilder(DefaultModel)


class User(object):
    __metaclass__ = metaclass
    username = Column(String(36), nullable = False, unique = True)


@Database.many_to_many(User)
class Group(object):
    __metaclass__ = metaclass
    name = Column(String(36), nullable = False, unique = True)


@Database.foreign_key(User)
class BlogEntry(object):
    __metaclass__ = metaclass
    title = Column(String(64), nullable = False)
    content = Column(Text)
