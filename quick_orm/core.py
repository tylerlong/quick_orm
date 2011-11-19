# coding=utf-8
"""
    quick_orm.core
    ~~~~~~~~~~~~~~
    Core of Quick ORM
"""
import inspect
from types import MethodType
from toolkit_library.string_util import StringUtil
from sqlalchemy import create_engine, Column, Integer, ForeignKey, String
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from sqlalchemy.schema import Table
from sqlalchemy.ext.declarative import declarative_base, declared_attr, DeclarativeMeta


def model_name_to_table_name(model_name):
    """Convert model name to table name"""
    return StringUtil.camelcase_to_underscore(model_name)


class Database(object):
    """Represent a connection to a specific database"""

    # BaseModel is a class variable, because it has nothing to do with specific instances of this class
    BaseModel = declarative_base() 

    def __init__(self, connection_string):
        """Initiate a database engine which is very low level, and a database session which deals with orm."""
        # Solve an issue with mysql character encoding(maybe it's a bug of MySQLdb)
        # Refer to http://plone.293351.n2.nabble.com/Troubles-with-encoding-SQLAlchemy-MySQLdb-or-mysql-configuration-pb-td4827540.html
        if 'mysql:' in connection_string and 'charset=' not in connection_string:
            raise ValueError("""No charset was specified for a mysql connection string. 
Please specify something like '?charset=utf8' explicitly.""")

        # The engine can do everything you can do in a database command console. 
        self.engine = create_engine(connection_string, convert_unicode = True, encoding = 'utf-8')

        # If you want to deal with orm, you need session 
        self.session = scoped_session(sessionmaker(autocommit = False, autoflush = False, bind = self.engine))

        def add_then_commit(session, obj):
            session.add(obj)
            session.commit()        
        self.session.add_then_commit = MethodType(add_then_commit, self.session)

        def add_all_then_commit(session, items):
            session.add_all(items)
            session.commit()        
        self.session.add_all_then_commit = MethodType(add_all_then_commit, self.session)

    
    def create_tables(self):
        """Create all tables"""
        Database.BaseModel.metadata.create_all(bind = self.engine)

   
    def drop_tables(self):
        """Drop all tables"""
        Database.BaseModel.metadata.drop_all(bind = self.engine)

    
    def load_data(self, data):
        """Load data into database from a module or an iterable of items 
        All items must be derived from Database.BaseModel, otherwise will be ignored.
        If the data paramter is a module, will try to load data from variables ending with 's' in that module.
        """
        if not data:
            raise ValueError('data parameter should not be None or empty')
        #Iterable of items
        if hasattr(data, '__iter__') and all(isinstance(item, Database.BaseModel) for item in data):
            self.session.add_all(data)
            self.session.commit()
        #Module
        elif inspect.ismodule(data):
            for items in (getattr(data, attr) for attr in dir(data) if attr.endswith('s')):
                self.load_data(items)


    @staticmethod
    def foreign_key(ref_model, ref_name = None, backref_name = None, one_to_one = False):
        """"Class decorator, add a foreign key to a SQLAlchemy model.
        Parameters:
        ref_model is the destination model, in a one-to-many relationship, it is the "one" side.
        ref_name is the user-friendly name of destination model(if omitted, destintion table name will be used instead).
        backref_name is the name used to back ref the "many" side.
        one_to_one: is this foreign_key for a one-to-one relationship?
        """
        if isinstance(ref_model, str):
            ref_model_name = ref_model
        else:
            ref_model_name = ref_model.__name__
        ref_table_name = model_name_to_table_name(ref_model_name)
        ref_name = ref_name or ref_table_name
        foreign_key = '{0}_id'.format(ref_name)        
        def ref_table(cls):
            model_name = cls.__name__
            table_name = model_name_to_table_name(model_name)
            setattr(cls, foreign_key, Column(Integer, ForeignKey('{0}.id'.format(ref_table_name))))
            # Assign to backref_name will change it to a local variable which we don't want to, so we have to create a new variable.
            # reference: http://docs.python.org/tutorial/classes.html#python-scopes-and-namespaces
            my_backref_name = backref_name or (table_name if one_to_one else '{0}s'.format(table_name))
            backref_options = dict(uselist = False) if one_to_one else dict(lazy = 'dynamic')
            setattr(cls, ref_name, relationship(ref_model_name, 
                primaryjoin = '{0}.{1} == {2}.id'.format(model_name, foreign_key, ref_model_name), 
                backref = backref(my_backref_name, **backref_options), remote_side = '{0}.id'.format(ref_model_name)))
            return cls
        return ref_table


    @staticmethod
    def one_to_one(ref_model, ref_name = None, backref_name = None):
        """Add a one-to-one relationship between two models.
        This method is a shortcut to the method Database.foreign_key(ref_model, ref_name, backref_name, True)
        """
        return Database.foreign_key(ref_model, ref_name, backref_name, True)


    @staticmethod
    def many_to_many(ref_model, ref_name = None, backref_name = None, middle_table_name = None):
        """Class Decorator, add a many-to-many relationship between two SQLAlchemy models.
        Parameters:
        ref_table_name is the name of the destination table, it is NOT the one decorated by this method.
        ref_name is how this model reference the destination models.
        backref_name is how the destination model reference this model.
        middle_table_name is the middle table name of this many-to-many relationship.
        """
        if isinstance(ref_model, str):
            ref_model_name = ref_model
        else:
            ref_model_name = ref_model.__name__
        ref_table_name = model_name_to_table_name(ref_model_name)
        ref_name = ref_name or '{0}s'.format(ref_table_name)
        def ref_table(cls):
            table_name = model_name_to_table_name(cls.__name__)
            my_middle_table_name = middle_table_name or '{0}_{1}'.format(table_name, ref_table_name)

            if table_name == ref_table_name:
                left_column_name = 'left_id'
                right_column_name = 'right_id'                
            else:
                left_column_name = '{0}_id'.format(table_name)
                right_column_name = '{0}_id'.format(ref_table_name)           

            middle_table = Table(
                my_middle_table_name, Database.BaseModel.metadata,
                Column(left_column_name, Integer, ForeignKey('{0}.id'.format(table_name)), primary_key = True),
                Column(right_column_name, Integer, ForeignKey('{0}.id'.format(ref_table_name)), primary_key = True),
            )

            my_backref_name = backref_name or '{0}s'.format(table_name)
            parameters = dict(secondary = middle_table, lazy = 'dynamic', backref = backref(my_backref_name, lazy = 'dynamic'))
            if table_name == ref_table_name:             
                parameters['primaryjoin'] = cls.id == middle_table.c.left_id
                parameters['secondaryjoin'] = cls.id == middle_table.c.right_id

            setattr(cls, ref_name, relationship(ref_model_name, **parameters))

            return cls
        return ref_table


    class BaseMeta(DeclarativeMeta):
        """metaclass for all model classes, let model class inherit Database.BaseModel and handle table inheritance.
        All other model metaclasses are either directly or indirectly derived from this class.
        """
        def __new__(cls, name, bases, attrs):
            # add Database.BaseModel as parent class
            bases = list(bases)
            # no need to inherit object because it's going to inherit other classes which already inherited object
            if object in bases: 
                bases.remove(object)
            bases.append(Database.BaseModel)
            seen = set()
            bases = tuple(base for base in bases if not base in seen and not seen.add(base))

            # the for loop bellow handles table inheritance
            for base in [base for base in bases if Database.BaseModel in base.__bases__]:
                if not hasattr(base, 'real_type'):
                    setattr(base, 'real_type', Column('real_type', String(24), nullable = False, index = True))
                if base.__mapper__.polymorphic_on is None:
                    base.__mapper__.polymorphic_on = base.__table__.c.real_type
                if base.__mapper__.polymorphic_identity is None:
                    base.__mapper__.polymorphic_identity = model_name_to_table_name(base.__name__)
                    
                #for ref_grandchildren
                models = Database.BaseModel.__subclasses__()
                for foreign_key in [foreign_key for foreign_key in base.__table__.foreign_keys 
                    if any(model_name_to_table_name(model.__name__) == foreign_key.column.table.name for model in models)]:
                    foreign_model = [model for model in models if model_name_to_table_name(model.__name__) == foreign_key.column.table.name][0]
                    setattr(foreign_model, model_name_to_table_name(name) + 's', 
                        property(lambda self: getattr(self, model_name_to_table_name(base.__name__) + 's').filter_by(real_type = model_name_to_table_name(name))))

                attrs['id'] = declared_attr(lambda cls: Column(Integer, ForeignKey('{0}.id'.format(model_name_to_table_name(base.__name__))), primary_key = True))
                attrs['__mapper_args__'] = declared_attr(lambda cls: {'polymorphic_identity': model_name_to_table_name(name)})              

            return DeclarativeMeta.__new__(cls, name, bases, attrs)


    class DefaultMeta(BaseMeta):
        """default metaclass for model classes, specify tablename and create a primary key for the model.
        All of user defined metaclasses should be either directly or indirectly derived from this class.
        """
        def __new__(cls, name, bases, attrs):
            attrs['__tablename__'] = declared_attr(lambda cls: model_name_to_table_name(cls.__name__))
            attrs['id'] = Column(Integer, primary_key = True)
            return Database.BaseMeta.__new__(cls, name, bases, attrs)    
    

    @staticmethod
    def MetaBuilder(*models):
        """Build a new model metaclass. The new metaclass is derived from Database.DefaultMeta,
        and it will add *models as base classes to the model classes.
        """
        class InnerMeta(Database.DefaultMeta):
            """metaclass for model classes, it will add *models as bases of the model classes."""
            def __new__(cls, name, bases, attrs):
                bases = list(bases)
                for model in models:
                    bases.append(model)
                seen = set()
                bases = tuple(base for base in bases if not base in seen and not seen.add(base))
                return Database.DefaultMeta.__new__(cls, name, bases, attrs)
        return InnerMeta
