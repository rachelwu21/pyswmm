#!/usr/bin/env python

""" Test suite to test polygon functionality. """

import unittest
import numpy as np
import os

from pyswmm import Simulation, Nodes, Links

class Test_SwmmLink(unittest.TestCase):
    
    def setUp(self):
        sim = self.sim = Simulation('./swmm_pipe_test.inp')
        

        node_names = ['Inlet', 'Outlet']
        link_names = ['Culvert']
    
        nodes = self.nodes = [Nodes(sim)[names] for names in node_names]
        links = self.links = [Links(sim)[names] for names in link_names]

        openning0 = self.nodes[0].create_opening(4, 1.0, 1.0, 0.6, 1.6, 1.0)
        self.nodes[0].overland_depth = 1.0

        self.sim.start()



    def tearDown(self):
        self.nodes = None
        self.links = None
        self.sim.report()
        self.sim.close()


    def test_establishment_of_a_swmmlink(self):
        assert self.nodes[0].total_outflow == 0

    def test_simple_pipe(self):
        #FIXME: Not yet done
        for ind, step in enumerate(self.sim):
            self.sim.step_advance(1.0)

            for node in self.nodes:
                pass
                #FIXME (Ole): Todo
                #print 'total_inflow', node.total_inflow
                #print 'total_outflow', node.total_outflow
             


        
################################################################################

if __name__ == "__main__":
    suite = unittest.makeSuite(Test_SwmmLink, 'test')
    runner = unittest.TextTestRunner()
    runner.run(suite)
