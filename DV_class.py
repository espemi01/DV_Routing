# a cost of 0 means you are the host.

import socket
from threading import Thread

class Table: #holds the value pulled from the queue pushed from the socket

	def __init__(self):
		self.myName = ''
		self.DVT = {} 
		self.NT = {}

	def addSelf(self, name): #adding a value with the cost of 0 to signify this host is the sender to other nodes
		self.myName = name
		self.DVT[name] = [0, name]

	def add(self, name, cost, ip): #appends a new node to the existing table
		self.NT[name] = ip
		self.DVT[name] = [cost, name]

	def update(self, name, cost, x): #checks if the updated information is new, if so, it updates the table accordingly; if not, it returns false
		total = cost + self.DVT[x][0]

		if name in self.DVT:
			if self.DVT[name][0] > total:
				self.DVT[name] = [total, x]
				return true
			else:
				return false
		else:
			self.DVT[name] = [total, x]
			return true

	def build(self): #Builds a table that is ready to send to the neighbors
		result = {}
		for i in self.DVT:
			if i != self.myName:
				result[i] = self.DVT[i][0]
		return result

class ReadIn(Thread): #reads the values from the socket and pushes them to the queue to be processed by the router process.
	def __init__(self, queue):
		Thread.__init__(self)
		self.queue = queue
		self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.s.bind(('', 50007))

	def run(self):
		while 1:
			p = self.s.recvfrom(1024)
			self.queue.put(p)