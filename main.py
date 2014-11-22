import Router, pullSocket, Table, sender
import queue

def main():
	myQueue = queue.Queue() #Make an empty queue to have things pushed to
	r = Router.Router("start.txt", myQueue)
	s = pullSocket.pullSocket(myQueue)
	send = sender.sender(myQueue)

	r.start()
	s.start()
	send.start()

	

if __name__ == "__main__":
	main()