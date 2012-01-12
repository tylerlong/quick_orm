from quick_orm.core import Database
from sqlalchemy import Column, String, DateTime, func

class DefaultModel(object):
    name = Column(String(70))
    created = Column(DateTime, default = func.now(), nullable = False)

metaclass = Database.MetaBuilder(DefaultModel)

class User(object):
    __metaclass__ = metaclass

class Group(object):
    __metaclass__ = metaclass

Database.register()

if __name__ == '__main__':
    db = Database('sqlite://')
    db.create_tables()
    user = User(name = 'tylerlong')
    db.session.add(user)
    group = Group(name = 'python')
    db.session.add_then_commit(group)

    print user.name, user.created
    print group.name, group.created
