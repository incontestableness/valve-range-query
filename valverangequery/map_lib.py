import socket, struct, sys
import threading
import time
import logging

from .source_packet import *

PACKETSIZE=1400
WHOLE=-1
SPLIT=-2

# IP_BASE_ADDRESS_A = "192.168"		#For within a subnet
# IP_BASE_ADDRESS_A = "172.25"		#For intranet

server_list = []
class sendThread (threading.Thread):
	def __init__(self, axlimits, aylimits, udp, port, wait, base_ipaddr, force_list):
		threading.Thread.__init__(self)
		self.axlimits = axlimits
		self.aylimits = aylimits
		self.udp = udp
		self.port = port
		self.wait = wait
		self.base_ipaddr = base_ipaddr
		self.force_list = force_list
	def run(self):
		logging.info("Starting Sender Thread")

		spacket = SourceQueryPacket()
		spacket.putLong(WHOLE)
		spacket.putByte(A2S_INFO)
		spacket.putString(A2S_INFO_STRING)

		if self.force_list == []: 
			# Create a list of IP addresses to scan from the limits we were given
			for i in list(range(self.axlimits[0], self.axlimits[1] + 1)):
				base_ip = self.base_ipaddr + "." + str(i) + "."
				for j in list(range(self.aylimits[0], self.aylimits[1] + 1)):
					current_ip = base_ip + str(j)
					self.force_list.append(current_ip)

		for current_ip in self.force_list: 
			logging.debug("Scanning " + current_ip)
			try:
				self.udp.sendto(spacket.getvalue(),(current_ip, self.port))
			except socket.error as msg:
				if(msg[0] == 1):
					logging.debug("Sender Error at ip "+ current_ip + " error: " + str(msg))
				else:
					logging.info("Sender Error at ip "+ current_ip + " error: " + str(msg))
				continue
			time.sleep(self.wait);
		logging.info("Sender Thread Ended")

class receiverThread (threading.Thread):
	def __init__(self, udp):
		threading.Thread.__init__(self)
		self.udp = udp

	def run(self):
		logging.info("Starting Receiver Thread")
		global server_list
		while True:
			try:
				packet, addr = self.receive()
			except (socket.error, socket.timeout) as msg:
				if type(msg) == socket.timeout:
					logging.info("Receiver timed out")
					break
				elif msg[0] == 111:					 #Error Connection Refused
					logging.exception("Receiver Error " + str(msg))
				else:
					logging.exception("Receiver Error " + str(msg))
					continue
			except KeyboardInterrupt:
				logging.error("KeyboardInterrupt exiting...")	
				sys.exit(0)
			else:
				dat= packet.parsePacket()
				logging.debug("Parsed map info from "+addr[0])
				server_list.append(dat)
		logging.info("Receiver Thread Ended")

	def receive(self):
		try:
			data, addr = self.udp.recvfrom(PACKETSIZE)
		except (socket.error, socket.timeout) as msg:
			raise
		except KeyboardInterrupt:
			logging.error("KeyboardInterrupt exiting...")	
			sys.exit(0)
		else:
			logging.debug("Data received from" + str(addr))
			packet = SourceQueryPacket(data)
			typ = packet.getLong()

			if typ == WHOLE:
				logging.debug("Whole Packet")
				packet.host = addr[0]
				return packet,addr

			elif typ == SPLIT:
				# handle split packets
				logging.debug("Split Packet")
				reqid = packet.getLong()
				total = packet.getByte()
				num = packet.getByte()
				splitsize = packet.getShort()
				result = [0 for x in xrange(total)]

				result[num] = packet.read()

				# fetch all remaining splits
				while 0 in result:
					packet = SourceQueryPacket(self.udp.recv(PACKETSIZE))

					if packet.getLong() == SPLIT and packet.getLong() == reqid:
						total = packet.getByte()
						num = packet.getByte()
						splitsize = packet.getShort()
						result[num] = packet.read()

					else:
						raise SourceQueryError('Invalid split packet')

				packet = SourceQueryPacket("".join(result))

				if packet.getLong() == WHOLE:
					packet.host = addr[0]
					return packet,addr
				else:
					raise SourceQueryError('Invalid split packet')
			else:
				raise SourceQueryError("Received invalid packet type %d" % (typ,))

class SourceScanner(object):
	def __init__(self, port=27015, timeout=2.0, axlimits=[1,255], aylimits=[1,255], wait=0.2, base_ipaddr = "172.25", force_list=[]):
			self.port = port
			self.wait = wait
			self.timeout = timeout
			self.axlimits = axlimits
			self.aylimits = aylimits
			self.udp = False
			self.result = []
			self.base_ipaddr = base_ipaddr
			self.force_list = force_list

	def scan_servers(self):
			self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			self.udp.settimeout(self.timeout)
			self.udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

			global server_list 
			server_list = []

			rthread = receiverThread(self.udp)
			rthread.start()

			sthread = sendThread(self.axlimits, self.aylimits, self.udp, self.port, self.wait, self.base_ipaddr, self.force_list)
			sthread.start()
			sthread.join()

			rthread.join()

			return server_list
