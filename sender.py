from threading import Thread
import json

class sender(Thread):
	def __init__(self, q):
		Thread.__init__(self)
		self.q = q
		self.msg = {'type':'message', 'source':'mike'}

	def run(self):
		while 1:
			content = input("What would you like your message to say: ")
			dest = input("Who would you like to send your message to: ")

			self.msg['message'] = {'content':content, 'destination':dest, 'path':['mike']}

			msgJSON = json.dumps(self.msg)
			msgOUT = msgJSON.encode('utf-8')
			self.q.put(msgOUT)