# coding=utf-8
"""
    quick_orm.testsuite.models
    ~~~~~~~~~~~~~~~~~~~~~~~~~~
    database models to be tested against
"""
from quick_orm.core import Database
from sqlalchemy import Column, String, Text, DateTime, func


class DefaultModel(object):
    created = Column(DateTime, default = func.now(), nullable = False)

metaclass = Database.MetaBuilder(DefaultModel)


@Database.many_to_many('Group')
class User(object):
    __metaclass__ = metaclass
    name = Column(String(36), nullable = False, unique = True)


class Group(object):
    __metaclass__ = metaclass
    name = Column(String(36), nullable = False, unique = True)


@Database.foreign_key(User, backref_name = 'blog_entries')
class BlogEntry(object):
    __metaclass__ = metaclass
    title = Column(String(64), nullable = False)
    content = Column(Text)
