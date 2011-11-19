from distutils.core import setup
import quick_orm
from quick_orm.examples import examples_list, examples_dict

def read_examples():
    result = ''
    for example_file in examples_list:
        result = '{0}{1} example\n{2}\n{3}\n\n\n'.format(result, examples_dict[example_file], 
            '*' * (len(examples_dict[example_file]) + 8),
            open('quick_orm/examples/{0}.py'.format(example_file)).read())
    return result.rstrip()

long_description = open('README').read().replace('{{ examples }}', read_examples())

setup(
    name = quick_orm.__name__,
    version = quick_orm.__version__,
    url = 'http://stackoverflow.com/users/862862/tyler-long',
    license = 'BSD',
    author = quick_orm.__author__,
    author_email = 'tyler4long@gmail.com',
    description = """A python orm which enables you to get started in less than a minute! Super easy to setup and super easy to use, yet super powerful! You would regret that you didn't discorver it earlier!""",
    long_description = long_description,
    packages = ['quick_orm', 'quick_orm.examples', ],
    install_requires = open('requirements.txt').read().splitlines(),
    platforms = 'any',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
