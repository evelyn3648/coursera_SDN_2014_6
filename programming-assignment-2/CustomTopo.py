'''
Coursera:
- Software Defined Networking (SDN) course
-- Programming Assignment 2

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta, Muhammad Shahbaz
'''

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel
from CustomTopo import *
class CustomTopo(Topo):
    "Simple Data Center Topology"

    "linkopts - (1:core, 2:aggregation, 3: edge) parameters"
    "fanout - number of child switch per parent switch"
    def __init__(self, linkopts1, linkopts2, linkopts3, fanout=2, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)
        
        # Add your logic here  ..
	core_switch = self.addSwitch('c0')
	agg_switch = [self.addSwitch('a%s' %i) for i in irange(1,fanout)]
	for i in range (0,fanout):
		self.addLink(core_switch, agg_switch[i], **linkopts1)

        edge_switch = [self.addSwitch('e%s' %j) for j in irange (1,fanout*fanout)]
	for j in range (0,fanout*fanout):
		print "J= %d"%(j)
	       	self.addLink(agg_switch[j/fanout], edge_switch[j], **linkopts2)
	
	host = [self.addHost('h%s'%k) for k in irange (1,fanout*fanout*fanout)]
	for k in range (0,fanout*fanout*fanout):
		print "K= %d"%(k)
	        self.addLink(edge_switch[k/fanout], host[k], **linkopts3)
		

        
                    
topos = { 'custom': ( lambda: CustomTopo() ) }


'''
def SimpleTest():
    "Set up link parameters"
    print "a. Setting link parameters"
    "--- core to aggregation switches"
    linkopts1 = {'bw':50, 'delay':'5ms'}
    "--- aggregation to edge switches"
    linkopts2 = {'bw':30, 'delay':'10ms'}
    "--- edge switches to hosts"
    linkopts3 = {'bw':10, 'delay':'15ms'}
 
    "Creating network and run simple performance test"
    print "b. Creating Custom Topology"
    topo = CustomTopo(linkopts1, linkopts2, linkopts3, fanout=2)
 
    print "c. Firing up Mininet"
    net = Mininet(topo=topo, link=TCLink)
    net.start()
    dumpNodeConnections(net.hosts)
#    h1 = net.get('h1')
#    h27 = net.get('h27')
 
#    print "d. Starting Test"
    # Start pings
#    outputString = h1.cmd('ping', '-c6', h27.IP())
 
    print "e. Stopping Mininet"
    net.stop()
 
 
if __name__ == '__main__':
    #logging.basicConfig(level=logging.DEBUG)
    #logger = logging.getLogger("sdn2")
    SimpleTest()
'''
