from distutils.core import setup
import quick_orm
from quick_orm.examples import examples_list, examples_dict

def read_examples():
    result = ''
    for example_file in examples_list:
        result = '{0}\r\n|\r\n\r\n{1} example\r\n{2}\r\n\r\n::\r\n\r\n    {3}\r\n\r\n'.format(result, examples_dict[example_file], 
            '*' * (len(examples_dict[example_file]) + 8),
            '\r\n    '.join(open('quick_orm/examples/{0}.py'.format(example_file)).read().splitlines()))
    return result.rstrip()

readme = requirements = None
with open('README_template', 'r') as file:
    readme = file.read()
readme = readme.replace('{{ examples }}', read_examples())
with open('requires.txt', 'r') as file:
    text = file.read().rstrip()
    requirements = text.splitlines()
with open('quick_orm/core.py', 'r') as file:
    readme = readme.replace('{{ lines_count }}', str(len(file.read().splitlines())))
with open('README.rst', 'w') as file:
    file.write(readme)


setup(
    name = quick_orm.__name__,
    version = quick_orm.__version__,
    url = 'https://github.com/tylerlong/quick_orm',
    license = 'BSD',
    author = quick_orm.__author__,
    author_email = 'tyler4long@gmail.com',
    description = 'A python ORM, quick, easy, simple yet powerful, based on sqlalchemy.',
    long_description = readme,
    packages = ['quick_orm', 'quick_orm.examples', ],
    install_requires = requirements,
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
