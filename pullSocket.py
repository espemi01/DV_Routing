import socket
from threading import Thread

class pullSocket(Thread): #reads the values from the socket and pushes them to the queue to be processed by the router process.
	def __init__(self, queue1):
		Thread.__init__(self)
		self.queue = queue1
		self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.s.bind(('', 50007))
		print('open on port on 50007')

	def run(self):
		while 1:
			p, _ = self.s.recvfrom(1024)
			self.queue.put(p)