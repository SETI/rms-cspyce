################################################################################
# unittester.py: global unit-tester
################################################################################

from test_errors    import *
from test_kernels   import *
from test_nokernels import *

from test_cyl_lat_sph import *
from test_k           import *
from test_l           import *

################################################################################
# To run all unittests...

import unittest

if __name__ == '__main__':

    unittest.main(verbosity=2)

################################################################################
