# coding=utf-8
"""
    manage
    ~~~~~~
    Provides useful commands to manage the project
"""
import sys, subprocess
from toolkit_library.inspector import ModuleInspector, PackageInspector
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
    run_testsuite()


if __name__ == '__main__':
    inspector = ModuleInspector(sys.modules[__name__])
    inspector.invoke(*sys.argv[1:])
