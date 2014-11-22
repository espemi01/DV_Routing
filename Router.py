from threading import Thread
import json, socket, Table

class Router(Thread): #does all the processing
	def __init__(self, initFile, queue):
		Thread.__init__(self)
		self.queue = queue
		self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.s.bind(("",50008))
		self.t = Table.Table()
		self.myName = 'mike'

		self.t, self.name = self.makeTable(initFile)

	def makeTable(self, initFile): #sets neighbors
		myFile = open(initFile, 'r')
		myName = ''
		t = Table.Table()

		for i in myFile:
			line = i.strip()
			name, cost, ip = line.split(' ')

			cost = int(cost)
			if (cost == 0):
				self.t.addSelf()

			else:
				anIP = ip.strip()
				cost = int(cost)
				t.add(name, cost, anIP)

		myFile.close()
		return (t, myName)

	def run(self):
		self.restart()
		print('running')
		self.pushUpdate()
		while True:
			packet = self.queue.get()
			msgIN = json.loads(packet.decode('utf-8'))
			print('got something...')

			if msgIN['type'] == 'table':
				if self.gotUpdate(msgIN['table'],msgIN['source']):
					print("Got an update from: ", msgIN['source'])
					print(self.t.DVT)
					self.pushUpdate()

			elif msgIN['type'] == 'message':
				if self.gotMessage(msgIN):
					print("You Received: ", msgIN['message']['content'])
					print("Path: ", msgIN['message']['path'])
				elif len(msgIN['message']['path']) == 1:
					self.sendMSG(msgIN)
				else:
					msgIN['message']['path'].append(self.myName)
					self.fwdMSG(msgIN)
					print("Message to ", msgIN['message']['destination'], " forwarded...")

			elif msgIN['type'] == 'restart':
				self.pushUpdate()

			else:
				print ("JSON type: ", msgIN['type'], " is not a valid type")

	def gotMessage(self, msg):
		if msg['message']['destination'] == self.myName:
			return True
		return False

	def restart(self):
		msg = {'type': 'restart'}
		result = json.dumps(msg)

		t = Table.Table()
		NT = self.t.NT

		for i in NT:
			self.s.sendto(result.encode('utf-8'),(NT[i], 50007))

	def gotUpdate(self, t, source):
		status = False
		for a in t:
			if self.t.update(a, t[a], source):
				status = True
		return status

	def makeUpdate(self):
		res = {'type':'table', 'source':self.myName}
		res['table'] = self.t.build()

		result = json.dumps(res)
		return [result.encode('utf-8'),self.t.NT]

	def pushUpdate(self):
		j, t = self.makeUpdate()
		for i in t:
			self.s.sendto(j,(t[i], 50007))

	def fwdMSG(self, msgIN):
		destNAME = msgIN['message']['destination']
		nextHop = self.t.DVT[destNAME][1]
		print(nextHop)

		addr = self.t.NT[nextHop]
		print(addr)

		msgJSON = json.dumps(msgIN)
		msgOUT = msgJSON.encode('utf-8')
		print(msgOUT)
		self.s.sendto(msgOUT, (addr, 50007))

	def sendMSG(self, msgIN):
		destNAME = msgIN['message']['destination']
		nextHop = self.t.DVT[destNAME][1]
		print(nextHop)

		addr = self.t.NT[nextHop]
		print(addr)

		msgJSON = json.dumps(msgIN)
		msgOUT = msgJSON.encode('utf-8')
		print(msgOUT)
		self.s.sendto(msgOUT, (addr, 50007))