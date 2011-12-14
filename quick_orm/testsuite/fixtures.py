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
blog_entries.append(BlogEntry(title = 'blog_entry_title_1',  content = 'blog_entry_content_1',  user = users[0]))
blog_entries.append(BlogEntry(title = 'blog_entry_title_2',  content = 'blog_entry_content_2',  user = users[1]))
blog_entries.append(BlogEntry(title = 'blog_entry_title_3',  content = 'blog_entry_content_3',  user = users[2]))
blog_entries.append(BlogEntry(title = 'blog_entry_title_4',  content = 'blog_entry_content_4',  user = users[2]))
blog_entries.append(BlogEntry(title = 'blog_entry_title_5',  content = 'blog_entry_content_5',  user = users[3]))
blog_entries.append(BlogEntry(title = 'blog_entry_title_6',  content = 'blog_entry_content_6',  user = users[3]))
blog_entries.append(BlogEntry(title = 'blog_entry_title_7',  content = 'blog_entry_content_7',  user = users[4]))
blog_entries.append(BlogEntry(title = 'blog_entry_title_8',  content = 'blog_entry_content_8',  user = users[4]))

topics = []
topics.append(Topic(name = 'topic_name_1'))
topics.append(Topic(name = 'topic_name_2'))
topics.append(Topic(name = 'topic_name_3'))
topics.append(Topic(name = 'topic_name_4'))
topics.append(Topic(name = 'topic_name_5'))

questions = []
questions.append(Question(title = 'question_title_1', content = 'question_content_1', topics = [topics[0], topics[1], ], user = users[4]))
questions.append(Question(title = 'question_title_2', content = 'question_content_2', topics = [topics[1], ], user = users[4]))
questions.append(Question(title = 'question_title_3', content = 'question_content_3', topics = [topics[2], ], user = users[4]))
questions.append(Question(title = 'question_title_4', content = 'question_content_4', topics = [topics[3], ], user = users[4]))
questions.append(Question(title = 'question_title_5', content = 'question_content_5', topics = [topics[4], ], user = users[4]))


answers = []
answers.append(Answer(content = 'answer_content_1', user = users[0]))
answers.append(Answer(content = 'answer_content_2', user = users[0]))
answers.append(Answer(content = 'answer_content_3', user = users[0]))
answers.append(Answer(content = 'answer_content_4', user = users[1]))
answers.append(Answer(content = 'answer_content_5', user = users[2]))
