# coding=utf-8
"""
    quick_orm.testsuite
    ~~~~~~~~~~~~~~~~~~~
    unit tests for quick_orm project
"""
import unittest
from quick_orm.core import Database

db = None
db_strs = { 
        'postgresql': 'postgresql://postgres:123456@localhost/quick_orm', 
        'sqlite': 'sqlite:///quick_orm/testsuite/quick_orm.db', 
        'mysql': 'mysql://root:123456@localhost/quick_orm?charset=utf8',
}

def run_testsuite(db_name):
    import quick_orm.testsuite.fixtures as fixtures

    global db
    db_str = db_strs[db_name]
    db = Database(db_str)
    db.drop_tables()
    db.create_tables()
    db.load_data(fixtures)

    from quick_orm.testsuite.core import CoreTestCase
    test_suite = unittest.TestSuite()
    test_suite.addTest(unittest.makeSuite(CoreTestCase))
    
    unittest.TextTestRunner(verbosity=1).run(test_suite)
