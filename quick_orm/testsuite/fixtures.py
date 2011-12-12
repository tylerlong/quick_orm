# coding=utf-8
"""
    quick_orm.testsuite.fixtures
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    sample data for testing purpose
"""
from toolkit_library.inspector import ModuleInspector 
import quick_orm.testsuite.models

exec(ModuleInspector(quick_orm.testsuite.models).import_all_classes_statement())

users = []
users.append(User(name = 'peter'))
users.append(User(name = 'tyler'))
users.append(User(name = 'simon'))
users.append(User(name = 'jason'))
users.append(User(name = 'justin'))

groups = []
groups.append(Group(name = 'admin', users = [users[0],]))
groups.append(Group(name = 'editor', users = [users[1], users[3], users[4], ]))
groups.append(Group(name = 'user', users = [users[2],]))

blog_entries = []
blog_entries.append(BlogEntry(title = 'title1',  content = 'content1',  user = users[0]))
blog_entries.append(BlogEntry(title = 'title2',  content = 'content2',  user = users[1]))
blog_entries.append(BlogEntry(title = 'title3',  content = 'content3',  user = users[2]))
blog_entries.append(BlogEntry(title = 'title4',  content = 'content4',  user = users[2]))
blog_entries.append(BlogEntry(title = 'title5',  content = 'content5',  user = users[3]))
blog_entries.append(BlogEntry(title = 'title6',  content = 'content6',  user = users[3]))
blog_entries.append(BlogEntry(title = 'title7',  content = 'content7',  user = users[4]))
blog_entries.append(BlogEntry(title = 'title8',  content = 'content8',  user = users[4]))

topics = []
topics.append(Topic(name = 'topic1'))
topics.append(Topic(name = 'topic2'))
topics.append(Topic(name = 'topic3'))
topics.append(Topic(name = 'topic4'))
topics.append(Topic(name = 'topic5'))

questions = []
questions.append(Question(title = 'title1', content = 'content1', topics = [topics[0], topics[1] ]))
questions.append(Question(title = 'title2', content = 'content2', topics = [topics[1], ]))
questions.append(Question(title = 'title3', content = 'content3', topics = [topics[2], ]))
questions.append(Question(title = 'title4', content = 'content4', topics = [topics[3], ]))
questions.append(Question(title = 'title5', content = 'content5', topics = [topics[4], ]))
