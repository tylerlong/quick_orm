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
users.append(User(username = 'peter'))
users.append(User(username = 'tyler'))
users.append(User(username = 'simon'))
users.append(User(username = 'jason'))
users.append(User(username = 'justin'))

groups = []
groups.append(Group(name = 'admin', users = users[:2]))
groups.append(Group(name = 'editor', users = users[2:3]))
groups.append(Group(name = 'user', users = uses[3:5]))

blog_entries = []
blog_entries.append(BlogEntry(title = 'title1'. content = 'content1', user = users[0]))
blog_entries.append(BlogEntry(title = 'title2'. content = 'content2', user = users[1]))
blog_entries.append(BlogEntry(title = 'title3'. content = 'content3', user = users[2]))
blog_entries.append(BlogEntry(title = 'title4'. content = 'content4', user = users[2]))
blog_entries.append(BlogEntry(title = 'title5'. content = 'content5', user = users[3]))
blog_entries.append(BlogEntry(title = 'title6'. content = 'content6', user = users[3]))
blog_entries.append(BlogEntry(title = 'title7'. content = 'content7', user = users[4]))
blog_entries.append(BlogEntry(title = 'title8'. content = 'content8', user = users[4]))
