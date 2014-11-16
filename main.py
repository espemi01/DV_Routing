import Router, pullSocket, Table
import queue

def main():
	myQueue = queue.Queue() #Make an empty queue to have things pushed to
	r = Router.Router("start.txt", myQueue)
	s = pullSocket.pullSocket(myQueue)

	r.start()
	s.start()

	

if __name__ == "__main__":
	main()