import sys, subprocess
from toolkit_library.inspector import PackageInspector
from quick_orm import examples


for module in PackageInspector(examples).get_all_modules():
    print '****** {0} ******'.format(module)
    theproc = subprocess.Popen([sys.executable, "quick_orm/examples/{0}.py".format(module)])
    theproc.communicate()
    print ''
