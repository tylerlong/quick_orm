from quick_orm.core import Database
from sqlalchemy import Column, String

__metaclass__ = Database.DefaultMeta

class User:
    name = Column(String(30))

Database.register()

if __name__ == '__main__':
    db = Database('sqlite://')
    db.create_tables()
    
    user = User(name = 'Hello World')
    db.session.add_then_commit(user)
    
    user = db.session.query(User).get(1)
    print 'My name is', user.name
