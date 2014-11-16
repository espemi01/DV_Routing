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
		cost = int(cost)
		self.NT[name] = ip
		self.DVT[name] = [cost, name]

	def restart(self):
		return self.NT

	def update(self, name, cost, source): #checks if the updated information is new, if so, it updates the table accordingly; if not, it returns false
		cost = int(cost)
		total = cost + self.DVT[source][0]

		if name in self.DVT:
			if self.DVT[name][0] > total:
				self.DVT[name] = [total, source]
				return True
			else:
				return False
		else:
			self.DVT[name] = [total, source]
			return True

	def build(self): #Builds a table that is ready to send to the neighbors
		result = {}
		for i in self.DVT:
			if i != self.myName:
				result[i] = self.DVT[i][0]
		return result