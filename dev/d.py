#!/usr/bin/env python

import sys, time
from daemon import Daemon
import threading
import SocketServer

class ThreadedUDPHandler(SocketServer.BaseRequestHandler):
  """
  This class works similar to the TCP handler class, except that
  self.request consists of a pair of data and client socket, and since
  there is no connection the client address must be given explicitly
  when sending data back via sendto().
  """

  def handle(self):
    data = self.request[0].strip()
    socket = self.request[1]
    print "%s wrote:" % self.client_address[0]

    # Time...
    time.sleep(1)
    print '.',
    time.sleep(1)
    print '.',
    time.sleep(1)
    print '.',
    time.sleep(1)

    print data
    socket.sendto(data.upper(), self.client_address)

class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer): 
  pass


class MyDaemon(Daemon):
  def run(self):
    HOST, PORT = "localhost", 9999
    server = ThreadedUDPServer((HOST, PORT), ThreadedUDPHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()

    while True:
      # every ten seconds
      # take list, calculate numbers
      # write out rrd
      time.sleep(1)


if __name__ == "__main__":
	daemon = MyDaemon('/tmp/daemon-example.pid')
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart" % sys.argv[0]
		sys.exit(2)
