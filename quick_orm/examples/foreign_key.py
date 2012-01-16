from quick_orm.core import Database
from sqlalchemy import Column, String, Text

__metaclass__ = Database.DefaultMeta

class Question:
    title = Column(String(70))
    content = Column(Text)

@Database.foreign_key(Question)
class Answer:
    content = Column(Text)

Database.register()

if __name__ == '__main__':
    db = Database('sqlite://')
    db.create_tables()
    
    question = Question(title = 'What is Quick ORM ?', content = 'What is Quick ORM ?')
    answer = Answer(question = question, content = 'Quick ORM is a python ORM which enables you to get started in less than a minute!')
    db.session.add_then_commit(answer)
    
    question = db.session.query(Question).get(1)
    print 'The question is:', question.title
    print 'The answer is:', question.answers.first().content
