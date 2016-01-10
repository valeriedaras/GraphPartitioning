# -*- coding: utf-8 -*-
"""
@author: Valérie Daras, Julie Rivière
"""
import unittest

import objectivefunctions as objf
import script as s


class TestObjFunctions(unittest.TestCase):

    def testCalculateWeight(self):
        # init : creation of json conf file
        # in this test, the config file does not contain json data
        try:
            copyFilename = "graphs/ex2.graph"
            graph = s.createGraph(copyFilename)
        except Exception:
            self.fail("Error during graph creation")
        else:
        # TEST
            self.assertTrue(objf.calculateWeight(1,2,graph) == 5)
            self.assertTrue(objf.calculateWeight(1,5,graph) == 2)
            self.assertTrue(objf.calculateWeight(2,1,graph) == 5)
            self.assertTrue(objf.calculateWeight(1,1,graph) == 0)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestObjFunctions)
    unittest.TextTestRunner(verbosity=2).run(suite)