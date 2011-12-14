# coding=utf-8
"""
    manage
    ~~~~~~
    Provides useful commands to manage the project
"""
import sys, subprocess
from toolkit_library.inspector import ModuleInspector, PackageInspector
from toolkit_library.input_util import InputUtil
from quick_orm import examples

def run_examples():
    """Run all of the examples"""
    # automatically install the newest code before testing
    subprocess.call([sys.executable, 'setup.py', 'install'])
    
    # call each example file and print the result
    for module in PackageInspector(examples).get_all_modules():    
        print '****** {0} ******'.format(module)
        subprocess.call([sys.executable, 'quick_orm/examples/{0}.py'.format(module)])
        print
    

def run_tests():
    """Run unit tests"""
    from quick_orm.testsuite import run_testsuite
    db_name = InputUtil.get_input('database', default = 'sqlite', pattern = '(?:mysql|sqlite|postgresql)')
    run_testsuite(db_name)


def run_test():
    """Run a simple test"""
    from quick_orm.core import Database
    from sqlalchemy import Column, Integer, ForeignKey, String
    from sqlalchemy.ext.declarative import declarative_base, declared_attr, DeclarativeMeta
    class Person(Database.BaseModel):
        __tablename__ = 'person'
        id = Column(Integer, primary_key=True)
        real_type = Column('real_type', String(50))
        __mapper_args__ = {'polymorphic_on': real_type}

    class Engineer(Person):
        __tablename__ = 'engineer'
        __mapper_args__ = {'polymorphic_identity': 'engineer'}
        id = Column(Integer, ForeignKey('person.id'), primary_key=True)
        primary_language = Column(String(50))

    
    db = Database('sqlite:///quick_orm/testsuite/test.db')
    db.drop_tables()
    db.create_tables()

    db.session.add_then_commit(Engineer(primary_language='English'))
    db.session.add_then_commit(Engineer(primary_language='Chinese'))


def run_test2():
    """temp test"""
    from quick_orm.core import Database
    from sqlalchemy import Column, String

    class Person(object):
        __metaclass__ = Database.DefaultMeta

    class Engineer(Person):
        __metaclass__ = Database.DefaultMeta
        primary_language = Column(String(50))

    
    db = Database('sqlite:///quick_orm/testsuite/test.db')
    db.drop_tables()
    db.create_tables()

    db.session.add_then_commit(Engineer(primary_language='English'))
    db.session.add_then_commit(Engineer(primary_language='Chinese'))




if __name__ == '__main__':
    inspector = ModuleInspector(sys.modules[__name__])
    inspector.invoke(*sys.argv[1:])
