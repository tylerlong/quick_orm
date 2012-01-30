from quick_orm.core import Database
from sqlalchemy import Column, String, Text

__metaclass__ = Database.DefaultMeta

class User:
    name = Column(String(70))

@Database.foreign_key(User)
class Post:
    content = Column(Text)

class Question(Post):
    title = Column(String(70))    

@Database.foreign_key(Question)
class Answer(Post):
    pass

@Database.foreign_key(Post)
class Comment(Post):
    pass

@Database.many_to_many(Post)
class Tag:
    name = Column(String(70))
    
Database.register()

if __name__ == '__main__':
    db = Database('sqlite://')
    db.create_tables()

    user1 = User(name = 'Tyler Long')
    user2 = User(name = 'Peter Lau')
    
    tag1 = Tag(name = 'quick_orm')
    tag2 = Tag(name = 'nice')
    
    question = Question(user = user1, title = 'What is quick_orm ?', content = 'What is quick_orm ?', tags = [tag1, ])
    question2 = Question(user = user1, title = 'Have you tried quick_orm ?', content = 'Have you tried quick_orm ?', tags = [tag1, ])

    answer = Answer(user = user1, question = question, tags = [tag1, ],
        content = 'quick_orm is a python ORM which enables you to get started in less than a minute!')
    
    comment1 = Comment(user = user2, content = 'good question', post = question)
    comment2 = Comment(user = user2, content = 'nice answer', post = answer, tags = [tag2, ])

    db.session.add_all_then_commit([question, question2, answer, comment1, comment2, tag1, tag2, ])

    question = db.session.query(Question).get(1)
    print 'tags for question "{0}": "{1}"'.format(question.title, ', '.join(tag.name for tag in question.tags))
    print 'new comment on question:', question.comments.first().content
    print 'new comment on answer:', question.answers.first().comments.first().content

    user = db.session.query(User).filter_by(name = 'Peter Lau').one()
    print 'Peter Lau has posted {0} comments'.format(user.comments.count())

    tag = db.session.query(Tag).filter_by(name = 'quick_orm').first()
    print '{0} questions are tagged "quick_orm"'.format(tag.questions.count())
