
'''
Coursera:
- Software Defined Networking (SDN) course
-- Programming Assignment: Layer-2 Firewall Application

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta
'''

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
from pox.lib.util import dpid_to_str
import os
import csv
''' Add your imports here ... '''



log = core.getLogger()
policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ[ 'HOME' ]

''' Add your global variables here ... '''



class Firewall (EventMixin):

    def __init__ (self):
        self.listenTo(core.openflow)
        log.info("Enabling Firewall Module")

    def _handle_ConnectionUp (self, event):
		log.info("Switch %s has come up.", dpid_to_str(event.dpid))
		csvfile = open('/home/mininet/pox/pox/misc/firewall-policies.csv', 'rb')
		black_list=[]
		total_row=0
		for row in csv.reader(csvfile, delimiter=','):
			black_list.append(row)
			total_row=total_row+1
			
		for i in range (1,total_row):
			compare=black_list[i][1]+black_list[i][2]
			log.info("TTTT %s", EthAddr(black_list[i][1]))
			msg = of.ofp_flow_mod()
			msg.match.dl_dst=EthAddr(black_list[i][1])
			msg.match.dl_src=EthAddr(black_list[i][2])
			msg.priority = 100
			msg.actions.append(of.ofp_action_output(port = of.OFPP_NONE))
			event.connection.send(msg)
			'''
			msg2 = of.ofp_flow_mod()
			msg2.match.dl_src=EthAddr(black_list[i][1])
			msg2.match.dl_dst=EthAddr(black_list[i][2])
			msg2.idle_timeout = 10
			msg2.hard_timeout = 30
			msg2.priority = 100
			msg2.actions.append(of.ofp_action_output(port = of.OFPP_NONE))
			msg2.data = event.ofp # 6a
			event.connection.send(msg2)
			'''
			log.info("Firewall rules installed on %s", dpidToStr(event.dpid))
    def drop (duration = None):
      """
      Drops this packet and optionally installs a flow to continue
      dropping similar ones for a while
      """
      if duration is not None:
        if not isinstance(duration, tuple):
          duration = (duration,duration)
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet)
        msg.idle_timeout = duration[0]
        msg.hard_timeout = duration[1]
        msg.buffer_id = event.ofp.buffer_id
        self.connection.send(msg)
      elif event.ofp.buffer_id is not None:
        msg = of.ofp_packet_out()
        msg.buffer_id = event.ofp.buffer_id
        msg.in_port = event.port
        self.connection.send(msg)
		
def launch ():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)