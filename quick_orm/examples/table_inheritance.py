from quick_orm.core import Database
from sqlalchemy import Column, String, Text

class User(object):
    __metaclass__ = Database.DefaultMeta
    name = Column(String(70))

@Database.foreign_key(User)
class Post(object):
    __metaclass__ = Database.DefaultMeta
    content = Column(Text)

class Question(Post):
    title = Column(String(70))    

@Database.foreign_key(Question)
class Answer(Post):
    pass

@Database.foreign_key(Post)
class Comment(Post):
    pass

Database.register()

if __name__ == '__main__':
    db = Database('sqlite://')
    db.create_tables()

    user1 = User(name = 'Tyler Long')
    user2 = User(name = 'Peter Lau')
    
    question = Question(user = user1, title = 'What is Quick ORM ?', content = 'What is Quick ORM ?')
    answer = Answer(user = user1, question = question, 
        content = 'Quick ORM is a python ORM which enables you to get started in less than a minute!')
    comment1 = Comment(user = user2, content = 'good question', post = question)
    comment2 = Comment(user = user2, content = 'nice answer', post = answer)
    db.session.add_all_then_commit([question, answer, comment1, comment2])

    question = db.session.query(Question).get(1)
    print 'new comment on question:', question.comments.first().content
    print 'new comment on answer:', question.answers.first().comments.first().content

    # Could the last two lines work as you expected? Try it yourself!
    user = db.session.query(User).filter_by(name = 'Peter Lau').one()
    print 'Peter Lau has posted {0} comments'.format(user.comments.count())
