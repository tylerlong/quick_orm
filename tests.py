import sys, subprocess
from toolkit_library.inspector import PackageInspector
from quick_orm import examples

# automatically install the newest code before testing
subprocess.call([sys.executable, 'setup.py', 'install'])

# call each example file and print the result
for module in PackageInspector(examples).get_all_modules():    
    print '****** {0} ******'.format(module)
    subprocess.call([sys.executable, 'quick_orm/examples/{0}.py'.format(module)])
    print
