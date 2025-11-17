from demo07_module import *

print(__name__)
print(mon_module.addition(0, 1))

import demo07_module

print(dir(mon_module))
print(demo07_module.__all__)
print(demo07_module.__doc__)