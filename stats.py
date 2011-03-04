#!/usr/bin/env python

import os, sys, time
import corestats
from pyrrd.rrd import DataSource, RRA, RRD
from pyrrd.graph import DEF, CDEF, VDEF, LINE, AREA, GPRINT
from pyrrd.graph import ColorAttributes
from pyrrd.graph import Graph

class StatsRecorder:
  def __init__(self, filename):
    if os.path.isfile(filename):
      self.rrd = RRD(filename)
    else:
      dataSources = []
      dataSources.append( DataSource(dsName='q1', dsType='GAUGE', heartbeat=600, minval=0) )
      dataSources.append( DataSource(dsName='q2', dsType='GAUGE', heartbeat=600, minval=0) )
      dataSources.append( DataSource(dsName='q3', dsType='GAUGE', heartbeat=600, minval=0) )
      dataSources.append( DataSource(dsName='lo', dsType='GAUGE', heartbeat=600, minval=0) )
      dataSources.append( DataSource(dsName='hi', dsType='GAUGE', heartbeat=600, minval=0) )
      dataSources.append( DataSource(dsName='total', dsType='GAUGE', heartbeat=600, minval=0) )

      roundRobinArchives = []
      roundRobinArchives.append(RRA(cf='AVERAGE', xff=0.5, steps=1, rows=8640)) # 24h at 1 sample per 10 secs
      roundRobinArchives.append(RRA(cf='AVERAGE', xff=0.5, steps=90, rows=2880)) # 1 month at 1 sample per 15 mins
      roundRobinArchives.append(RRA(cf='AVERAGE', xff=0.5, steps=2880, rows=5475)) # 5 years at 1 sample per 8 hours

      self.rrd = RRD(filename, step=10, ds=dataSources, rra=roundRobinArchives, start=int(time.time()))
      self.rrd.create()

    self.bucket = { 'a': [], 'b': [] }
    self.current_bucket = 'a'

  def add(self, value):
    self.bucket[self.current_bucket].append(value)

  def save(self):
    bucket = self.current_bucket

    if self.current_bucket == 'a':
      self.current_bucket = 'b'
    else:
      self.current_bucket = 'a'

    stats = corestats.Stats(self.bucket[bucket])

    q1 = stats.percentile(25)
    q2 = stats.percentile(50)
    q3 = stats.percentile(75)
    lo = stats.min()
    hi = stats.max()
    total = stats.count()

    self.bucket[bucket] = []

    self.rrd.bufferValue(str(int(time.time())), q1, q2, q3, lo, hi, total)
    self.rrd.update()
