"""pyswmm example

The purpose of this example is to understand the parameters that at each timestep can 
* control the pipe network
* be derived from the pipe network

It is our hope to eventually couple pyswmm with anuga through these parameters 
to create a better open source 2D urban flood model.

Stephen Roberts, Petar Milevski, Rudy van Drie, Ole Nielsen
December 2018 
"""

from pyswmm import Simulation, Nodes, Links

def run_swmm():

    #=======================================
    # setup all the nodes before starting
    #=======================================
    
    sim = Simulation('./swmm_pipe_test.inp')

    node_names = ['Inlet', 'Outlet']
    link_names = ['Culvert']
    
    nodes = [Nodes(sim)[names] for names in node_names]
    links = [Links(sim)[names] for names in link_names]
    
    # type, area, length, orifice_coeff, free_weir_coeff, submerged_weir_coeff
    opening0 = nodes[0].create_opening(4, 1.0, 1.0, 0.6, 1.6, 1.0)

    print
    print "n0 is coupled? ", nodes[0].is_coupled
    print "n1 is coupled? ", nodes[1].is_coupled


    #=======================================
    # Start the simulation
    #=======================================   
    sim.start()

    nodes[0].overland_depth = 1.0
    nodes[0].coupling_area = 1.0

    # This step_advance should be an integer multiple of the routing step
    # which is set in the ,inp file. Currently set to 1s.
    # Should be able to interrogate sim to find out what the
    # routing stepsize is. Maybe should issue a warning if
    # step_advance is set lower than the routing step size.
    # Indeed maybe step_advance should just allow advance n routing steps?
    
    for ind, step in enumerate(sim):
        sim.step_advance(1.0)

        if ind == 15:
            break    # Output from first 15 steps in enough
            
        print 70 * "="
        print 'STEP ', ind
        
        elapsed_time = (sim.current_time - sim.start_time).total_seconds()
        
        print 'Current time', sim.current_time
        print 'Elapsed time', elapsed_time
        print 'Advance seconds', sim._advance_seconds
        print 'Opening 0 flow', opening0.flow
        
        for i, j in enumerate(nodes):
            print 50*"="
            jstr = node_names[i]
            print jstr+' total_inflow', j.total_inflow
            print jstr+' total_outflow', j.total_outflow
            print jstr+' coupling_inflow', j.coupling_inflow
            
            print jstr+' coupling_area', j.coupling_area
            print jstr+' overland_depth', j.overland_depth
            print jstr+' number of openings', j.number_of_openings
            print jstr+' depth', j.depth
            print jstr+' volume', j.volume
            print jstr+' surcharge depth', j.surcharge_depth
            print jstr+' flooding', j.flooding
            print jstr+' lateral_inflow', j.lateral_inflow
 
        for i, l in enumerate(links):
            print 50*"="
            lstr = link_names[i]
            print lstr+' link flow', l.flow
            
            print lstr+' Area', l.ds_xsection_area   
            print lstr+' Froude', l.froude
            print lstr+' Depth', l.depth
            print lstr+' Flow limit' , l.flow_limit
            print lstr+' volume', l.volume
 
      
    print 70 * "="  
    print 'Current Time', sim.current_time
    print 'End time', sim.end_time
    print 'Elapsed time', (sim.current_time - sim.start_time).total_seconds()
    
    sim.report()
    sim.close()
        
run_swmm()


