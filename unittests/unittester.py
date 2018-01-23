################################################################################
# unittester.py: global unit-tester
################################################################################

from unittester_errors     import *
from unittester_kernels    import *
from unittester_nokernels  import *

################################################################################
# To run all unittests...

import unittest

if __name__ == '__main__':

    unittest.main(verbosity=2)

################################################################################
