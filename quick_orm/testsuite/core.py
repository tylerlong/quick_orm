# coding=utf-8
"""
    quick_orm.testsuite.core
    ~~~~~~~~~~~~~~~~~~~~~~~~
    test the core of quick_orm
"""
import unittest
from toolkit_library.inspector import ModuleInspector
import quick_orm.testsuite.models as models
from quick_orm.testsuite import db

exec(ModuleInspector(models).import_all_classes_statement())

class CoreTestCase(unittest.TestCase):
    """The default test case"""

    def tearDown(self):
        db.session.remove()

    def test_foreign_key(self):
        """Test foreign_key relationship"""
        user = db.session.query(User).filter_by(name = 'simon').first()
        assert user
        assert user.blog_entries.count() > 0
        assert user.blog_entries.first().user.name == 'simon'

    def test_many_to_many(self):
        """Test many_to_many relationship"""
        user = db.session.query(User).filter_by(name = 'simon').first()
        assert user
        assert user.groups.count() > 0
        assert user.groups.first().users.count() > 0
        assert any(u.name == 'simon' for u in user.groups.first().users)

    def test_foreign_key_cascade(self):
        """Test cascade in a foreign_key relationship.
        When record from the one side gets deleted, 
        records from the many side are deleted automatically.
        Make sure no ignorant records are deleted.
        """
        user_query = db.session.query(User)
        user_count = user_query.count()
        blog_query = db.session.query(BlogEntry)
        blog_count = blog_query.count()
        user = db.session.query(User).filter_by(name = 'peter').first()
        assert user
        user_blog_count = user.blog_entries.count()
        blog_entry = user.blog_entries.first()
        assert blog_entry
        db.session.delete_then_commit(user)
        blog_entry = db.session.query(BlogEntry).get(blog_entry.id)
        assert not blog_entry
        assert user_count - 1 == user_query.count()
        assert blog_count - user_blog_count == blog_query.count()

    def test_many_to_many_cascade(self):
        """Test cascade in a many_to_many relationship.
        when record from either side gets deleted, 
        records from the middle table are deleted automatically, 
        records from the other side retain.
        make sure no ignorant records are deleted.
        """
        user_query = db.session.query(User)
        user_count = user_query.count()
        group_query = db.session.query(Group)
        group_count = group_query.count()
        middle_query_str = 'select count(*) from user_group'
        middle_count = db.engine.execute(middle_query_str).scalar()
        
        user = db.session.query(User).filter_by(name = 'tyler').first()
        assert user
        user_middle_count = db.engine.execute('select count(*) from user_group where user_id={0}'.format(user.id)).scalar()
        group =db.session.query(Group).filter_by(name = 'editor').first()
        assert group
        query_str = 'select count(*) from user_group where user_id={0} and group_id={1}'.format(user.id, group.id)
        assert db.engine.execute(query_str).scalar() == 1
        db.session.delete_then_commit(user)
        assert db.engine.execute(query_str).scalar() == 0
        group = db.session.query(Group).filter_by(name = 'editor').first()
        assert group

        assert user_count - 1 == user_query.count()
        assert group_count == group_query.count()
        assert middle_count - user_middle_count == db.engine.execute(middle_query_str).scalar()

