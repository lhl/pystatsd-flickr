#!/usr/bin/env python

import sys, threading, time
import SocketServer

from daemon import Daemon

import logging
LOG_FILENAME = '/var/statsd/index-time.log'
logging.basicConfig(filename=LOG_FILENAME,level=logging.INFO,)

from stats import StatsRecorder
sr = StatsRecorder('/var/statsd/index-time.rrd')


class StatsDaemon(Daemon):
  def run(self):
    global sr
    logging.debug('Starting Stats Daemon...')
    HOST, PORT = "", 57475
    server = ThreadedUDPServer((HOST, PORT), ThreadedUDPHandler)

    server_thread = threading.Thread(target=server.serve_forever)
    # server_thread.setDaemon(True)
    server_thread.start()
    logging.debug('Server loop running in thread:', server_thread.getName())

    while True:
      logging.debug('udpserver running...')
      sr.save()
      time.sleep(5)
  

class ThreadedUDPHandler(SocketServer.BaseRequestHandler):
  def handle(self):
    global sr
    data = self.request[0].strip()
    socket = self.request[1]
    # logging.debug("%s wrote:" % self.client_address[0])
    sr.add(float(data))
    # socket.sendto(data.upper(), self.client_address)

class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer): 
  pass





if __name__ == "__main__":
  daemon = StatsDaemon('/var/statsd/statsd.pid')
  if len(sys.argv) == 2:
    if 'start' == sys.argv[1]:
      daemon.start()
    elif 'stop' == sys.argv[1]:
      daemon.stop()
    elif 'restart' == sys.argv[1]:
      daemon.restart()
    else:
      print "usage: %s start|stop|restart" % sys.argv[0]
      sys.exit(2)
    sys.exit(0)
  else:
    print "usage: %s start|stop|restart" % sys.argv[0]
    sys.exit(2)
